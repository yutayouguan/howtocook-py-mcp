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

    @performance_tracked("search_recipes_by_ingredients")
    async def search_recipes_by_ingredients(self, ingredients: List[str]) -> str:
        """
        根据现有食材搜索可以制作的菜谱

        Args:
            ingredients: 现有食材列表

        Returns:
            包含指定食材的菜谱列表，按匹配度排序
        """
        recipes = await self.repository.fetch_all_recipes()
        if not recipes:
            return "未能获取菜谱数据"

        if not ingredients:
            return "请提供至少一种食材"

        # 搜索包含指定食材的菜谱
        matching_recipes = []
        for recipe in recipes:
            match_count = 0
            recipe_ingredients = [ing.name.lower() for ing in recipe.ingredients]

            for ingredient in ingredients:
                ingredient_lower = ingredient.lower()
                # 检查是否有食材名称包含搜索的食材
                for recipe_ing in recipe_ingredients:
                    if ingredient_lower in recipe_ing or recipe_ing in ingredient_lower:
                        match_count += 1
                        break

            if match_count > 0:
                # 计算匹配度
                match_ratio = match_count / len(ingredients)
                matching_recipes.append(
                    {
                        "recipe": recipe,
                        "match_count": match_count,
                        "match_ratio": match_ratio,
                    }
                )

        if not matching_recipes:
            return f"未找到包含食材 {', '.join(ingredients)} 的菜谱"

        # 按匹配度排序
        matching_recipes.sort(
            key=lambda x: (x["match_count"], x["match_ratio"]), reverse=True
        )

        # 简化菜谱信息并添加匹配信息
        result_recipes = []
        for item in matching_recipes[:20]:  # 限制返回前20个结果
            recipe = item["recipe"]
            simplified = simplify_recipe(recipe)
            simplified_dict = simplified.model_dump()
            simplified_dict["match_info"] = {
                "matched_ingredients": item["match_count"],
                "total_searched": len(ingredients),
                "match_ratio": f"{item['match_ratio']:.1%}",
            }
            result_recipes.append(simplified_dict)

        return json.dumps(
            {
                "searched_ingredients": ingredients,
                "total_found": len(matching_recipes),
                "recipes": result_recipes,
            },
            ensure_ascii=False,
            indent=2,
        )

    @performance_tracked("filter_recipes_by_difficulty")
    async def filter_recipes_by_difficulty(self, difficulty: int) -> str:
        """
        按烹饪难度筛选菜谱

        Args:
            difficulty: 烹饪难度等级，1-5星

        Returns:
            指定难度等级的菜谱列表
        """
        recipes = await self.repository.fetch_all_recipes()
        if not recipes:
            return "未能获取菜谱数据"

        if difficulty < 1 or difficulty > 5:
            return "难度等级必须在1-5之间（1=最简单，5=最复杂）"

        # 筛选指定难度的菜谱
        filtered_recipes = [
            recipe for recipe in recipes if recipe.difficulty == difficulty
        ]

        if not filtered_recipes:
            return f"未找到难度等级为 {difficulty} 星的菜谱"

        # 简化菜谱信息
        simplified_recipes = [simplify_recipe(recipe) for recipe in filtered_recipes]

        difficulty_desc = {1: "非常简单", 2: "简单", 3: "中等", 4: "较难", 5: "很难"}

        return json.dumps(
            {
                "difficulty_level": difficulty,
                "difficulty_description": difficulty_desc.get(difficulty, "未知"),
                "total_count": len(filtered_recipes),
                "recipes": [recipe.model_dump() for recipe in simplified_recipes],
            },
            ensure_ascii=False,
            indent=2,
        )

    @performance_tracked("search_recipes_by_time")
    async def search_recipes_by_time(self, max_time_minutes: int) -> str:
        """
        按制作时间筛选菜谱

        Args:
            max_time_minutes: 最大制作时间（分钟）

        Returns:
            在指定时间内能完成的菜谱列表
        """
        recipes = await self.repository.fetch_all_recipes()
        if not recipes:
            return "未能获取菜谱数据"

        if max_time_minutes <= 0:
            return "制作时间必须大于0分钟"

        # 筛选在指定时间内能完成的菜谱
        quick_recipes = []
        for recipe in recipes:
            # 如果有总时间信息，使用总时间；否则使用烹饪时间；都没有则跳过
            recipe_time = recipe.total_time_minutes or recipe.cook_time_minutes
            if recipe_time and recipe_time <= max_time_minutes:
                quick_recipes.append(recipe)

        if not quick_recipes:
            return f"未找到在 {max_time_minutes} 分钟内能完成的菜谱"

        # 按时间排序（从短到长）
        quick_recipes.sort(
            key=lambda x: x.total_time_minutes or x.cook_time_minutes or 0
        )

        # 简化菜谱信息并添加时间信息
        result_recipes = []
        for recipe in quick_recipes:
            simplified = simplify_recipe(recipe)
            simplified_dict = simplified.model_dump()
            simplified_dict["time_info"] = {
                "total_time_minutes": recipe.total_time_minutes,
                "cook_time_minutes": recipe.cook_time_minutes,
                "prep_time_minutes": recipe.prep_time_minutes,
            }
            result_recipes.append(simplified_dict)

        return json.dumps(
            {
                "max_time_minutes": max_time_minutes,
                "total_found": len(quick_recipes),
                "recipes": result_recipes,
            },
            ensure_ascii=False,
            indent=2,
        )

    @performance_tracked("generate_shopping_list")
    async def generate_shopping_list(
        self, recipe_names: List[str], people_count: int = 1
    ) -> str:
        """
        根据菜谱生成购物清单

        Args:
            recipe_names: 菜谱名称列表
            people_count: 用餐人数

        Returns:
            按分类整理的购物清单
        """
        from ...shared.constants import SPICE_KEYWORDS, FRESH_KEYWORDS, PANTRY_KEYWORDS

        recipes = await self.repository.fetch_all_recipes()
        if not recipes:
            return "未能获取菜谱数据"

        if not recipe_names:
            return "请提供至少一个菜谱名称"

        if people_count <= 0:
            return "用餐人数必须大于0"

        # 查找指定的菜谱
        selected_recipes = []
        not_found = []

        for recipe_name in recipe_names:
            found = False
            for recipe in recipes:
                if recipe.name == recipe_name or recipe_name in recipe.name:
                    selected_recipes.append(recipe)
                    found = True
                    break
            if not found:
                not_found.append(recipe_name)

        if not selected_recipes:
            return f"未找到任何指定的菜谱: {', '.join(recipe_names)}"

        # 收集所有食材
        ingredient_dict = {}
        for recipe in selected_recipes:
            # 根据人数调整分量
            servings_ratio = (
                people_count / recipe.servings if recipe.servings > 0 else 1
            )

            for ingredient in recipe.ingredients:
                key = ingredient.name
                if key in ingredient_dict:
                    # 如果已存在，尝试合并数量
                    existing = ingredient_dict[key]
                    if ingredient.quantity and existing.get("quantity"):
                        # 如果单位相同，合并数量
                        if ingredient.unit == existing.get("unit"):
                            existing["quantity"] += ingredient.quantity * servings_ratio
                        else:
                            # 单位不同，保留文本描述
                            existing["text_quantity"] += (
                                f" + {ingredient.text_quantity}"
                            )
                    else:
                        existing["text_quantity"] += f" + {ingredient.text_quantity}"
                else:
                    # 新食材
                    adjusted_quantity = (
                        ingredient.quantity * servings_ratio
                        if ingredient.quantity
                        else None
                    )
                    ingredient_dict[key] = {
                        "name": ingredient.name,
                        "quantity": adjusted_quantity,
                        "unit": ingredient.unit,
                        "text_quantity": ingredient.text_quantity,
                        "notes": ingredient.notes or "",
                    }

        # 按类别分类食材
        categorized_ingredients = {
            "调料香料": [],
            "生鲜食材": [],
            "主食干货": [],
            "其他": [],
        }

        for ingredient in ingredient_dict.values():
            name_lower = ingredient["name"].lower()

            # 判断食材类别
            if any(keyword in name_lower for keyword in SPICE_KEYWORDS):
                categorized_ingredients["调料香料"].append(ingredient)
            elif any(keyword in name_lower for keyword in FRESH_KEYWORDS):
                categorized_ingredients["生鲜食材"].append(ingredient)
            elif any(keyword in name_lower for keyword in PANTRY_KEYWORDS):
                categorized_ingredients["主食干货"].append(ingredient)
            else:
                categorized_ingredients["其他"].append(ingredient)

        # 生成购物清单
        result = {
            "selected_recipes": [recipe.name for recipe in selected_recipes],
            "people_count": people_count,
            "shopping_list": categorized_ingredients,
            "total_ingredients": len(ingredient_dict),
            "summary": {
                "调料香料": len(categorized_ingredients["调料香料"]),
                "生鲜食材": len(categorized_ingredients["生鲜食材"]),
                "主食干货": len(categorized_ingredients["主食干货"]),
                "其他": len(categorized_ingredients["其他"]),
            },
        }

        if not_found:
            result["not_found_recipes"] = not_found

        return json.dumps(result, ensure_ascii=False, indent=2)
