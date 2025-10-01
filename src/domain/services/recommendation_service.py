"""
推荐业务服务
"""

import json
import random
from typing import List, Optional
from ..models import Recipe, DishRecommendation
from ..repositories import RecipeRepository
from ...infrastructure.monitoring.performance_monitor import performance_tracked
from ...shared.utils import simplify_recipe
from ...core.config import get_config


class RecommendationService:
    """推荐业务服务"""

    def __init__(self):
        self.repository = RecipeRepository()
        self.config = get_config()

    @performance_tracked("what_to_eat")
    async def what_to_eat(self, people_count: int) -> str:
        """
        不知道吃什么？根据人数直接推荐适合的菜品组合

        Args:
            people_count: 用餐人数，1-10之间的整数

        Returns:
            推荐的菜品组合，包含荤菜和素菜
        """
        # 验证人数
        if (
            people_count < self.config.recommendation.min_people_count
            or people_count > self.config.recommendation.max_people_count
        ):
            raise ValueError(
                f"用餐人数必须在{self.config.recommendation.min_people_count}-{self.config.recommendation.max_people_count}之间"
            )

        recipes = await self.repository.fetch_all_recipes()
        if not recipes:
            return "未能获取菜谱数据"

        # 根据人数计算荤素菜数量
        vegetable_count = (people_count + 1) // 2
        meat_count = (people_count + 1) // 2 + (people_count + 1) % 2

        # 获取所有荤菜
        meat_dishes = [
            recipe
            for recipe in recipes
            if recipe.category == "荤菜" or recipe.category == "水产"
        ]

        # 获取其他可能的菜品（当做素菜）
        vegetable_dishes = [
            recipe
            for recipe in recipes
            if recipe.category not in ["荤菜", "水产", "早餐", "主食"]
        ]

        # 特别处理：如果人数超过阈值，增加鱼类荤菜
        recommended_dishes = []
        fish_dish = None

        if people_count > self.config.recommendation.fish_threshold_people:
            fish_dishes = [recipe for recipe in recipes if recipe.category == "水产"]
            if fish_dishes:
                fish_dish = random.choice(fish_dishes)
                recommended_dishes.append(fish_dish)

        # 按照不同肉类的优先级选择荤菜
        selected_meat_dishes = []

        # 需要选择的荤菜数量
        remaining_meat_count = meat_count - (1 if fish_dish else 0)

        # 尝试按照肉类优先级选择荤菜
        for meat_type in self.config.recommendation.meat_types_priority:
            if len(selected_meat_dishes) >= remaining_meat_count:
                break

            meat_type_options = [
                dish
                for dish in meat_dishes
                if any(
                    meat_type.lower() in (ingredient.name or "").lower()
                    for ingredient in dish.ingredients
                )
            ]

            if meat_type_options:
                # 随机选择一道这种肉类的菜
                selected = random.choice(meat_type_options)
                selected_meat_dishes.append(selected)
                # 从可选列表中移除，避免重复选择
                meat_dishes = [dish for dish in meat_dishes if dish.id != selected.id]

        # 如果通过肉类筛选的荤菜不够，随机选择剩余的
        while len(selected_meat_dishes) < remaining_meat_count and meat_dishes:
            random_dish = random.choice(meat_dishes)
            selected_meat_dishes.append(random_dish)
            meat_dishes.remove(random_dish)

        # 随机选择素菜
        selected_vegetable_dishes = []
        while len(selected_vegetable_dishes) < vegetable_count and vegetable_dishes:
            random_dish = random.choice(vegetable_dishes)
            selected_vegetable_dishes.append(random_dish)
            vegetable_dishes.remove(random_dish)

        # 合并推荐菜单
        recommended_dishes.extend(selected_meat_dishes)
        recommended_dishes.extend(selected_vegetable_dishes)

        # 构建推荐结果
        dish_recommendation = DishRecommendation(
            people_count=people_count,
            meat_dish_count=len(selected_meat_dishes) + (1 if fish_dish else 0),
            vegetable_dish_count=len(selected_vegetable_dishes),
            dishes=[simplify_recipe(dish) for dish in recommended_dishes],
            message=f"为{people_count}人推荐的菜品，包含{len(selected_meat_dishes) + (1 if fish_dish else 0)}个荤菜和{len(selected_vegetable_dishes)}个素菜。",
        )

        # 返回JSON字符串
        return json.dumps(
            dish_recommendation.model_dump(), ensure_ascii=False, indent=2
        )
