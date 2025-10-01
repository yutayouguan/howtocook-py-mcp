"""
MCP工具模块
"""

from .recipe_tools import register_recipe_tools
from .meal_tools import register_meal_tools
from .recommendation_tools import register_recommendation_tools

__all__ = [
    "register_recipe_tools",
    "register_meal_tools",
    "register_recommendation_tools",
]
