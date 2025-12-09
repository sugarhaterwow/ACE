import logging

from fastapi import APIRouter, Query, UploadFile, File, Form, Body
from app.core.dependency import DependAuth
from typing import List, Optional, Dict
from tortoise.expressions import Q
# from app.controllers.tender import tender_controller 
from app.schemas.base import Success, Fail, SuccessExtra
from app.schemas.menus import *
import os, json, shutil
from app.settings.config import settings
from pydantic import BaseModel
from pathlib import Path

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


# 定义请求体数据模型
class ProjectCreateRequest(BaseModel):
    job_name: str


# 定义接收到的请求数据结构
class ChecklistItem(BaseModel):
    id: int
    item: str
    search_entities: list
    removed_entities: list
    analysis_type: str
    selected: bool

class ConfigUpdateRequest(BaseModel):
    Analysis_Checklist: Dict[str, list]
    Variable_Criteria: Dict[str, str]
    Exemption_Lists: Dict[str, str]

@router.post("/job")
def create_job(request: ProjectCreateRequest):
    
    job_name = request.job_name  # 获取请求体中的 job_name
    print("upload:", job_name)
    job_path = Path(settings.UPLOAD_ROOT) / job_name
    # 检查是否存在
    if os.path.exists(job_path):
        return Fail(code=409, msg="Project already exists!")
    try:
        os.makedirs(job_path)
        

        return Success(code=200, msg="Project created successfully!", data={"name": job_name})
    except Exception as e:
        return Fail(code=500, msg=f"Failed to create project: {str(e)}")


@router.delete("/job/{job_name}")
def delete_job(job_name: str):

    job_path = Path(settings.UPLOAD_ROOT) / job_name

    if not os.path.exists(job_path):
        return Fail(code=404, msg="Project not found")

    try:
        shutil.rmtree(job_path)
        return Success(code=204, msg="Job deleted")
    except Exception as e:
        return Fail(code=500, msg=f"Failed to delete project: {str(e)}")



@router.post("/upload")
async def upload_files(
    folder: str = Form(...),
    files: List[UploadFile] = File(...)
):
    print("收到的 folder:", folder)

    for f in files:
        print("文件名:", f.filename)
        print("文件类型:", f.content_type)
        content = await f.read()
        print("文件大小:", len(content), "字节")
    folder_path = Path(settings.UPLOAD_ROOT) / folder
    os.makedirs(folder_path, exist_ok=True)

    success_files = []
    failed_files = []

    for file in files:
        try:
            file_path = folder_path / file.filename
            with open(file_path, "wb") as f:
                f.write(await file.read())
            success_files.append(file.filename)
        except Exception as e:
            failed_files.append({"filename": file.filename, "error": str(e)})

    # 返回成功和失败的详细情况
    if failed_files:
        return Success(
            code=200,  # 207 Multi-Status 表示部分成功
            msg="Some files failed to upload!",
            data={"success": success_files, "failed": failed_files}
        )
    else:
        return Success(
            code=200,
            msg="All files uploaded successfully!",
            data={"success": success_files, "failed": failed_files}
        )

@router.delete("/{folder}/{filename}")
def delete_file(folder: str, filename: str):
    file_path = Path(settings.UPLOAD_ROOT) / folder / filename
    if not os.path.exists(file_path):
        return Fail(code=404, msg="File not found!")
    try:
        os.remove(file_path)
        return Success(code=200, msg=f"File {filename} deleted successfully!", data={"folder": folder, "filename": filename})
    except Exception as e:
        return Fail(code=500, msg=f"Failed to delete file: {str(e)}")


@router.get("/analysis-checklist", summary="查看投标书列表")
async def list_tender(
    values: List[str] = Query(...),
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
    print("total:", total)
    return Success(code=200, msg="Loaded Successfully", data=checklist_data)

@router.put("/update-config", summary="提交投标书配")
async def update_config(config_update: dict = Body(...)):
    print("Received config update:", config_update)
     # 直接访问整个请求体数据
    Analysis_Checklist = config_update.get("Analysis Checklist")
    Variable_Criteria = config_update.get("Variable Criteria")
    Exemption_Lists = config_update.get("Exemption Lists")
    
    for checklist_key, checklist_value in Analysis_Checklist.items():
        if checklist_key and len(checklist_value) > 0:
            parsedValues = checklist_key.split('::')
            filename = f"{''.join(parsedValues[-1].lower().split())}.json"
            file_path = os.path.join(settings.CHECKLIST_ROOT, filename)
            
             # 读取原有的 JSON 数据
            with open(file_path, "r", encoding="utf-8") as f:
                original_data = json.load(f)
            
            # 更新 checklist_value 中的数据
            for item in checklist_value:
                item_id = item.get("id")

                # 找到原 JSON 中对应 id 的项
                original_item = next((x for x in original_data if x.get("id") == item_id), None)

                if original_item:
                    # 如果 selected 为 False，不覆盖原有数据，但将 selected 修改为 False
                    if item.get("selected") is False:
                        original_item["selected"] = False
                    else:
                        # 如果 selected 为 True，则完全覆盖原数据
                        original_item.update(item)

    for criteria_key, criteria_value in Variable_Criteria.items():
        file_path = os.path.join(settings.CONFIGS_ROOT, "review-profile.json")

        # 读取配置文件
        with open(file_path, "r", encoding="utf-8") as f:
            review_profile = json.load(f)

        step = next((s for s in review_profile.get("steps", []) if s["title"] == "Variable Criteria"), None)
        print("step:", step)
        
        # 遍历 review_profile 的 steps，找到对应的 title
        for module in step.get("modules", []):
            print("Module Title:", module["title"], "Criteria Key:", criteria_key)
            
            # 找到对应的步骤和模块 
            for comp in module.get("components", []):
                
                # 找到对应的步骤和模块
                if comp["label"] == criteria_key:  # 如果 label 匹配
                    # 更新 value
                    print("Updating", criteria_value, comp)
                    comp["value"] = criteria_value
        
        # 保存更新后的配置文件
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(review_profile, f, ensure_ascii=False, indent=4)

    for exemption_key, exemption_value in Exemption_Lists.items():
        # 获取配置文件路径
        file_path = os.path.join(settings.CONFIGS_ROOT, "review-profile.json")

        # 读取配置文件
        with open(file_path, "r", encoding="utf-8") as f:
            review_profile = json.load(f)

        step = next((s for s in review_profile.get("steps", []) if s["title"] == "Exemption Lists"), None)
        
        # 遍历 review_profile 的 steps，找到对应的 title
        for module in step.get("modules", []):

                # 找到对应的步骤和模块 
            for comp in module.get("components", []):
                
                # 找到对应的步骤和模块
                if comp["label"] == exemption_key:  # 如果 label 匹配
                    # 更新 value
                    print("Updating", exemption_value, comp)
                    comp["value"] = exemption_value

        # 保存更新后的配置文件
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(review_profile, f, ensure_ascii=False, indent=4)

    # 如果所有字段都不为空，直接返回成功
    return Success(code=200, msg="Submitted successfully", data=config_update)

@router.put("/submit-config", summary="提交投标书配")
async def submit_config(config_update: dict = Body(...)):
    # 检查所有字段是否都不为空
    # if not config_update.get("Analysis_Checklist") or not config_update.get("Variable_Criteria") or not config_update.get("Exemption_Lists"):
    #     return Fail(code=400, msg="All configuration sections must be provided and non-empty.", data=None)
    
    # 如果所有字段都不为空，直接返回成功
    return Success(code=200, msg="Submitted successfully", data=config_update)