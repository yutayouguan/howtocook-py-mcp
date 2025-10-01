"""
膳食计划相关的数据模型
"""

from pydantic import BaseModel
from typing import List
from .recipe import SimpleRecipe


class DayPlan(BaseModel):
    """单日膳食计划模型"""

    day: str
    breakfast: List[SimpleRecipe]
    lunch: List[SimpleRecipe]
    dinner: List[SimpleRecipe]


class MealPlan(BaseModel):
    """完整膳食计划模型"""

    weekdays: List[DayPlan] = []
    weekend: List[DayPlan] = []
