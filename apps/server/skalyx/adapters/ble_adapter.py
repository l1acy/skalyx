import asyncio
import logging
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

from skalyx.adapters.parsers.base import Parser
from skalyx.adapters.parsers.bthome2 import BTHomeV2Parser
from skalyx.core.bus import EventBus
from skalyx.core.config import Config, ConfigDevice
from skalyx.schemas.event import Event

logger = logging.getLogger('adapters.ble')
bus = EventBus()

PARSER_MAP = {
    'bthome_v2': BTHomeV2Parser
}
BLE_BASED_PARSERS = {'bthome_v2'}

@dataclass
class BLEAdvertisingDeviceConfig:
    device_id: str
    address: str
    service_data_uuid: str
    parser: Parser

class _Deduper:
    def __init__(self):
        self._last_packet_id: dict[str, int] = {}
        self._last_raw: dict[str, bytes] = {}

    def is_duplicate(self, address: str, raw: bytes, packet_id: int | None) -> bool:
        if packet_id is not None:
            prev = self._last_packet_id.get(address)
            self._last_packet_id[address] = packet_id
            return prev == packet_id

        prev_raw = self._last_raw.get(address)
        self._last_raw[address] = raw
        return prev_raw == raw

def make_event(device_id: str, metric: str, value: Any, unit: str | None) -> Event:
    return Event(
        device_id=device_id,
        source='ble',
        metric=metric,
        value=value,
        unit=unit or '',
        timestamp=datetime.now(UTC).isoformat(),
        meta={}
    )


class BleAdapter:
    def __init__(self) -> None:
        self.__scanner: BleakScanner | None = None
        self.__task: asyncio.Task | None = None
        self.__stop_event: asyncio.Event | None = None
        self.__loop: asyncio.AbstractEventLoop | None = None
        self.__deduper = _Deduper()
        self._devices_by_address = {d.address.upper(): d for d in Config().data.devices}

    async def _handle_raw(self, config: ConfigDevice, raw: bytes) -> None:
        parser = PARSER_MAP.get(config.parser)
        if not parser:
            logger.error("Skalyx didn't support the %s parser", config.parser)
            return

        try:
            metrics = parser.parse(raw)
        except Exception:
            logger.exception("An error occurred while parsing data from %s: %r", config.device_id, raw)
            return

        packet_id = None
        device_metrics = []
        for m in metrics:
            if m.metric == "packet_id":
                packet_id = int(m.value)
            else:
                device_metrics.append(m)

        if self.__deduper.is_duplicate(config.address, raw, packet_id):
            return

        for m in device_metrics:
            event = make_event(config.device_id, m.metric, m.value, m.unit)
            await bus.publish(event)

    def scanner_callback(self, device: BLEDevice, adv_data: AdvertisementData):
        device_config = self._devices_by_address.get(device.address.upper())
        if not device_config:
            return

        if device_config.parser not in BLE_BASED_PARSERS:
            return

        parser_config = device_config.parser_params
        raw = adv_data.service_data.get(parser_config.service_data_uuid)
        if not raw:
            return

        asyncio.create_task(self._handle_raw(device_config, bytes(raw)))

    async def __scan_forever(self):
        self.__scanner = BleakScanner(self.scanner_callback)
        await self.__scanner.start()
        logger.info('Ble adapter listening (background task)')

        try:
            if not self.__stop_event:
                logger.warning('Stop event is none. Aborting')
                return
            else:
                await self.__stop_event.wait()
        finally:
            await self.__scanner.stop()
            logger.info('Ble adapter stopped')

    async def start(self):
        if self.__task and not self.__task.done():
            logger.warning('Ble adapter already running')
            return

        self.__loop = asyncio.get_running_loop()

        self.__stop_event = asyncio.Event()
        self.__task = asyncio.create_task(self.__scan_forever())


    async def stop(self):
        if not self.__task or self.__task.done():
            return

        if self.__stop_event:
            self.__stop_event.set()
        else:
            logger.error('Stop event is none. Stopping forcefully')
            self.__task.cancel()

        try:
            await asyncio.wait_for(self.__task, timeout=3.0)
        except TimeoutError:
            logger.error("Scanner didn't stop in time, cancelling forcefully")
            self.__task.cancel()

            try:
                await self.__task
            except asyncio.CancelledError:
                pass
        finally:
            self.__task = None
            self.__scanner = None

    def get_status(self):
        if not self.__task:
            return False

        return not self.__task.done()
