from fastapi import APIRouter

from .searchDocument import router

searchDocument_router = APIRouter()
searchDocument_router.include_router(router, tags=["查找文件模块"])

__all__ = ["searchDocument_router"]
