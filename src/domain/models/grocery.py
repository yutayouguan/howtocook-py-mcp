"""
购物清单相关的数据模型
"""

from pydantic import BaseModel
from typing import List, Optional


class ShoppingPlanCategories(BaseModel):
    """购物计划分类模型"""

    fresh: List[str] = []
    pantry: List[str] = []
    spices: List[str] = []
    others: List[str] = []


class GroceryItem(BaseModel):
    """购物清单项目模型"""

    name: str
    total_quantity: Optional[float] = None
    unit: Optional[str] = None
    recipe_count: int
    recipes: List[str]


class GroceryList(BaseModel):
    """购物清单模型"""

    ingredients: List[GroceryItem] = []
    shopping_plan: ShoppingPlanCategories = ShoppingPlanCategories()
