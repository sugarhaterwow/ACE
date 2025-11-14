from fastapi import APIRouter

from .configs import router

configs_router = APIRouter()
configs_router.include_router(router, tags=["配置模块"])

__all__ = ["configs_router"]

