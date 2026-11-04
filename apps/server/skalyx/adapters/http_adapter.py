import asyncio
import logging
import time
from datetime import UTC, datetime
from typing import Any

import aiohttp

from skalyx.adapters.parsers.openweathermap import OpenWeatherMapParser
from skalyx.core.bus import EventBus
from skalyx.core.config import Config, ConfigDevice
from skalyx.schemas.event import Event

logger = logging.getLogger('adapters.http')
bus = EventBus()

PARSER_MAP = {
    'openweathermap': OpenWeatherMapParser
}
HTTP_BASED_PARSERS = {'openweathermap'}


def make_event(device_id: str, metric: str, value: Any, unit: str | None) -> Event:
    return Event(
        device_id=device_id,
        source='http',
        metric=metric,
        value=value,
        unit=unit or '',
        timestamp=datetime.now(UTC).isoformat(),
        meta={}
    )


class HTTPAdapter:
    def __init__(self) -> None:
        self.__devices = Config().data.devices
        self.__task: asyncio.Task | None = None
        self.__stop_event = asyncio.Event()
        self.__loop: asyncio.AbstractEventLoop | None = None
        self.__running: bool = False
        self.__http_session: aiohttp.ClientSession | None = None
        self.__devices_ask_time: dict[str, float] = {i.device_id: 0 for i in self.__devices}

    async def __poll_once(self, client: aiohttp.ClientSession, device: ConfigDevice):
        if not isinstance(device.parser_params, dict):
            logger.error(
                "Invalid HTTP device configuration for %s: "
                "`parser_params` must be a dictionary", device.device_id,
            )
            return
        if device.parser not in HTTP_BASED_PARSERS:
            logger.error('HTTP device %s does not support parser %s', device.device_id, device.parser)
            return

        self.__devices_ask_time[device.device_id] = time.monotonic()

        try:
            async with client.get(
                url=device.address.format(**device.parser_params),
                timeout=aiohttp.ClientTimeout(total=device.ask_interval or 60)
            ) as response:
                response.raise_for_status()
                body = await response.text()
                parser = PARSER_MAP[device.parser]
                metrics = parser.parse(body)

                for m in metrics:
                    await bus.publish(make_event(device_id=device.device_id, metric=m.metric, unit=m.unit, value=m.value))

                logger.info('%s http device asked with %d status code', device.device_id, response.status)

        except AssertionError:
            logger.error('Invalid HTTP device configuration: `parser_params` must be a dictionary')
        except aiohttp.ClientResponseError as exception:
            logger.warning('%s responded with HTTP error: %s', device.device_id, exception)
        except (aiohttp.ClientError, TimeoutError) as exception:
            logger.warning('%s poll failed: %s', device.device_id, exception)
        except Exception:
            logger.exception('Unexpected error while polling %s', device.device_id)

    async def __device_poll_task(self, device: ConfigDevice) -> None:
        assert self.__http_session

        while self.__running:
            await self.__poll_once(self.__http_session, device)

            if not self.__running:
                break

            try:
                await asyncio.wait_for(self.__stop_event.wait(), timeout=device.ask_interval)
            except TimeoutError:
                pass

    async def start(self) -> None:
        if self.__running:
            logger.warning("HTTPAdapter.start() called while already running, ignoring")
            return

        self.__loop = asyncio.get_running_loop()

        self.__running = True
        self.__stop_event.clear()
        self.__http_session = aiohttp.ClientSession()

        self.__tasks = [
            asyncio.create_task(
                self.__device_poll_task(device), name=f"poll-{device.device_id}"
            )
            for device in self.__devices
        ]


    async def stop(self) -> None:
        self.__running = False
        self.__stop_event.set()

        for t in self.__tasks:
            t.cancel()
        await asyncio.gather(*self.__tasks, return_exceptions=True)

        if self.__http_session and not self.__http_session.closed:
            await self.__http_session.close()
            self.__http_session = None
