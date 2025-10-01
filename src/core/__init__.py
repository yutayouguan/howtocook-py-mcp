"""
核心模块 - 包含应用程序的核心配置和入口点
"""

from .config import get_config, AppConfig
from .app import app, create_app

__all__ = ["get_config", "AppConfig", "app", "create_app"]
