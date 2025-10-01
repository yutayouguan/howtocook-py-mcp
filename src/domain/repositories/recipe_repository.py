"""
菜谱数据访问层
"""

import httpx
from typing import List
from ..models import Recipe
from ...infrastructure.cache import cached
from ...core.config import get_config


class RecipeRepository:
    """菜谱数据仓库"""

    @cached(ttl=3600, key_prefix="recipes")  # 缓存1小时
    async def fetch_all_recipes(self) -> List[Recipe]:
        """
        异步获取所有菜谱数据

        Returns:
            List[Recipe]: 菜谱列表，如果获取失败则返回空列表
        """
        try:
            config = get_config()
            async with httpx.AsyncClient() as client:
                response = await client.get(config.data_source.recipes_url)

                if response.status_code != 200:
                    raise Exception(f"HTTP 请求失败! 状态码: {response.status_code}")

                # 解析 JSON 数据并验证模型
                data = response.json()
                return [Recipe.model_validate(recipe) for recipe in data]
        except Exception as error:
            print(f"获取远程菜谱数据失败: {error}")
            return []

    def get_all_categories(self, recipes: List[Recipe]) -> List[str]:
        """
        从菜谱列表中提取所有分类

        Args:
            recipes: 菜谱列表

        Returns:
            List[str]: 所有分类的列表
        """
        categories = set()
        for recipe in recipes:
            if recipe.category:
                categories.add(recipe.category)
        return list(categories)

    def get_recipes_by_category(
        self, recipes: List[Recipe], category: str
    ) -> List[Recipe]:
        """
        根据分类筛选菜谱

        Args:
            recipes: 菜谱列表
            category: 分类名称

        Returns:
            List[Recipe]: 指定分类的菜谱列表
        """
        return [recipe for recipe in recipes if recipe.category == category]
