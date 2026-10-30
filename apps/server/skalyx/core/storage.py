import asyncio
import json
import logging

import aiosqlite

logger = logging.getLogger("core.storage")


class Storage:
    def __init__(self, bus, db_path="storage.sqlite3") -> None:
        self.__subscription = bus.subscribe()
        self.__db_path = db_path
        self.__connection: aiosqlite.Connection | None = None
        self.__is_running = False

    @property
    def connection(self):
        return self.__connection

    async def __listener_task(self):
        while self.__is_running:
            event = await self.__subscription.get()

            if not self.__connection:
                logger.warning("Database connection is closing. Aborting.")
                return

            await self.__connection.execute(
                """
                    INSERT INTO records (
                        device_id,
                        source,
                        metric,
                        value,
                        unit,
                        timestamp,
                        meta,
                        value_type
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    event.device_id,
                    event.source,
                    event.metric,
                    str(event.value),
                    event.unit,
                    event.timestamp,
                    json.dumps(event.meta),
                    type(event.value).__name__
                ),
            )
            await self.__connection.commit()

    async def start(self):
        self.__connection = await aiosqlite.connect(self.__db_path)

        await self.__connection.executescript(
            """
                CREATE TABLE IF NOT EXISTS records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_id TEXT,
                    source TEXT,
                    metric TEXT,
                    value TEXT,
                    unit TEXT,
                    timestamp TEXT,
                    meta TEXT,
                    value_type TEXT
                );
            """
        )

        self.__is_running = True
        asyncio.create_task(self.__listener_task())

    async def stop(self):
        if self.__connection:
            await self.__connection.close()

        self.__is_running = False
