#!/usr/bin/env python
"""
HowToCook MCP 服务器的综合测试套件
测试所有工具、资源和提示模板的功能
"""

import asyncio
import json
import logging
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.core.app import app
from src.domain.services import RecipeService, MealService, RecommendationService
from src.infrastructure.cache import get_cache
from src.core.config import get_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_tools():
    """测试所有 MCP 工具"""
    print("🧪 开始测试 HowToCook MCP 工具...")

    recipe_service = RecipeService()
    meal_service = MealService()
    recommendation_service = RecommendationService()

    # Test 1: Get all recipes
    print("\n1. 测试获取所有菜谱...")
    try:
        result = await recipe_service.get_all_recipes()
        data = json.loads(result)
        print(f"   ✅ 成功获取 {len(data)} 个菜谱")
    except Exception as e:
        print(f"   ❌ 失败: {e}")

    # Test 2: Get recipes by category
    print("\n2. 测试按分类获取菜谱...")
    categories = ["水产", "早餐", "荤菜", "主食"]
    for category in categories:
        try:
            result = await recipe_service.get_recipes_by_category(category)
            data = json.loads(result)
            print(f"   ✅ {category}: {len(data)} 个菜谱")
        except Exception as e:
            print(f"   ❌ {category} 失败: {e}")

    # Test 3: Recipe details
    print("\n3. 测试菜谱详情...")
    try:
        result = await recipe_service.get_recipe_details("宫保鸡丁")
        data = json.loads(result)
        print(f"   ✅ 获取菜谱详情: {data.get('name', '未知')}")
    except Exception as e:
        print(f"   ❌ 失败: {e}")

    # Test 4: Search by ingredients
    print("\n4. 测试按食材搜索...")
    try:
        result = await recipe_service.search_recipes_by_ingredients(["鸡肉", "土豆"])
        data = json.loads(result)
        print(f"   ✅ 找到 {data.get('total_found', 0)} 个匹配菜谱")
    except Exception as e:
        print(f"   ❌ 失败: {e}")

    # Test 5: Filter by difficulty
    print("\n5. 测试按难度筛选...")
    try:
        result = await recipe_service.filter_recipes_by_difficulty(2)
        data = json.loads(result)
        print(f"   ✅ 2星难度菜谱: {data.get('total_count', 0)} 个")
    except Exception as e:
        print(f"   ❌ 失败: {e}")

    # Test 6: What to eat recommendations
    print("\n6. 测试菜品推荐...")
    people_counts = [2, 4, 6]
    for count in people_counts:
        try:
            result = await recommendation_service.what_to_eat(count)
            data = json.loads(result)
            print(
                f"   ✅ {count}人: {data['meat_dish_count']}荤 + {data['vegetable_dish_count']}素"
            )
        except Exception as e:
            print(f"   ❌ {count}人 失败: {e}")

    # Test 7: Meal planning
    print("\n7. 测试膳食计划...")
    try:
        result = await meal_service.recommend_meals(
            3, allergies=["虾"], avoid_items=["香菜"]
        )
        data = json.loads(result)
        print(f"   ✅ 制定了 {len(data.get('weekdays', []))} 天的膳食计划")
    except Exception as e:
        print(f"   ❌ 失败: {e}")

    # Test 8: Generate shopping list
    print("\n8. 测试购物清单生成...")
    try:
        result = await recipe_service.generate_shopping_list(
            ["宫保鸡丁", "麻婆豆腐"], 4
        )
        data = json.loads(result)
        print(f"   ✅ 生成购物清单: {data.get('total_ingredients', 0)} 种食材")
    except Exception as e:
        print(f"   ❌ 失败: {e}")

    # Test 9: Seasonal recommendations
    print("\n9. 测试季节推荐...")
    try:
        result = await recipe_service.get_seasonal_recommendations("current")
        data = json.loads(result)
        print(
            f"   ✅ {data.get('season', '未知')}季节推荐: {data.get('total_found', 0)} 个菜谱"
        )
    except Exception as e:
        print(f"   ❌ 失败: {e}")

    # Test 10: Nutrition analysis
    print("\n10. 测试营养分析...")
    try:
        result = await recipe_service.analyze_recipe_nutrition("宫保鸡丁")
        data = json.loads(result)
        print(
            f"   ✅ 营养分析: {data.get('total_nutrition', {}).get('calories', 0)} 卡路里"
        )
    except Exception as e:
        print(f"   ❌ 失败: {e}")

    print("\n✅ 工具测试完成!")


async def test_server_info():
    """测试服务器信息"""
    print("\n📊 服务器信息:")
    print(f"   名称: {app.name}")
    print(f"   版本: {app.version}")
    print(f"   说明: {app.instructions}")


async def test_error_handling():
    """测试错误处理机制"""
    print("\n🛡️ 测试错误处理...")

    recommendation_service = RecommendationService()
    recipe_service = RecipeService()

    # Test invalid people count
    try:
        await recommendation_service.what_to_eat(15)  # Invalid count
        print("   ❌ 应该抛出错误但没有")
    except ValueError:
        print("   ✅ 正确处理无效人数")
    except Exception as e:
        print(f"   ⚠️ 意外错误: {e}")

    # Test invalid category
    try:
        result = await recipe_service.get_recipes_by_category("不存在的分类")
        data = json.loads(result)
        print(f"   ✅ 不存在的分类返回 {len(data)} 个结果")
    except Exception as e:
        print(f"   ⚠️ 分类测试错误: {e}")


async def test_cache_system():
    """测试缓存系统"""
    print("\n💾 测试缓存系统...")

    cache = get_cache()

    # 测试缓存设置和获取
    try:
        await cache.set("test_key", "test_value", 60)
        cached_value = await cache.get("test_key")
        if cached_value == "test_value":
            print("   ✅ 缓存设置和获取正常")
        else:
            print("   ❌ 缓存值不匹配")
    except Exception as e:
        print(f"   ❌ 缓存测试失败: {e}")

    # 测试缓存统计
    try:
        stats = cache.get_stats()
        print(f"   ✅ 缓存统计: {stats}")
    except Exception as e:
        print(f"   ❌ 缓存统计失败: {e}")

    # 清理测试缓存
    await cache.delete("test_key")


async def test_configuration():
    """测试配置系统"""
    print("\n⚙️ 测试配置系统...")

    try:
        config = get_config()
        print(f"   ✅ 服务器名称: {config.server.name}")
        print(f"   ✅ 服务器版本: {config.server.version}")
        print(f"   ✅ 缓存配置: 启用={config.cache.enabled}, TTL={config.cache.ttl}")
        print(f"   ✅ 推荐配置: {config.recommendation.max_people_count} 最大人数")
    except Exception as e:
        print(f"   ❌ 配置测试失败: {e}")


async def main():
    """运行所有测试"""
    print("🍳 HowToCook MCP 服务器测试套件")
    print("=" * 50)

    await test_server_info()
    await test_tools()
    await test_error_handling()

    await test_cache_system()
    await test_configuration()

    print("\n🎉 所有测试完成!")


if __name__ == "__main__":
    asyncio.run(main())
