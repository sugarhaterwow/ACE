# controllers/tender_controller.py
import os
import json
import shutil
from pathlib import Path
from typing import List
from fastapi import UploadFile
from settings import settings
from utils.responses import Success, Fail
import logging

logger = logging.getLogger(__name__)

class TenderController:
    def __init__(self, job_name: str):
        # 如果有 ORM 模型，可以在这里绑定
        self.job_name = job_name
        self.upload_root = settings.UPLOAD_ROOT
        self.checklist_root = settings.CHECKLIST_ROOT


    async def upload_files(self, folder: str, files: List[UploadFile]):
        """上传文件到指定文件夹"""
        folder_path = Path(self.upload_root) / folder
        os.makedirs(folder_path, exist_ok=True)

        success_files = []
        failed_files = []

        for file in files:
            try:
                file_path = folder_path / file.filename
                content = await file.read()
                with open(file_path, "wb") as f:
                    f.write(content)
                success_files.append(file.filename)
            except Exception as e:
                logger.error("File save failed: %s", e)
                failed_files.append({"filename": file.filename, "error": str(e)})

        if failed_files:
            return Success(
                code=200,
                msg="Some files failed to upload!",
                data={"success": success_files, "failed": failed_files}
            )
        else:
            return Success(
                code=200,
                msg="All files uploaded successfully!",
                data={"success": success_files, "failed": failed_files}
            )

    def delete_file(self, folder: str, filename: str):
        """删除指定文件"""
        file_path = Path(self.upload_root) / folder / filename
        if not os.path.exists(file_path):
            return Fail(code=404, msg="File not found!")
        try:
            os.remove(file_path)
            return Success(code=200, msg=f"File {filename} deleted successfully!",
                           data={"folder": folder, "filename": filename})
        except Exception as e:
            return Fail(code=500, msg=f"Failed to delete file: {str(e)}")


tender_controller = TenderController()
