"""
HowToCook MCP 服务器
一个菜谱助手 MCP 服务器，提供烹饪推荐和膳食计划功能
"""

from .core import app, create_app, get_config

__version__ = "0.2.0"
__all__ = ["app", "create_app", "get_config"]
