from fastapi import APIRouter

from .clauseRecommender import router

clauseRecommender_router = APIRouter()
clauseRecommender_router.include_router(router, tags=["条款推荐模块"])

__all__ = ["clauseRecommender_router"]
