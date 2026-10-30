from fastapi import APIRouter

from skalyx.api.v1.rest import rest_router
from skalyx.api.v1.websocket import websocket_router

v1_api_router = APIRouter(prefix='/v1')

v1_api_router.include_router(rest_router)
v1_api_router.include_router(websocket_router)
