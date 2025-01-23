from django.apps import AppConfig
import os
from pathlib import Path

# 获取项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent


class BillsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bills"
    verbose_name = "账单管理"
    path = str(BASE_DIR / "bills")
