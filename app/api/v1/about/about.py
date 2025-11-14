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



@router.get("/", summary="Get About Page Analysis Result")
async def get_page_config():
    file_path = os.path.join(settings.MOCKDATA_ROOT, "about.json")
    if not os.path.exists(file_path):
        logger.warning("Config file not found: %s", file_path)
        raise HTTPException(status_code=404, detail=f"Configuration file about.json not found.")
    
    with open(file_path, "r", encoding="utf-8") as f:
        config_data = json.load(f)  # 读取 JSON 文件内容
    
    return Success(msg="Data loaded Successfully", data=config_data)
    




    
        
    