#!/usr/bin/env python
"""
测试 MCP 服务器功能
"""

import asyncio
import json
from src.core import app


async def test_prompts():
    """测试提示模板"""
    print("=== 测试提示模板 ===")

    try:
        # 测试膳食计划提示
        meal_prompt = await app.get_prompt(
            "meal_planning_assistant",
            {
                "people_count": 2,
                "dietary_restrictions": ["素食"],
                "budget_level": "medium",
            },
        )
        print("✅ 膳食计划提示测试成功")

        # 测试菜谱推荐提示
        recipe_prompt = await app.get_prompt(
            "recipe_recommendation",
            {"occasion": "晚餐", "cooking_time": 30, "skill_level": "beginner"},
        )
        print("✅ 菜谱推荐提示测试成功")

    except Exception as e:
        print(f"❌ 提示测试失败: {e}")


async def test_tools():
    """测试工具"""
    print("\n=== 测试工具 ===")

    try:
        # 测试获取所有菜谱
        result = await app.call_tool("get_all_recipes", {})
        print("✅ 获取所有菜谱工具测试成功")

        # 测试推荐菜品
        result = await app.call_tool("what_to_eat", {"people_count": 2})
        print("✅ 推荐菜品工具测试成功")

    except Exception as e:
        print(f"❌ 工具测试失败: {e}")


async def test_resources():
    """测试资源"""
    print("\n=== 测试资源 ===")

    try:
        # 测试分类资源
        result = await app.read_resource("howtocook://categories")
        print("✅ 分类资源测试成功")

        # 测试统计资源
        result = await app.read_resource("howtocook://stats")
        print("✅ 统计资源测试成功")

        # 测试健康检查资源
        result = await app.read_resource("howtocook://health")
        print("✅ 健康检查资源测试成功")

    except Exception as e:
        print(f"❌ 资源测试失败: {e}")


async def main():
    """主测试函数"""
    print("开始测试 HowToCook MCP 服务器...")

    await test_prompts()
    await test_tools()
    await test_resources()

    print("\n测试完成！")


if __name__ == "__main__":
    asyncio.run(main())
