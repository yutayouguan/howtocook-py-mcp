#!/usr/bin/env python
"""
Example usage of the HowToCook MCP tools
"""

import asyncio
import json
from src.tools.get_all_recipes import get_all_recipes
from src.tools.get_recipes_by_category import get_recipes_by_category
from src.tools.what_to_eat import what_to_eat
from src.tools.recommend_meals import recommend_meals


async def main():
    print("🍳 HowToCook MCP Tools Example Usage\n")

    # Example 1: Get recipes by category
    print("1. 获取水产类菜谱:")
    seafood_recipes = await get_recipes_by_category("水产")
    seafood_data = json.loads(seafood_recipes)
    print(f"   找到 {len(seafood_data)} 个水产菜谱")
    if seafood_data:
        print(f"   例如: {seafood_data[0]['name']}")
    print()

    # Example 2: What to eat recommendation
    print("2. 为4人推荐菜谱:")
    recommendation = await what_to_eat(4)
    rec_data = json.loads(recommendation)
    print(
        f"   推荐了 {rec_data['meat_dish_count']} 个荤菜和 {rec_data['vegetable_dish_count']} 个素菜"
    )
    print(f"   消息: {rec_data['message']}")
    print()

    # Example 3: Meal planning with restrictions
    print("3. 为2人制定膳食计划（避免香菜和虾）:")
    meal_plan = await recommend_meals(2, allergies=["虾"], avoid_items=["香菜"])
    plan_data = json.loads(meal_plan)
    print(f"   制定了 {len(plan_data['weekdays'])} 天的膳食计划")
    if plan_data["weekdays"]:
        first_day = plan_data["weekdays"][0]
        print(f"   {first_day['day']} 早餐: {len(first_day['breakfast'])} 道菜")
        print(f"   {first_day['day']} 午餐: {len(first_day['lunch'])} 道菜")
        print(f"   {first_day['day']} 晚餐: {len(first_day['dinner'])} 道菜")

    print("\n✅ 所有工具测试完成!")


if __name__ == "__main__":
    asyncio.run(main())
