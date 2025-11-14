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

@router.get("/{page}")
async def get_page_data(page: str):
    file_path = os.path.join(settings.MOCKDATA_ROOT, f"{page}.json")
    if not os.path.exists(file_path):
        logger.warning("Config file not found: %s", file_path)
        raise HTTPException(status_code=404, detail=f"Configuration file {page}.json not found.")
    
    with open(file_path, "r", encoding="utf-8") as f:
        config_data = json.load(f)  # 读取 JSON 文件内容
    
    return Success(msg="Loaded Successfully", data=config_data)


    
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

    




    
        
    