"""
菜谱业务服务
"""

import json
from typing import List, Optional
from ..models import Recipe, SimpleRecipe, NameOnlyRecipe
from ..repositories import RecipeRepository
from ...infrastructure.monitoring.performance_monitor import performance_tracked
from ...shared.utils import simplify_recipe, simplify_recipe_name_only


class RecipeService:
    """菜谱业务服务"""

    def __init__(self):
        self.repository = RecipeRepository()

    @performance_tracked("get_all_recipes")
    async def get_all_recipes(self) -> str:
        """
        获取所有菜谱

        Returns:
            所有菜谱的简化信息，只包含名称和描述
        """
        recipes = await self.repository.fetch_all_recipes()
        if not recipes:
            return "未能获取菜谱数据"

        # 返回更简化版的菜谱数据，只包含name和description
        simplified_recipes = [simplify_recipe_name_only(recipe) for recipe in recipes]

        # 返回JSON字符串
        return json.dumps(
            [recipe.model_dump() for recipe in simplified_recipes],
            ensure_ascii=False,
            indent=2,
        )

    @performance_tracked("get_recipes_by_category")
    async def get_recipes_by_category(self, category: str) -> str:
        """
        根据分类获取菜谱

        Args:
            category: 菜谱分类

        Returns:
            指定分类的菜谱列表
        """
        recipes = await self.repository.fetch_all_recipes()
        if not recipes:
            return "未能获取菜谱数据"

        # 筛选指定分类的菜谱
        filtered_recipes = self.repository.get_recipes_by_category(recipes, category)

        if not filtered_recipes:
            return f"未找到分类为 '{category}' 的菜谱"

        # 简化菜谱信息
        simplified_recipes = [simplify_recipe(recipe) for recipe in filtered_recipes]

        return json.dumps(
            [recipe.model_dump() for recipe in simplified_recipes],
            ensure_ascii=False,
            indent=2,
        )

    async def get_all_categories(self) -> List[str]:
        """
        获取所有菜谱分类

        Returns:
            所有分类的列表
        """
        recipes = await self.repository.fetch_all_recipes()
        return self.repository.get_all_categories(recipes)

    @performance_tracked("get_recipe_details")
    async def get_recipe_details(self, recipe_name: str) -> str:
        """
        获取指定菜谱的详细做法

        Args:
            recipe_name: 菜谱名称

        Returns:
            菜谱的详细信息，包括食材、做法步骤、小贴士等
        """
        recipes = await self.repository.fetch_all_recipes()
        if not recipes:
            return "未能获取菜谱数据"

        # 查找指定名称的菜谱
        target_recipe = None
        for recipe in recipes:
            if recipe.name == recipe_name or recipe_name in recipe.name:
                target_recipe = recipe
                break

        if not target_recipe:
            # 如果没有找到完全匹配的，尝试模糊匹配
            for recipe in recipes:
                if (
                    recipe_name.lower() in recipe.name.lower()
                    or recipe.name.lower() in recipe_name.lower()
                ):
                    target_recipe = recipe
                    break

        if not target_recipe:
            return f"未找到名为 '{recipe_name}' 的菜谱。请检查菜谱名称是否正确，或使用 get_all_recipes 工具查看所有可用菜谱。"

        # 返回完整的菜谱信息
        return json.dumps(
            target_recipe.model_dump(),
            ensure_ascii=False,
            indent=2,
        )
