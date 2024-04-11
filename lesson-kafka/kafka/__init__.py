from kafka.consumer import Consumer
from kafka.producer import Producer

if __name__ == "__main__":
    producer = Producer()
    producer({"order_ids": 909, "status_id": 100})
    message = Consumer().get_message(topics=["order-events"])

    assert message
    pass