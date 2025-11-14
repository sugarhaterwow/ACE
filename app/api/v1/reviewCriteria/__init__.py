from fastapi import APIRouter

from .reviewCriteria import router

reviewCriteria_router = APIRouter()
reviewCriteria_router.include_router(router, tags=["审查标准模块"])

__all__ = ["reviewCriteria_router"]
