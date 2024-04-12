# Builder

ARG GITHUB_PATH=github.com/ozonmp/act-device-api

FROM --platform=linux/x86_64 golang:1.16-alpine AS builder
RUN apk add --update make curl git protoc protobuf protobuf-dev
COPY . /home/${GITHUB_PATH}
WORKDIR /home/${GITHUB_PATH}
RUN make deps-go && make build-go

# gRPC Server

FROM --platform=linux/x86_64 alpine:latest as server
LABEL org.opencontainers.image.source https://${GITHUB_PATH}
RUN apk --no-cache add ca-certificates
RUN apk --no-cache add curl
WORKDIR /root/

COPY --from=builder /home/${GITHUB_PATH}/bin/grpc-server .
COPY --from=builder /home/${GITHUB_PATH}/config.yml .
COPY --from=builder /home/${GITHUB_PATH}/migrations/ ./migrations

RUN chown root:root grpc-server

EXPOSE 50051
EXPOSE 8080
EXPOSE 9100

CMD ["./grpc-server"]
