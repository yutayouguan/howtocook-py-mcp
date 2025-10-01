"""
膳食计划业务服务
"""

import json
import random
from typing import List, Optional
from ..models import Recipe, MealPlan, DayPlan
from ..repositories import RecipeRepository
from ...infrastructure.monitoring.performance_monitor import performance_tracked
from ...shared.utils import simplify_recipe
from ...core.config import get_config


class MealService:
    """膳食计划业务服务"""

    def __init__(self):
        self.repository = RecipeRepository()
        self.config = get_config()

    @performance_tracked("recommend_meals")
    async def recommend_meals(
        self,
        people_count: int,
        allergies: Optional[List[str]] = None,
        avoid_items: Optional[List[str]] = None,
    ) -> str:
        """
        根据用户的忌口、过敏原、人数智能推荐菜谱，创建一周的膳食计划

        Args:
            people_count: 用餐人数，1-10之间的整数
            allergies: 过敏原列表，如['大蒜', '虾']
            avoid_items: 忌口食材列表，如['葱', '姜']

        Returns:
            一周的膳食计划
        """
        # 验证人数
        if (
            people_count < self.config.recommendation.min_people_count
            or people_count > self.config.recommendation.max_people_count
        ):
            raise ValueError(
                f"用餐人数必须在{self.config.recommendation.min_people_count}-{self.config.recommendation.max_people_count}之间"
            )

        if allergies is None:
            allergies = []
        if avoid_items is None:
            avoid_items = []

        recipes = await self.repository.fetch_all_recipes()
        if not recipes:
            return "未能获取菜谱数据"

        # 过滤掉含有忌口和过敏原的菜谱
        filtered_recipes = self._filter_recipes_by_restrictions(
            recipes, allergies, avoid_items
        )

        # 将菜谱按分类分组
        recipes_by_category = self._group_recipes_by_category(filtered_recipes)

        # 创建每周膳食计划
        meal_plan = MealPlan()

        # 周一至周五
        for i in range(self.config.meal_plan.weekdays):
            day_plan = DayPlan(
                day=["周一", "周二", "周三", "周四", "周五"][i],
                breakfast=[],
                lunch=[],
                dinner=[],
            )

            # 早餐 - 根据人数推荐1-2个早餐菜单
            self._add_breakfast_to_day_plan(day_plan, people_count, recipes_by_category)

            # 午餐和晚餐的菜谱数量，根据人数确定
            meal_count = max(2, (people_count + 2) // 3)

            # 午餐
            self._add_lunch_to_day_plan(day_plan, meal_count, recipes_by_category)

            # 晚餐
            self._add_dinner_to_day_plan(day_plan, meal_count, recipes_by_category)

            meal_plan.weekdays.append(day_plan)

        # 返回JSON字符串
        return json.dumps(meal_plan.model_dump(), ensure_ascii=False, indent=2)

    def _filter_recipes_by_restrictions(
        self, recipes: List[Recipe], allergies: List[str], avoid_items: List[str]
    ) -> List[Recipe]:
        """根据过敏原和忌口食材过滤菜谱"""
        filtered_recipes = []
        for recipe in recipes:
            # 检查是否包含过敏原或忌口食材
            has_restrictions = False
            for ingredient in recipe.ingredients:
                ingredient_name = ingredient.name.lower()
                if any(
                    allergy.lower() in ingredient_name for allergy in allergies
                ) or any(item.lower() in ingredient_name for item in avoid_items):
                    has_restrictions = True
                    break

            if not has_restrictions:
                filtered_recipes.append(recipe)

        return filtered_recipes

    def _group_recipes_by_category(self, recipes: List[Recipe]) -> dict:
        """将菜谱按分类分组"""
        recipes_by_category = {}

        for recipe in recipes:
            if recipe.category in self.config.recommendation.default_categories:
                if recipe.category not in recipes_by_category:
                    recipes_by_category[recipe.category] = []
                recipes_by_category[recipe.category].append(recipe)

        return recipes_by_category

    def _add_breakfast_to_day_plan(
        self, day_plan: DayPlan, people_count: int, recipes_by_category: dict
    ):
        """为日计划添加早餐"""
        breakfast_count = max(1, (people_count + 4) // 5)
        if "早餐" in recipes_by_category and recipes_by_category["早餐"]:
            for _ in range(breakfast_count):
                if not recipes_by_category["早餐"]:
                    break
                breakfast_index = random.randrange(len(recipes_by_category["早餐"]))
                selected_recipe = recipes_by_category["早餐"][breakfast_index]
                day_plan.breakfast.append(simplify_recipe(selected_recipe))
                # 避免重复，从候选列表中移除
                recipes_by_category["早餐"].pop(breakfast_index)

    def _add_lunch_to_day_plan(
        self, day_plan: DayPlan, meal_count: int, recipes_by_category: dict
    ):
        """为日计划添加午餐"""
        for _ in range(meal_count):
            # 随机选择菜系：主食、水产、蔬菜、荤菜等
            categories = ["主食", "水产", "荤菜", "素菜", "甜品"]

            # 随机选择一个分类
            while categories:
                selected_category = random.choice(categories)
                categories.remove(selected_category)

                if (
                    selected_category in recipes_by_category
                    and recipes_by_category[selected_category]
                ):
                    index = random.randrange(
                        len(recipes_by_category[selected_category])
                    )
                    selected_recipe = recipes_by_category[selected_category][index]
                    day_plan.lunch.append(simplify_recipe(selected_recipe))
                    # 避免重复，从候选列表中移除
                    recipes_by_category[selected_category].pop(index)
                    break

    def _add_dinner_to_day_plan(
        self, day_plan: DayPlan, meal_count: int, recipes_by_category: dict
    ):
        """为日计划添加晚餐"""
        for _ in range(meal_count):
            # 随机选择菜系，与午餐类似但可添加汤羹
            categories = ["主食", "水产", "荤菜", "素菜", "甜品", "汤羹"]

            # 随机选择一个分类
            while categories:
                selected_category = random.choice(categories)
                categories.remove(selected_category)

                if (
                    selected_category in recipes_by_category
                    and recipes_by_category[selected_category]
                ):
                    index = random.randrange(
                        len(recipes_by_category[selected_category])
                    )
                    selected_recipe = recipes_by_category[selected_category][index]
                    day_plan.dinner.append(simplify_recipe(selected_recipe))
                    # 避免重复，从候选列表中移除
                    recipes_by_category[selected_category].pop(index)
                    break
