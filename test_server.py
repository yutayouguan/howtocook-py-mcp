#!/usr/bin/env python
"""
HowToCook MCP 服务器的综合测试套件
测试所有工具、资源和提示模板的功能
"""

import asyncio
import json
import logging
from src.app import app
from src.tools.get_all_recipes import get_all_recipes
from src.tools.get_recipes_by_category import get_recipes_by_category
from src.tools.what_to_eat import what_to_eat
from src.tools.recommend_meals import recommend_meals
from src.cache import cache
from src.config import get_server_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_tools():
    """测试所有 MCP 工具"""
    print("🧪 开始测试 HowToCook MCP 工具...")

    # Test 1: Get all recipes
    print("\n1. 测试获取所有菜谱...")
    try:
        result = await get_all_recipes()
        data = json.loads(result)
        print(f"   ✅ 成功获取 {len(data)} 个菜谱")
    except Exception as e:
        print(f"   ❌ 失败: {e}")

    # Test 2: Get recipes by category
    print("\n2. 测试按分类获取菜谱...")
    categories = ["水产", "早餐", "荤菜", "主食"]
    for category in categories:
        try:
            result = await get_recipes_by_category(category)
            data = json.loads(result)
            print(f"   ✅ {category}: {len(data)} 个菜谱")
        except Exception as e:
            print(f"   ❌ {category} 失败: {e}")

    # Test 3: What to eat recommendations
    print("\n3. 测试菜品推荐...")
    people_counts = [2, 4, 6]
    for count in people_counts:
        try:
            result = await what_to_eat(count)
            data = json.loads(result)
            print(
                f"   ✅ {count}人: {data['meat_dish_count']}荤 + {data['vegetable_dish_count']}素"
            )
        except Exception as e:
            print(f"   ❌ {count}人 失败: {e}")

    # Test 4: Meal planning
    print("\n4. 测试膳食计划...")
    try:
        result = await recommend_meals(3, allergies=["虾"], avoid_items=["香菜"])
        data = json.loads(result)
        print(f"   ✅ 制定了 {len(data['weekdays'])} 天的膳食计划")
        if data["weekdays"]:
            first_day = data["weekdays"][0]
            print(
                f"   {first_day['day']}: 早餐{len(first_day['breakfast'])}道, 午餐{len(first_day['lunch'])}道, 晚餐{len(first_day['dinner'])}道"
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

    # Test invalid people count
    try:
        await what_to_eat(15)  # Invalid count
        print("   ❌ 应该抛出错误但没有")
    except ValueError:
        print("   ✅ 正确处理无效人数")
    except Exception as e:
        print(f"   ⚠️ 意外错误: {e}")

    # Test invalid category
    try:
        result = await get_recipes_by_category("不存在的分类")
        data = json.loads(result)
        print(f"   ✅ 不存在的分类返回 {len(data)} 个结果")
    except Exception as e:
        print(f"   ⚠️ 分类测试错误: {e}")


async def test_cache_system():
    """测试缓存系统"""
    print("\n💾 测试缓存系统...")

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
        config = get_server_config()
        print(f"   ✅ 服务器名称: {config['name']}")
        print(f"   ✅ 服务器版本: {config['version']}")
        print(f"   ✅ 缓存配置: {config['cache']}")
        print(
            f"   ✅ 推荐配置: {config['recommendation']['max_people_count']} 最大人数"
        )
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
