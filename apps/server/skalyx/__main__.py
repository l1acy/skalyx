import asyncio
from argparse import ArgumentParser
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from skalyx import ble_adapter, bus, storage
from skalyx.api.api import api_router
from skalyx.api.frontend import frontend_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await ble_adapter.start()
    await storage.start()
    bus_task = asyncio.create_task(bus.run())
    yield
    await ble_adapter.stop()
    await storage.stop()
    bus.stop()
    bus_task.cancel()

app = FastAPI(lifespan=lifespan)
app.add_middleware(GZipMiddleware, minimum_size=512)
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['*'], allow_methods=['*'])

app.include_router(api_router)
app.include_router(frontend_router)



if __name__ == "__main__":
    parser = ArgumentParser(
        prog='Skalyx Core',
        description='Skalyx core'
    )
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', default=1823, type=int)
    args = parser.parse_args()

    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        timeout_graceful_shutdown=5
    )
