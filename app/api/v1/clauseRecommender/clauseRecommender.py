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
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter()

class UpdateRequest(BaseModel):
    id: int
    active: bool



@router.get("/", summary="根据输入推荐相关条款")
async def recommend(
    query: Optional[str] = Query(None, description="关键字"),
):
    if not query:
        return Success(msg="Input cannot be empty", data=[])
    
    file_path = os.path.join(settings.MOCKDATA_ROOT, "clause-recommender.json")
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            results = json.load(f)
    except Exception as e:
        return Success(msg="Failed to load mock data", data=[])
    
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



    

@router.put("/update", summary="修改条款的 active 状态")
async def update_recommendation(req: UpdateRequest):
    file_path = os.path.join(settings.MOCKDATA_ROOT, "clause-recommender.json")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to load mock data")

    updated_row = None
    for row in data:
        if row.get("id") == req.id:
            row["action"] = req.active   # 修改 JSON 中的 action 字段
            updated_row = row
            break

    if not updated_row:
        raise HTTPException(status_code=404, detail=f"Record with id {req.id} not found")

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to save mock data")

    return Success(msg="Updated successfully", data=updated_row)



    
        
    