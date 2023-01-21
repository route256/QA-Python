from dataclasses import dataclass


@dataclass(frozen=True)
class DeviceResponse:
    id: str
    platform: str
    userId: str
    enteredAt: str
