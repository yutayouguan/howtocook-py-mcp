"""
膳食计划提示模板
"""

from typing import List, Optional


async def meal_planning_prompt(
    people_count: int,
    dietary_restrictions: Optional[List[str]] = None,
    cuisine_preferences: Optional[List[str]] = None,
    budget_level: str = "medium",
) -> str:
    """
    膳食计划助手提示模板

    Args:
        people_count: 用餐人数
        dietary_restrictions: 饮食限制（如素食、无麸质等）
        cuisine_preferences: 菜系偏好（如川菜、粤菜等）
        budget_level: 预算水平（low/medium/high）

    Returns:
        str: 格式化的提示文本
    """

    restrictions_text = ""
    if dietary_restrictions:
        restrictions_text = f"饮食限制：{', '.join(dietary_restrictions)}\n"

    preferences_text = ""
    if cuisine_preferences:
        preferences_text = f"菜系偏好：{', '.join(cuisine_preferences)}\n"

    budget_descriptions = {
        "low": "经济实惠，注重性价比",
        "medium": "适中预算，营养均衡",
        "high": "不限预算，追求品质",
    }

    budget_text = budget_descriptions.get(budget_level, "适中预算，营养均衡")

    return f"""你是一位专业的营养师和厨师，请为以下需求制定膳食计划：

用餐人数：{people_count}人
{restrictions_text}{preferences_text}预算水平：{budget_text}

请考虑以下因素：
1. 营养均衡：确保蛋白质、维生素、纤维等营养素的合理搭配
2. 口味多样：避免连续几天重复相似的菜品
3. 季节性：优先选择当季食材
4. 制作难度：合理安排简单和复杂菜品的比例
5. 食材利用：尽量减少食材浪费，提高利用率

请使用 HowToCook MCP 服务的工具来获取菜谱信息并制定计划。"""
