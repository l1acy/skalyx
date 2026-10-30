import logging
import threading
from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from enum import Enum
from typing import Any

logger = logging.getLogger("core.registry")


class DeviceStatus(str, Enum):
    UNKNOWN = "unknown"
    ONLINE = "online"
    OFFLINE = "offline"
    ERROR = "error"


@dataclass
class DeviceRecord:
    device_id: str
    source: str
    name: str | None = None
    config: dict[str, Any] = field(default_factory=dict)

    status: DeviceStatus = DeviceStatus.UNKNOWN
    last_seen: datetime | None = None
    last_error: str | None = None


class DeviceRegistry:
    def __init__(self, offline_after: timedelta = timedelta(minutes=5)):
        self._offline_after = offline_after
        self._devices: dict[str, DeviceRecord] = {}
        self._lock = threading.Lock()

    def register(self, device_id: str, source: str, name: str | None = None,
                 config: dict[str, Any] | None = None) -> DeviceRecord:
        with self._lock:
            existing = self._devices.get(device_id)
            if existing:
                existing.source = source
                existing.name = name or existing.name
                existing.config = config or existing.config
                return existing

            record = DeviceRecord(
                device_id=device_id,
                source=source,
                name=name,
                config=config or {},
            )
            self._devices[device_id] = record
            logger.info("Device has been registered: %s (%s)", device_id, source)
            return record

    def unregister(self, device_id: str) -> None:
        with self._lock:
            if device_id in self._devices:
                del self._devices[device_id]
                logger.info("Device has been deleted from registry: %s", device_id)

    @classmethod
    def from_config_list(cls, devices: Iterable[dict[str, Any]], **kwargs) -> "DeviceRegistry":
        registry = cls(**kwargs)
        for d in devices:
            registry.register(
                device_id=d["device_id"],
                source=d["source"],
                name=d.get("name"),
                config=d.get("config", {}),
            )
        return registry

    def mark_seen(self, device_id: str, seen_at: datetime | None = None) -> None:
        with self._lock:
            record = self._devices.get(device_id)
            if record is None:
                record = DeviceRecord(device_id=device_id, source="unknown")
                self._devices[device_id] = record
                logger.warning("Event from unknown device: %s", device_id)

            record.last_seen = seen_at or datetime.now(UTC)
            record.status = DeviceStatus.ONLINE
            record.last_error = None

    def mark_error(self, device_id: str, error: str) -> None:
        with self._lock:
            record = self._devices.get(device_id)
            if record:
                record.status = DeviceStatus.ERROR
                record.last_error = error

    def mark_offline(self, device_id: str) -> None:
        with self._lock:
            record = self._devices.get(device_id)
            if record:
                record.status = DeviceStatus.OFFLINE

    def mark_stale_as_offline(self) -> list[str]:
        now = datetime.now(UTC)
        went_offline = []
        with self._lock:
            for record in self._devices.values():
                if record.status != DeviceStatus.ONLINE:
                    continue
                if record.last_seen and (now - record.last_seen) > self._offline_after:
                    record.status = DeviceStatus.OFFLINE
                    went_offline.append(record.device_id)
        for device_id in went_offline:
            logger.info("Device changed mode to offline: %s", device_id)
        return went_offline

    def get(self, device_id: str) -> DeviceRecord | None:
        with self._lock:
            return self._devices.get(device_id)

    def list_all(self, source: str | None = None,
                 status: DeviceStatus | None = None) -> list[DeviceRecord]:
        with self._lock:
            records = list(self._devices.values())
        if source:
            records = [r for r in records if r.source == source]
        if status:
            records = [r for r in records if r.status == status]
        return records
