from typing import Any, Literal

from pydantic import BaseModel

EventSource = Literal['ble', 'http']


class Event(BaseModel):
    device_id: str
    source: EventSource
    metric: str
    value: Any
    unit: str
    timestamp: str
    meta: Any
