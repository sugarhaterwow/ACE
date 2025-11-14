from fastapi import APIRouter

from .tenderReview import router

tenderReview_router = APIRouter()
tenderReview_router.include_router(router, tags=["投标书模块"])

__all__ = ["tenderReview_router"]
