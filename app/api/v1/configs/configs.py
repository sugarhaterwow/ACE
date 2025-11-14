import logging
import os, json
from app.settings.config import settings
from fastapi import APIRouter, HTTPException
from app.schemas.base import Success, Fail

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/{page}")
async def get_page_config(page: str):
    file_path = os.path.join(settings.CONFIGS_ROOT, f"{page}.json")
    if not os.path.exists(file_path):
        logger.warning("Config file not found: %s", file_path)
        raise HTTPException(status_code=404, detail=f"Configuration file {page}.json not found.")
    
    with open(file_path, "r", encoding="utf-8") as f:
        config_data = json.load(f)  # 读取 JSON 文件内容
    
    return Success(msg="Loaded Successfully", data=config_data)



