"""
MCP模块 - 包含工具，资源,提示词注册
"""

from .tools import (
    register_recipe_tools,
    register_meal_tools,
    register_recommendation_tools,
)
from .resources import register_api_resources
from .prompts import meal_planning, meal_planning_prompt, recipe_recommendation_prompt

__all__ = [
    "register_recipe_tools",
    "register_meal_tools",
    "register_recommendation_tools",
    "register_api_resources",
    "meal_planning",
    "meal_planning_prompt",
    "recipe_recommendation_prompt",
]
