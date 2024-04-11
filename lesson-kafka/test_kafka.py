import random
from dataclasses import asdict

import pytest

from kafka import Producer, Consumer
from kafka.consumers import Consumers
from kafka.models import order_events


@pytest.fixture
def create_order():
    data = {"order_ids": random.randint(10, 100), "status_id": random.randint(10, 100)}
    producer = Producer()({"order_ids": random.randint(10, 100), "status_id": random.randint(10, 100)})
    producer = Producer()({"order_ids": random.randint(10, 100), "status_id": random.randint(10, 100)})
    producer = Producer()(data)
    producer = Producer()({"order_ids": random.randint(10, 100), "status_id": random.randint(10, 100)})
    return data



class TestKafka:
    def test_consumer_kafka(self):
        producer = Producer()({"order_ids": 909, "status_id": 100})
        # some .... sql.get('')
        # assert

    def test_producer_kafka(self, create_order):
        message = Consumers().order_events(body_filter={"order_ids": create_order["order_ids"]})

        assert message.order_ids == create_order["order_ids"]
        assert message.status_id == create_order["status_id"]
