import asyncio
import logging

from skalyx.schemas.event import Event

logger = logging.getLogger('core.bus')


class EventBus:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, max_queue_size=1024) -> None:
        if hasattr(self, '_EventBus__initialized'):
            return

        self.__queue = asyncio.Queue[Event](maxsize=max_queue_size)
        self.__subscribers: list[asyncio.Queue[Event]] = []
        self.__is_running = False
        self.__initialized = True

    async def publish(self, event: Event):
        await self.__queue.put(event)

    async def publish_nowait(self, event: Event):
        try:
            self.__queue.put_nowait(event)
        except asyncio.QueueFull:
            logger.warning('Bus queue is overflowed, event dropped; %s', event.model_dump_json())

    def subscribe(self, max_queue_size=1024) -> asyncio.Queue[Event]:
        queue = asyncio.Queue[Event](maxsize=max_queue_size)
        self.__subscribers.append(queue)
        logger.debug(
            'Added new subscriber to event bus, all subscribers: %s',
            len(self.__subscribers)
        )

        return queue

    def unsubscribe(self, queue: asyncio.Queue) -> None:
        if queue in self.__subscribers:
            self.__subscribers.remove(queue)
            logger.debug("Removed subscriber, left: %d", len(self.__subscribers))

    async def run(self) -> None:
        self.__is_running = True
        logger.info("Event bus is running")
        while self.__is_running:
            event = await self.__queue.get()
            self._dispatch(event)

    def _dispatch(self, event: Event) -> None:
        for queue in list(self.__subscribers):
            try:
                queue.put_nowait(event)
            except asyncio.QueueFull:
                logger.warning(
                    "Subscriber's queue is overflowed, event to him has been dropped (device_id=%s, metric=%s)",
                    event.device_id, event.metric,
                )

    def stop(self) -> None:
        self.__is_running = False


    def get_status(self):
        return self.__is_running
