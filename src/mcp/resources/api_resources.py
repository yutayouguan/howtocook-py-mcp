"""
MCP API资源
"""

import json
from fastmcp import FastMCP
from ...domain.services import RecipeService
from ...infrastructure.monitoring.health_checker import get_health_checker


def register_api_resources(server: FastMCP):
    """注册API资源"""
    recipe_service = RecipeService()
    health_checker = get_health_checker()

    @server.resource("howtocook://categories")
    async def get_recipe_categories():
        """
        获取所有可用的菜谱分类

        Returns:
            所有菜谱分类的列表
        """
        categories = await recipe_service.get_all_categories()
        if not categories:
            return json.dumps({"error": "无法获取菜谱数据"}, ensure_ascii=False)

        categories.sort()

        return json.dumps(
            {
                "categories": categories,
                "total_count": len(categories),
                "description": "所有可用的菜谱分类",
            },
            ensure_ascii=False,
            indent=2,
        )

    @server.resource("howtocook://stats")
    async def get_recipe_stats():
        """
        获取菜谱统计信息

        Returns:
            菜谱的统计信息
        """
        from ...domain.repositories import RecipeRepository

        repository = RecipeRepository()
        recipes = await repository.fetch_all_recipes()

        if not recipes:
            return json.dumps({"error": "无法获取菜谱数据"}, ensure_ascii=False)

        # 统计各分类的菜谱数量
        category_counts = {}
        for recipe in recipes:
            category = recipe.category or "未分类"
            category_counts[category] = category_counts.get(category, 0) + 1

        # 统计难度分布
        difficulty_counts = {}
        for recipe in recipes:
            difficulty = recipe.difficulty
            difficulty_counts[difficulty] = difficulty_counts.get(difficulty, 0) + 1

        return json.dumps(
            {
                "total_recipes": len(recipes),
                "categories": category_counts,
                "difficulty_distribution": difficulty_counts,
                "description": "菜谱数据统计信息",
            },
            ensure_ascii=False,
            indent=2,
        )

    @server.resource("howtocook://health")
    async def get_health_status():
        """
        获取服务器健康状态

        Returns:
            服务器健康检查结果
        """
        health_result = await health_checker.full_health_check()
        return json.dumps(health_result, ensure_ascii=False, indent=2)
