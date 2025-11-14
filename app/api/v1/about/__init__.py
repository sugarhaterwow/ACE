from fastapi import APIRouter

from .about import router

about_router = APIRouter()
about_router.include_router(router, tags=["汇总模块"])

__all__ = ["about_router"]
