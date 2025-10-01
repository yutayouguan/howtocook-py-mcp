"""
菜谱相关的数据模型
"""

from pydantic import BaseModel
from typing import List, Optional, Dict


class Ingredient(BaseModel):
    """食材模型"""

    name: str
    quantity: Optional[float] = None
    unit: Optional[str] = None
    text_quantity: str
    notes: Optional[str] = ""


class Step(BaseModel):
    """制作步骤模型"""

    step: int
    description: str


class Recipe(BaseModel):
    """完整菜谱模型"""

    id: str
    name: str
    description: str
    source_path: str
    image_path: Optional[str] = None
    category: str
    difficulty: int
    tags: List[str]
    servings: int
    ingredients: List[Ingredient]
    steps: List[Step]
    prep_time_minutes: Optional[int] = None
    cook_time_minutes: Optional[int] = None
    total_time_minutes: Optional[int] = None
    additional_notes: List[str] = []


class SimpleRecipe(BaseModel):
    """简化菜谱模型 - 包含基本信息和食材"""

    id: str
    name: str
    description: str
    ingredients: List[Dict[str, str]]


class NameOnlyRecipe(BaseModel):
    """最简菜谱模型 - 仅包含名称和描述"""

    name: str
    description: str


class DishRecommendation(BaseModel):
    """菜品推荐结果模型"""

    people_count: int
    meat_dish_count: int
    vegetable_dish_count: int
    dishes: List[SimpleRecipe]
    message: str
