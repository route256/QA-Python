from dataclasses import dataclass


@dataclass
class Message:
    order_ids: int = None
    status_id: int = None
    name: str = None
