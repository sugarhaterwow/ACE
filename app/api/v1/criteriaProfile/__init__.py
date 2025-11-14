from fastapi import APIRouter

from .criteriaProfile import router

criteriaProfile_router = APIRouter()
criteriaProfile_router.include_router(router, tags=["标准概述模块"])

__all__ = ["criteriaProfile_router"]
