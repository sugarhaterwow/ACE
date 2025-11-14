from fastapi import APIRouter

from .userManagement import router

userManagement_router = APIRouter()
userManagement_router.include_router(router, tags=["用户管理模块"])

__all__ = ["userManagement_router"]
