from django.apps import AppConfig
import os
from pathlib import Path

# 获取项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent


class StatsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "stats"
    verbose_name = "统计分析"
    path = str(BASE_DIR / "stats")
