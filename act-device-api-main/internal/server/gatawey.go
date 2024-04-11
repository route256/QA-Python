package server

import (
	"context"
	"crypto/sha256"
	"crypto/subtle"
	"errors"
	grpc_opentracing "github.com/grpc-ecosystem/go-grpc-middleware/tracing/opentracing"
	"github.com/grpc-ecosystem/grpc-gateway/v2/runtime"
	"github.com/opentracing/opentracing-go"
	"github.com/opentracing/opentracing-go/ext"
	"github.com/ozonmp/act-device-api/internal/config"
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promauto"
	"github.com/rs/zerolog/log"
	"google.golang.org/grpc"
	"net/http"
	_ "net/http/pprof"

	pb "github.com/ozonmp/act-device-api/pkg/act-device-api"
)

var (
	httpTotalRequests = promauto.NewCounter(prometheus.CounterOpts{
		Name: "http_microservice_requests_total",
		Help: "The total number of incoming HTTP requests",
	})
)

var grpcGatewayTag = opentracing.Tag{Key: string(ext.Component), Value: "grpc-gateway"}

func tracingWrapper(h http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		httpTotalRequests.Inc()
		parentSpanContext, err := opentracing.GlobalTracer().Extract(
			opentracing.HTTPHeaders,
			opentracing.HTTPHeadersCarrier(r.Header))
		if err == nil || errors.Is(err, opentracing.ErrSpanContextNotFound) {
			serverSpan := opentracing.GlobalTracer().StartSpan(
				"ServeHTTP",
				ext.RPCServerOption(parentSpanContext),
				grpcGatewayTag,
			)
			r = r.WithContext(opentracing.ContextWithSpan(r.Context(), serverSpan))
			defer serverSpan.Finish()
		}
		h.ServeHTTP(w, r)
	})
}

func authHandler(next http.Handler, userCfgHash [32]byte, passCfgHash [32]byte) http.Handler {
	return http.HandlerFunc(func(rw http.ResponseWriter, r *http.Request) {
		user, pass, ok := r.BasicAuth()
		log.Info().Msgf("r %s", ok)

		if ok {
			log.Info().Msgf("User and pass from config %s", userCfgHash, passCfgHash)

			userHash := sha256.Sum256([]byte(user))
			passHash := sha256.Sum256([]byte(pass))
			log.Info().Msgf("User and pass from header %s", userHash, passHash)

			if subtle.ConstantTimeCompare(userHash[:], userCfgHash[:]) == 1 && subtle.ConstantTimeCompare(passHash[:], passCfgHash[:]) == 1 {
				next.ServeHTTP(rw, r)
				return
			}
		}
		http.Error(rw, "Invalid Credentials, use echo -ne 'ozon:route256' for Basic header", http.StatusUnauthorized)
	})
}

func createGatewayServer(grpcAddr, gatewayAddr string) *http.Server {
	// Create a client connection to the gRPC Server we just started.
	// This is where the gRPC-Gateway proxies the requests.
	conn, err := grpc.DialContext(
		context.Background(),
		grpcAddr,
		grpc.WithUnaryInterceptor(
			grpc_opentracing.UnaryClientInterceptor(
				grpc_opentracing.WithTracer(opentracing.GlobalTracer()),
			),
		),
		grpc.WithInsecure(),
	)
	if err != nil {
		log.Fatal().Err(err).Msg("Failed to dial server")
	}
	cfg := config.GetConfigInstance()
	userCfgHash := sha256.Sum256([]byte(cfg.Rest.User))
	passCfgHash := sha256.Sum256([]byte(cfg.Rest.Password))

	mux := runtime.NewServeMux()

	if err := pb.RegisterActDeviceApiServiceHandler(context.Background(), mux, conn); err != nil {
		log.Fatal().Err(err).Msg("Failed registration handler")
	}

	gatewayServer := &http.Server{
		Addr:    gatewayAddr,
		Handler: authHandler(tracingWrapper(mux), userCfgHash, passCfgHash),
	}

	return gatewayServer
}
