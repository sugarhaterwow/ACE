import logging

from fastapi import APIRouter, Query, HTTPException, UploadFile, File, Form, Request, Path
from app.core.dependency import DependAuth
from app.models import User
from typing import List
from typing import Optional
from tortoise.expressions import Q
# from app.controllers.tender import tender_controller 
from app.schemas.base import Success, Fail, SuccessExtra
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


# @router.post("/upload", summary="Upload tender documents")
# async def upload_tender(
#     files: List[UploadFile] = File(...),
#     current_user: User = DependAuth
# ):
#     # Create user-specific directory
#     user_dir = os.path.join(settings.UPLOAD_ROOT, str(current_user.id))
#     os.makedirs(user_dir, exist_ok=True)

#     saved_files = []
#     for file in files:
#         if not file.filename.endswith((".pdf", ".doc", ".docx")):
#             raise HTTPException(status_code=400, detail="Only PDF/DOC/DOCX files are allowed")

#         save_path = os.path.join(user_dir, file.filename)
#         try:
#             content = await file.read()
#             with open(save_path, "wb") as f:
#                 f.write(content)
#             saved_files.append({"filename": file.filename, "path": save_path})
#         except Exception as e:
#             logger.error("File save failed: %s", e)
#             raise HTTPException(status_code=500, detail="File save failed")

#     return {
#         "msg": "Files uploaded successfully",
#         "user_id": current_user.id,
#         "files": saved_files
#     }


@router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...), folder: str = Form("Default")):
    folder_path = Path(settings.UPLOAD_ROOT) / folder
    folder_path.mkdir(parents=True, exist_ok=True)

    uploaded_names = []

    for file in files:
        filename = Path(file.filename).name
        file_path = folder_path / filename
        with open(file_path, "wb") as f:
            while content := await file.read(1024*1024):
                f.write(content)
        uploaded_names.append(filename)

    return {"success": True, "uploaded": uploaded_names}


@router.post("/delete")
async def delete_file(filename: str = Form(...), folder: str = Form("Default")):
    try:
        file_path = os.path.join(settings.UPLOAD_ROOT, filename)

        if os.path.exists(file_path):
            os.remove(file_path)
            return Success(msg=f"{filename} deleted.")
        else:
            return Success(msg="File not found.", status_code=404)
    except Exception as e:
        return Success(msg="File deletion failed.", data={"error": str(e)})


@router.get("/analysis-checklist", summary="查看投标书列表")
async def list_tender(
    values: List[str] = Query(...),
    page: int = Query(1, gt=0, description="页码"),
    page_size: int = Query(0, ge=0, description="每页数量，0 表示返回全部")
):
    if not values:
        return Fail(code=400, msg="values parameter cannot be empty", data=[])
    
    
    filename = f"{''.join(values[-1].lower().split())}.json"
    file_path = os.path.join(settings.CHECKLIST_ROOT, filename)

    if not os.path.exists(file_path):
        logger.warning("Config file not found: %s", file_path)
        return Fail(code=404, msg=f"Configuration file {filename} not found.", data=[])

    with open(file_path, "r", encoding="utf-8") as f:
        checklist_data = json.load(f)
    print(checklist_data)
    total = len(checklist_data)

    # 如果 page_size=0 → 返回全部
    if page_size == 0:
        return SuccessExtra(msg="Loaded Successfully", data=checklist_data, total=total, page=1, page_size=total)

    # 否则分页
    start = (page - 1) * page_size
    end = start + page_size
    paged_data = checklist_data[start:end]

    return SuccessExtra(msg="Loaded Successfully", data=paged_data, total=total, page=page, page_size=page_size)


@router.post("/submit-analysis", summary="提交投标书配置")
async def submit_analysis(payload: dict):
    # 遍历 payload 的每个 key:value
    for key, value in payload.items():
        if value in (None, "", []):
            return Fail(
                code=400,
                msg=f"Field '{key}' cannot be empty",
                data=payload
            )

    # 如果所有字段都不为空，直接返回成功
    return Success(code=200, msg="Submitted successfully", data=payload)