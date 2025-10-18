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

    @performance_tracked("search_recipes_by_cuisine")
    async def search_recipes_by_cuisine(self, cuisine_type: str) -> str:
        """
        按菜系搜索菜谱

        Args:
            cuisine_type: 菜系类型

        Returns:
            指定菜系的菜谱列表
        """
        from ...shared.constants import CUISINE_TYPES

        recipes = await self.repository.fetch_all_recipes()
        if not recipes:
            return "未能获取菜谱数据"

        # 获取菜系关键词
        keywords = CUISINE_TYPES.get(cuisine_type, [cuisine_type])

        # 搜索包含菜系关键词的菜谱
        matching_recipes = []
        for recipe in recipes:
            recipe_text = f"{recipe.name} {recipe.description}".lower()

            # 检查是否包含菜系关键词
            for keyword in keywords:
                if keyword.lower() in recipe_text:
                    matching_recipes.append(recipe)
                    break

        if not matching_recipes:
            available_cuisines = list(CUISINE_TYPES.keys())
            return f"未找到 '{cuisine_type}' 菜系的菜谱。支持的菜系: {', '.join(available_cuisines)}"

        # 简化菜谱信息
        simplified_recipes = [simplify_recipe(recipe) for recipe in matching_recipes]

        return json.dumps(
            {
                "cuisine_type": cuisine_type,
                "total_found": len(matching_recipes),
                "recipes": [recipe.model_dump() for recipe in simplified_recipes],
            },
            ensure_ascii=False,
            indent=2,
        )

    @performance_tracked("get_ingredient_substitutes")
    async def get_ingredient_substitutes(self, ingredient_name: str) -> str:
        """
        获取食材的替代建议

        Args:
            ingredient_name: 需要替代的食材名称

        Returns:
            该食材的替代方案和使用建议
        """
        from ...shared.constants import INGREDIENT_SUBSTITUTES

        # 直接匹配
        if ingredient_name in INGREDIENT_SUBSTITUTES:
            substitutes = INGREDIENT_SUBSTITUTES[ingredient_name]
        else:
            # 模糊匹配
            substitutes = []
            for key, values in INGREDIENT_SUBSTITUTES.items():
                if ingredient_name in key or key in ingredient_name:
                    substitutes = values
                    ingredient_name = key  # 使用匹配到的标准名称
                    break

        if not substitutes:
            return f"暂未找到 '{ingredient_name}' 的替代方案。建议查找相似功能的食材或调料。"

        return json.dumps(
            {
                "original_ingredient": ingredient_name,
                "substitutes": substitutes,
                "usage_tips": [
                    "替代时请注意口味差异，可能需要调整用量",
                    "建议先少量尝试，根据个人口味调整",
                    "某些替代品可能会改变菜品的最终颜色或质地",
                ],
            },
            ensure_ascii=False,
            indent=2,
        )

    @performance_tracked("search_recipes_by_tags")
    async def search_recipes_by_tags(self, tags: List[str]) -> str:
        """
        按标签搜索菜谱

        Args:
            tags: 标签列表

        Returns:
            包含指定标签的菜谱列表
        """
        recipes = await self.repository.fetch_all_recipes()
        if not recipes:
            return "未能获取菜谱数据"

        if not tags:
            return "请提供至少一个标签"

        # 搜索包含指定标签的菜谱
        matching_recipes = []
        for recipe in recipes:
            recipe_tags = [tag.lower() for tag in recipe.tags]
            recipe_text = f"{recipe.name} {recipe.description}".lower()

            match_count = 0
            for tag in tags:
                tag_lower = tag.lower()
                # 检查标签是否在菜谱标签中或描述中
                if tag_lower in recipe_tags or tag_lower in recipe_text:
                    match_count += 1

            if match_count > 0:
                matching_recipes.append(
                    {
                        "recipe": recipe,
                        "match_count": match_count,
                        "match_ratio": match_count / len(tags),
                    }
                )

        if not matching_recipes:
            return f"未找到包含标签 {', '.join(tags)} 的菜谱"

        # 按匹配度排序
        matching_recipes.sort(
            key=lambda x: (x["match_count"], x["match_ratio"]), reverse=True
        )

        # 简化菜谱信息
        result_recipes = []
        for item in matching_recipes[:20]:  # 限制返回前20个结果
            recipe = item["recipe"]
            simplified = simplify_recipe(recipe)
            simplified_dict = simplified.model_dump()
            simplified_dict["match_info"] = {
                "matched_tags": item["match_count"],
                "total_searched": len(tags),
                "recipe_tags": recipe.tags,
            }
            result_recipes.append(simplified_dict)

        return json.dumps(
            {
                "searched_tags": tags,
                "total_found": len(matching_recipes),
                "recipes": result_recipes,
            },
            ensure_ascii=False,
            indent=2,
        )

    @performance_tracked("get_seasonal_recommendations")
    async def get_seasonal_recommendations(self, season: str = "current") -> str:
        """
        获取季节性菜谱推荐

        Args:
            season: 季节

        Returns:
            适合该季节的菜谱推荐
        """
        from ...shared.constants import SEASONAL_INGREDIENTS
        import datetime

        # 确定季节
        if season == "current":
            month = datetime.datetime.now().month
            if month in [3, 4, 5]:
                season = "spring"
            elif month in [6, 7, 8]:
                season = "summer"
            elif month in [9, 10, 11]:
                season = "autumn"
            else:
                season = "winter"

        season_map = {
            "spring": "春季",
            "summer": "夏季",
            "autumn": "秋季",
            "winter": "冬季",
        }

        if season not in SEASONAL_INGREDIENTS:
            return f"不支持的季节: {season}。支持的季节: spring(春), summer(夏), autumn(秋), winter(冬), current(当前)"

        seasonal_ingredients = SEASONAL_INGREDIENTS[season]

        recipes = await self.repository.fetch_all_recipes()
        if not recipes:
            return "未能获取菜谱数据"

        # 搜索包含时令食材的菜谱
        seasonal_recipes = []
        for recipe in recipes:
            ingredient_names = [ing.name.lower() for ing in recipe.ingredients]
            recipe_text = f"{recipe.name} {recipe.description}".lower()

            seasonal_count = 0
            matched_ingredients = []

            for seasonal_ing in seasonal_ingredients:
                seasonal_ing_lower = seasonal_ing.lower()
                # 检查是否包含时令食材
                for ing_name in ingredient_names:
                    if seasonal_ing_lower in ing_name or ing_name in seasonal_ing_lower:
                        seasonal_count += 1
                        matched_ingredients.append(seasonal_ing)
                        break
                # 也检查菜名和描述
                if seasonal_ing_lower in recipe_text:
                    if seasonal_ing not in matched_ingredients:
                        seasonal_count += 1
                        matched_ingredients.append(seasonal_ing)

            if seasonal_count > 0:
                seasonal_recipes.append(
                    {
                        "recipe": recipe,
                        "seasonal_count": seasonal_count,
                        "matched_ingredients": matched_ingredients,
                    }
                )

        if not seasonal_recipes:
            return f"未找到适合{season_map.get(season, season)}的菜谱"

        # 按时令食材数量排序
        seasonal_recipes.sort(key=lambda x: x["seasonal_count"], reverse=True)

        # 简化菜谱信息
        result_recipes = []
        for item in seasonal_recipes[:15]:  # 限制返回前15个结果
            recipe = item["recipe"]
            simplified = simplify_recipe(recipe)
            simplified_dict = simplified.model_dump()
            simplified_dict["seasonal_info"] = {
                "seasonal_ingredients_count": item["seasonal_count"],
                "matched_seasonal_ingredients": item["matched_ingredients"],
            }
            result_recipes.append(simplified_dict)

        return json.dumps(
            {
                "season": season_map.get(season, season),
                "seasonal_ingredients": seasonal_ingredients,
                "total_found": len(seasonal_recipes),
                "recipes": result_recipes,
            },
            ensure_ascii=False,
            indent=2,
        )

    @performance_tracked("analyze_recipe_nutrition")
    async def analyze_recipe_nutrition(self, recipe_name: str) -> str:
        """
        分析菜谱营养成分

        Args:
            recipe_name: 菜谱名称

        Returns:
            菜谱的营养分析
        """
        from ...shared.constants import NUTRITION_DATA

        recipes = await self.repository.fetch_all_recipes()
        if not recipes:
            return "未能获取菜谱数据"

        # 查找指定菜谱
        target_recipe = None
        for recipe in recipes:
            if recipe.name == recipe_name or recipe_name in recipe.name:
                target_recipe = recipe
                break

        if not target_recipe:
            return f"未找到名为 '{recipe_name}' 的菜谱"

        # 分析营养成分
        total_nutrition = {"calories": 0, "protein": 0, "fat": 0, "carbs": 0}
        analyzed_ingredients = []
        unknown_ingredients = []

        for ingredient in target_recipe.ingredients:
            ing_name = ingredient.name
            found_nutrition = False

            # 尝试匹配营养数据
            for nutrition_key, nutrition_value in NUTRITION_DATA.items():
                if nutrition_key in ing_name or ing_name in nutrition_key:
                    # 估算重量 (简化处理)
                    estimated_weight = 100  # 默认100g
                    if ingredient.quantity:
                        estimated_weight = ingredient.quantity
                    elif "克" in ingredient.text_quantity:
                        try:
                            estimated_weight = float(
                                "".join(filter(str.isdigit, ingredient.text_quantity))
                            )
                        except:
                            pass

                    # 计算营养成分
                    weight_ratio = estimated_weight / 100
                    ingredient_nutrition = {
                        "name": ing_name,
                        "weight_g": estimated_weight,
                        "calories": nutrition_value["calories"] * weight_ratio,
                        "protein": nutrition_value["protein"] * weight_ratio,
                        "fat": nutrition_value["fat"] * weight_ratio,
                        "carbs": nutrition_value["carbs"] * weight_ratio,
                    }

                    analyzed_ingredients.append(ingredient_nutrition)

                    # 累加到总营养
                    for key in total_nutrition:
                        total_nutrition[key] += ingredient_nutrition[key]

                    found_nutrition = True
                    break

            if not found_nutrition:
                unknown_ingredients.append(ing_name)

        # 按人数调整
        servings = target_recipe.servings if target_recipe.servings > 0 else 1
        per_serving_nutrition = {
            key: round(value / servings, 1) for key, value in total_nutrition.items()
        }

        return json.dumps(
            {
                "recipe_name": target_recipe.name,
                "servings": servings,
                "total_nutrition": {
                    "calories": round(total_nutrition["calories"], 1),
                    "protein_g": round(total_nutrition["protein"], 1),
                    "fat_g": round(total_nutrition["fat"], 1),
                    "carbs_g": round(total_nutrition["carbs"], 1),
                },
                "per_serving_nutrition": {
                    "calories": per_serving_nutrition["calories"],
                    "protein_g": per_serving_nutrition["protein"],
                    "fat_g": per_serving_nutrition["fat"],
                    "carbs_g": per_serving_nutrition["carbs"],
                },
                "analyzed_ingredients": analyzed_ingredients,
                "unknown_ingredients": unknown_ingredients,
                "analysis_note": "营养数据为估算值，实际数值可能因食材品质、烹饪方法等因素有所差异",
            },
            ensure_ascii=False,
            indent=2,
        )
