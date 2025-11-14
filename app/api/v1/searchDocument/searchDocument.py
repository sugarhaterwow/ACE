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

# @router.get("/list", summary="查看投标书列表")
# async def list_tender(
#     keyword: Optional[str] = Query(None, description="关键词搜索"),
#     start_date: Optional[str] = Query(None, description="开始日期 YYYY-MM-DD"),
#     end_date: Optional[str] = Query(None, description="结束日期 YYYY-MM-DD"),
#     status: Optional[str] = Query(None, description="状态过滤"),
#     page: int = Query(1, description="页码"),
#     page_size: int = Query(10, description="每页数量"),
# ):
#     # 初始化查询
#     query = tender_controller.model.all()

#     # 关键词模糊匹配
#     if keyword:
#         query = query.filter(
#             Q(name__icontains=keyword) | Q(description__icontains=keyword)
#         )

#     # 日期范围
#     if start_date and end_date:
#         query = query.filter(Q(analysis__range=(start_date, end_date)))

#     # 状态过滤
#     if status:
#         query = query.filter(Q(status=status))

#     # 分页
#     offset = (page - 1) * page_size
#     results = query.offset(offset).limit(page_size).all()

#     return SuccessExtra(data=res_menu, total=len(res_menu), page=page, page_size=page_size)



@router.get("/", summary="搜索相关文档")
async def search(
    query: Optional[str] = Query(None, description="关键字"),
):
    if not query:
        return Success(msg="Input cannot be empty", data=[])
    
    # Simulated checklist data
    results = [{"id": 1, "item": "Sample Document"}]

    if not results:
        return Success(msg=f"No records found containing '{query}'", data=[])

    return Success(msg="Loaded successfully", data=results)

    




    
        
    