import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from skalyx import bus

websocket_router = APIRouter()


@websocket_router.websocket('/gateway')
async def ws_gateway(websocket: WebSocket):
    await websocket.accept()
    subscription = bus.subscribe()

    async def forward_events():
        while True:
            event = await subscription.get()
            await websocket.send_json(event.model_dump())

    async def watch_disconnect():
        while True:
            await websocket.receive_text()

    forward_task = asyncio.create_task(forward_events())
    watch_task = asyncio.create_task(watch_disconnect())

    try:
        done, pending = await asyncio.wait(
            {forward_task, watch_task},
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()
        for task in done:
            task.result()
    except WebSocketDisconnect:
        pass
    finally:
        bus.unsubscribe(subscription)
        forward_task.cancel()
        watch_task.cancel()