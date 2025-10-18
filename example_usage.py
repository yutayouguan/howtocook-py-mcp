#!/usr/bin/env python
"""
HowToCook MCP 工具使用示例
展示14个工具的完整功能
"""

import asyncio
import json
from src.domain.services import RecipeService, MealService, RecommendationService


async def main():
    print("🍳 HowToCook MCP 工具使用示例\n")

    recipe_service = RecipeService()
    meal_service = MealService()
    recommendation_service = RecommendationService()

    # 基础功能示例
    print("📚 基础菜谱功能:")

    # Example 1: Get recipes by category
    print("1. 获取水产类菜谱:")
    seafood_recipes = await recipe_service.get_recipes_by_category("水产")
    seafood_data = json.loads(seafood_recipes)
    print(f"   找到 {len(seafood_data)} 个水产菜谱")
    if seafood_data:
        print(f"   例如: {seafood_data[0]['name']}")
    print()

    # Example 2: Get recipe details
    print("2. 获取宫保鸡丁详细做法:")
    recipe_details = await recipe_service.get_recipe_details("宫保鸡丁")
    details_data = json.loads(recipe_details)
    if "name" in details_data:
        print(f"   菜谱: {details_data['name']}")
        print(f"   食材数量: {len(details_data.get('ingredients', []))}")
        print(f"   制作步骤: {len(details_data.get('steps', []))}")
    print()

    # 智能搜索示例
    print("🔍 智能搜索功能:")

    # Example 3: Search by ingredients
    print("3. 根据食材搜索（鸡肉+土豆）:")
    ingredient_search = await recipe_service.search_recipes_by_ingredients(
        ["鸡肉", "土豆"]
    )
    search_data = json.loads(ingredient_search)
    print(f"   找到 {search_data.get('total_found', 0)} 个匹配菜谱")
    if search_data.get("recipes"):
        print(f"   推荐: {search_data['recipes'][0]['name']}")
    print()

    # Example 4: Filter by difficulty
    print("4. 筛选简单菜谱（2星难度）:")
    easy_recipes = await recipe_service.filter_recipes_by_difficulty(2)
    easy_data = json.loads(easy_recipes)
    print(f"   找到 {easy_data.get('total_count', 0)} 个简单菜谱")
    print()

    # Example 5: Search by cuisine
    print("5. 搜索川菜:")
    sichuan_recipes = await recipe_service.search_recipes_by_cuisine("川菜")
    sichuan_data = json.loads(sichuan_recipes)
    print(f"   找到 {sichuan_data.get('total_found', 0)} 道川菜")
    print()

    # 实用功能示例
    print("🛠️ 实用辅助功能:")

    # Example 6: Generate shopping list
    print("6. 生成购物清单（宫保鸡丁+麻婆豆腐，4人份）:")
    shopping_list = await recipe_service.generate_shopping_list(
        ["宫保鸡丁", "麻婆豆腐"], 4
    )
    list_data = json.loads(shopping_list)
    print(f"   总计 {list_data.get('total_ingredients', 0)} 种食材")
    summary = list_data.get("summary", {})
    print(
        f"   生鲜: {summary.get('生鲜食材', 0)}种, 调料: {summary.get('调料香料', 0)}种"
    )
    print()

    # Example 7: Get ingredient substitutes
    print("7. 查询生抽替代方案:")
    substitutes = await recipe_service.get_ingredient_substitutes("生抽")
    sub_data = json.loads(substitutes)
    if "substitutes" in sub_data:
        print(f"   可用替代: {', '.join(sub_data['substitutes'][:2])}等")
    print()

    # 营养分析示例
    print("📊 营养分析功能:")

    # Example 8: Nutrition analysis
    print("8. 分析宫保鸡丁营养成分:")
    nutrition = await recipe_service.analyze_recipe_nutrition("宫保鸡丁")
    nutrition_data = json.loads(nutrition)
    if "total_nutrition" in nutrition_data:
        total = nutrition_data["total_nutrition"]
        print(f"   总热量: {total.get('calories', 0):.0f} 卡路里")
        print(f"   蛋白质: {total.get('protein_g', 0):.1f}g")
    print()

    # 智能推荐示例
    print("🤖 智能推荐功能:")

    # Example 9: What to eat recommendation
    print("9. 为4人推荐菜谱:")
    recommendation = await recommendation_service.what_to_eat(4)
    rec_data = json.loads(recommendation)
    print(
        f"   推荐了 {rec_data['meat_dish_count']} 个荤菜和 {rec_data['vegetable_dish_count']} 个素菜"
    )
    print()

    # Example 10: Meal planning with restrictions
    print("10. 为2人制定膳食计划（避免香菜和虾）:")
    meal_plan = await meal_service.recommend_meals(
        2, allergies=["虾"], avoid_items=["香菜"]
    )
    plan_data = json.loads(meal_plan)
    weekdays = plan_data.get("weekdays", [])
    print(f"   制定了 {len(weekdays)} 天的膳食计划")
    if weekdays:
        first_day = weekdays[0]
        print(
            f"   {first_day['day']}: 早餐{len(first_day['breakfast'])}道, 午餐{len(first_day['lunch'])}道, 晚餐{len(first_day['dinner'])}道"
        )

    print("\n✅ 14个工具功能展示完成!")
    print("🎉 HowToCook MCP 服务器功能强大，覆盖完整烹饪流程！")


if __name__ == "__main__":
    asyncio.run(main())
