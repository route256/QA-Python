import json

from confluent_kafka import Producer as OriginalProducer

class Producer:
    def __init__(self):
        self.producer = OriginalProducer({
            "bootstrap.servers": "127.0.0.1:9092"
        })

    def __call__(self, data):
        self.producer.produce(topic="order-events", value=json.dumps(data))
        self.producer.flush()
        print(f'Message {data} has been produced.')