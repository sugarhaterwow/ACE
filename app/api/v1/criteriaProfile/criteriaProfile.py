import logging

from fastapi import APIRouter, Query, HTTPException, UploadFile, File, Depends
from app.core.dependency import DependAuth
from app.models import User
from typing import List
from typing import Optional
from tortoise.expressions import Q
# from app.controllers.tender import tender_controller 
from app.schemas.base import Success, Fail
from app.schemas.menus import *
import os, json
from app.settings.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/", summary="查看审查标准")
async def list(
    query: Optional[str] = Query(None, description="关键字"),
):
    print(query)
    if not query:
        return Success(msg="Checklist cannot be empty", data=[])
    
    file_path = os.path.join(settings.CRITERIAPROFILE_ROOT, "hongkong.json")
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            results = json.load(f)
    except Exception as e:
        return Success(msg="Failed to load mock data", data=[])
    print(results)
    
    # query_lower = query.lower()
    # results = [
    #     value for value in mockdata.values()
    #     if query_lower in value.get("item", "").lower()
    #     or query_lower in value.get("search_entities", "").lower()
    #     or query_lower in value.get("analysis_type", "").lower()
    # ]

    # if not results:
    #     return Success(msg=f"No records found containing '{query}'", data=[])

    if not results:
        return Success(msg=f"No records found containing '{query}'", data=[])

    return Success(msg="Loaded successfully", data=results)

    




@router.post("/")
async def update_variable_criteria(a: str, b: str, c: str, d: str):
    """更新 Variable Criteria 配置"""
    try:
        
        return Success(msg="Get", data=[])
    except Exception as e:
        return Success(msg="Failed to load mock data", data=[])





        
    