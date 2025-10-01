"""
菜谱推荐提示模板
"""

from typing import Optional


async def recipe_recommendation_prompt(
    occasion: str, cooking_time: Optional[int] = None, skill_level: str = "beginner"
) -> str:
    """
    菜谱推荐提示模板

    Args:
        occasion: 用餐场合（如早餐、午餐、晚餐、聚会等）
        cooking_time: 可用烹饪时间（分钟）
        skill_level: 烹饪技能水平（beginner/intermediate/advanced）

    Returns:
        str: 格式化的提示文本
    """

    time_text = ""
    if cooking_time:
        time_text = f"可用时间：{cooking_time}分钟\n"

    skill_descriptions = {
        "beginner": "新手友好，步骤简单",
        "intermediate": "有一定基础，可以尝试中等难度",
        "advanced": "经验丰富，可以挑战复杂菜品",
    }

    skill_text = skill_descriptions.get(skill_level, "新手友好，步骤简单")

    return f"""请为以下场合推荐合适的菜谱：

用餐场合：{occasion}
{time_text}技能水平：{skill_text}

推荐要求：
1. 符合用餐场合的特点和氛围
2. 考虑制作时间和技能要求
3. 提供详细的制作步骤和注意事项
4. 如果可能，推荐搭配的菜品或饮品

请使用 HowToCook MCP 服务来查找和推荐菜谱。"""
