from fastapi import APIRouter

from skalyx.api.v1 import v1_api_router

api_router = APIRouter(prefix='/api')

api_router.include_router(v1_api_router)
