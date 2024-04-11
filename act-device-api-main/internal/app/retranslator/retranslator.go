package retranslator

import (
	"github.com/ozonmp/act-device-api/internal/app/repo"
	"time"

	"github.com/gammazero/workerpool"
	"github.com/ozonmp/act-device-api/internal/app/consumer"
	"github.com/ozonmp/act-device-api/internal/app/producer"
	"github.com/ozonmp/act-device-api/internal/app/sender"
	"github.com/ozonmp/act-device-api/internal/model"
)

type Retranslator interface {
	Start()
	Close()
}

type Config struct {
	ChannelSize uint64

	ConsumerCount  uint64
	ConsumeSize    uint64
	ConsumeTimeout time.Duration

	ProducerCount uint64
	WorkerCount   int

	Repo   repo.EventRepo
	Sender sender.EventSender
}

type retranslator struct {
	events     chan model.DeviceEvent
	consumer   consumer.Consumer
	producer   producer.Producer
	workerPool *workerpool.WorkerPool
}

func NewRetranslator(cfg Config) Retranslator {
	events := make(chan model.DeviceEvent, cfg.ChannelSize)
	workerPool := workerpool.New(cfg.WorkerCount)

	c := consumer.NewDbConsumer(
		cfg.ConsumerCount,
		cfg.ConsumeSize,
		cfg.ConsumeTimeout,
		cfg.Repo,
		events)
	p := producer.NewKafkaProducer(
		cfg.ProducerCount,
		cfg.Sender,
		cfg.Repo,
		events,
		workerPool)

	return &retranslator{
		events:     events,
		consumer:   c,
		producer:   p,
		workerPool: workerPool,
	}
}

func (r *retranslator) Start() {
	r.producer.Start()
	r.consumer.Start()
}

func (r *retranslator) Close() {
	r.consumer.Close()
	r.producer.Close()
	r.workerPool.StopWait()
}
