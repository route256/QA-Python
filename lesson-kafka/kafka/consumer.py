import json
from dataclasses import is_dataclass, asdict

from confluent_kafka import DeserializingConsumer


class Consumer:
    def __init__(self):
        self.consumer = DeserializingConsumer({
            "bootstrap.servers": "127.0.0.1:9092",
            "group.id": "route",
            "auto.offset.reset": "latest",
            "value.deserializer": self._value_deserializer
        })

    def _value_deserializer(self, value, ctx):
        if value is not None:
            return json.loads(value.decode('utf-8'))
        return value

    def get_message(self, topics, body_filter: dict):
        self.consumer.subscribe(topics=topics)
        while True:
            message = self.consumer.poll(1.0)
            if message is None:
                continue
            if is_dataclass(body_filter):
                body_filter = asdict(body_filter)

            if not (body_filter.items() <= message.value().items()):
                continue
            print(f"Received message: {message.value()}")
            return message.value()

    # def get_messages(self, topics, body_filter):
    #     messages = []
    #         message = self.get_message(topics, body_filter)
    #         messages.append(message)
    #     return messages

