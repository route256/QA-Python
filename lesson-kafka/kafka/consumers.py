from dacite import from_dict

from kafka import Consumer
from kafka.models import order_events


def model(schema):
    def wrapper(func):
        def callback(*args, **kwargs):
            message = func(*args, **kwargs)
            return from_dict(data_class=schema, data=message)
        return callback
    return wrapper


class Consumers:
    @model(order_events.Message)
    def order_events(self, body_filter=None):
        return Consumer().get_message(topics=["order-events"], body_filter=body_filter)

    # @model(item_events.Message)
    def item_events(self, body_filter=None):
        return Consumer().get_message(topics=["order-events"], body_filter=body_filter)