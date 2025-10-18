"""
菜谱相关的MCP工具
"""

from fastmcp import FastMCP
from ...domain.services import RecipeService


def register_recipe_tools(server: FastMCP):
    """注册菜谱相关工具"""
    recipe_service = RecipeService()

    @server.tool()
    async def get_all_recipes():
        """
        获取所有菜谱

        Returns:
            所有菜谱的简化信息，只包含名称和描述
        """
        return await recipe_service.get_all_recipes()

    @server.tool()
    async def get_recipes_by_category(category: str):
        """
        根据分类获取菜谱

        Args:
            category: 菜谱分类，如"荤菜"、"素菜"、"汤羹"等

        Returns:
            指定分类的菜谱列表
        """
        return await recipe_service.get_recipes_by_category(category)

    @server.tool()
    async def get_recipe_details(recipe_name: str):
        """
        获取指定菜谱的详细做法

        Args:
            recipe_name: 菜谱名称，如"宫保鸡丁"、"麻婆豆腐"等

        Returns:
            菜谱的详细信息，包括食材、做法步骤、小贴士等
        """
        return await recipe_service.get_recipe_details(recipe_name)

    @server.tool()
    async def search_recipes_by_ingredients(ingredients: list[str]):
        """
        根据现有食材搜索可以制作的菜谱

        Args:
            ingredients: 现有食材列表，如["鸡肉", "土豆", "胡萝卜"]

        Returns:
            包含指定食材的菜谱列表，按匹配度排序
        """
        return await recipe_service.search_recipes_by_ingredients(ingredients)

    @server.tool()
    async def filter_recipes_by_difficulty(difficulty: int):
        """
        按烹饪难度筛选菜谱

        Args:
            difficulty: 烹饪难度等级，1-5星（1=最简单，5=最复杂）

        Returns:
            指定难度等级的菜谱列表
        """
        return await recipe_service.filter_recipes_by_difficulty(difficulty)

    @server.tool()
    async def search_recipes_by_time(max_time_minutes: int):
        """
        按制作时间筛选菜谱

        Args:
            max_time_minutes: 最大制作时间（分钟），如30表示30分钟内能完成的菜

        Returns:
            在指定时间内能完成的菜谱列表
        """
        return await recipe_service.search_recipes_by_time(max_time_minutes)

    @server.tool()
    async def generate_shopping_list(recipe_names: list[str], people_count: int = 1):
        """
        根据菜谱生成购物清单

        Args:
            recipe_names: 菜谱名称列表，如["宫保鸡丁", "麻婆豆腐"]
            people_count: 用餐人数，用于调整食材用量

        Returns:
            按分类整理的购物清单，包含食材名称和用量
        """
        return await recipe_service.generate_shopping_list(recipe_names, people_count)

    @server.tool()
    async def search_recipes_by_cuisine(cuisine_type: str):
        """
        按菜系搜索菜谱

        Args:
            cuisine_type: 菜系类型，如"川菜"、"粤菜"、"鲁菜"、"苏菜"、"浙菜"、"闽菜"、"湘菜"、"徽菜"等

        Returns:
            指定菜系的菜谱列表
        """
        return await recipe_service.search_recipes_by_cuisine(cuisine_type)

    @server.tool()
    async def get_ingredient_substitutes(ingredient_name: str):
        """
        获取食材的替代建议

        Args:
            ingredient_name: 需要替代的食材名称，如"生抽"、"料酒"、"五花肉"等

        Returns:
            该食材的替代方案和使用建议
        """
        return await recipe_service.get_ingredient_substitutes(ingredient_name)

    @server.tool()
    async def search_recipes_by_tags(tags: list[str]):
        """
        按标签搜索菜谱

        Args:
            tags: 标签列表，如["下饭菜", "宴客菜", "快手菜", "素食", "减脂"]等

        Returns:
            包含指定标签的菜谱列表
        """
        return await recipe_service.search_recipes_by_tags(tags)

    @server.tool()
    async def get_seasonal_recommendations(season: str = "current"):
        """
        获取季节性菜谱推荐

        Args:
            season: 季节，可选值："spring"(春)、"summer"(夏)、"autumn"(秋)、"winter"(冬)、"current"(当前季节)

        Returns:
            适合该季节的菜谱推荐，包含时令食材
        """
        return await recipe_service.get_seasonal_recommendations(season)

    @server.tool()
    async def analyze_recipe_nutrition(recipe_name: str):
        """
        分析菜谱营养成分

        Args:
            recipe_name: 菜谱名称

        Returns:
            菜谱的营养分析，包括估算的卡路里、蛋白质、脂肪等信息
        """
        return await recipe_service.analyze_recipe_nutrition(recipe_name)
