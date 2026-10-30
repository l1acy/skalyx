import json
from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from skalyx import ble_adapter, bus, storage
from skalyx.api.v1.schemas import ModuleHealth, SystemHealthResponse
from skalyx.schemas.event import Event

rest_router = APIRouter()
data_types = {
    'str': str,
    'int': int,
    'bool': bool,
    'float': float
}


@rest_router.get('/system/health')
async def get_system_health() -> SystemHealthResponse:
    bus_is_ok = bus.get_status()
    bus_status = ModuleHealth(
        module='bus',
        is_ok=bus_is_ok,
        message=""
    )

    ble_adapter_is_ok = ble_adapter.get_status()
    ble_adapter_status = ModuleHealth(
        module='ble_adapter',
        is_ok=ble_adapter_is_ok,
        message=""
    )

    return [bus_status, ble_adapter_status]


@rest_router.get('/history')
async def get_sensors_history():
    if not storage.connection:
        raise HTTPException(status_code=HTTPStatus.SERVICE_UNAVAILABLE)

    cursor = await storage.connection.execute("SELECT * FROM records")
    data_raw = await cursor.fetchall()

    return [
        Event(
            device_id=device_id,
            source=source,
            metric=metric,
            value=data_types[value_type](value),
            unit=unit,
            timestamp=timestamp,
            meta=json.loads(meta)) for _, device_id, source, metric,value,unit,timestamp,meta,value_type in data_raw
    ]
