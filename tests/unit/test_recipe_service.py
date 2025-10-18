"""
RecipeService 单元测试
"""

import pytest
import json
from unittest.mock import AsyncMock, patch
from src.domain.services.recipe_service import RecipeService
from src.domain.models.recipe import Recipe, Ingredient, Step


@pytest.fixture
def sample_recipe():
    """示例菜谱数据"""
    return Recipe(
        id="test-recipe-1",
        name="测试菜谱",
        description="这是一个测试菜谱",
        source_path="test/path",
        category="测试",
        difficulty=2,
        tags=["测试", "简单"],
        servings=2,
        ingredients=[
            Ingredient(name="测试食材1", text_quantity="100g"),
            Ingredient(name="测试食材2", text_quantity="50ml"),
        ],
        steps=[Step(step=1, description="第一步"), Step(step=2, description="第二步")],
    )


@pytest.fixture
def recipe_service():
    """RecipeService 实例"""
    return RecipeService()


class TestRecipeService:
    """RecipeService 测试类"""

    @pytest.mark.asyncio
    async def test_get_all_recipes_success(self, recipe_service, sample_recipe):
        """测试成功获取所有菜谱"""
        with patch.object(
            recipe_service.repository, "fetch_all_recipes", return_value=[sample_recipe]
        ):
            result = await recipe_service.get_all_recipes()
            data = json.loads(result)

            assert len(data) == 1
            assert data[0]["name"] == "测试菜谱"

    @pytest.mark.asyncio
    async def test_get_all_recipes_empty(self, recipe_service):
        """测试获取空菜谱列表"""
        with patch.object(
            recipe_service.repository, "fetch_all_recipes", return_value=[]
        ):
            result = await recipe_service.get_all_recipes()

            assert result == "未能获取菜谱数据"

    @pytest.mark.asyncio
    async def test_get_recipe_details_found(self, recipe_service, sample_recipe):
        """测试成功获取菜谱详情"""
        with patch.object(
            recipe_service.repository, "fetch_all_recipes", return_value=[sample_recipe]
        ):
            result = await recipe_service.get_recipe_details("测试菜谱")
            data = json.loads(result)

            assert data["name"] == "测试菜谱"
            assert data["difficulty"] == 2
            assert len(data["ingredients"]) == 2

    @pytest.mark.asyncio
    async def test_get_recipe_details_not_found(self, recipe_service, sample_recipe):
        """测试菜谱未找到"""
        with patch.object(
            recipe_service.repository, "fetch_all_recipes", return_value=[sample_recipe]
        ):
            result = await recipe_service.get_recipe_details("不存在的菜谱")

            assert "未找到名为" in result

    @pytest.mark.asyncio
    async def test_search_recipes_by_ingredients(self, recipe_service, sample_recipe):
        """测试按食材搜索"""
        with patch.object(
            recipe_service.repository, "fetch_all_recipes", return_value=[sample_recipe]
        ):
            result = await recipe_service.search_recipes_by_ingredients(["测试食材1"])
            data = json.loads(result)

            assert data["total_found"] == 1
            assert len(data["recipes"]) == 1

    @pytest.mark.asyncio
    async def test_filter_recipes_by_difficulty(self, recipe_service, sample_recipe):
        """测试按难度筛选"""
        with patch.object(
            recipe_service.repository, "fetch_all_recipes", return_value=[sample_recipe]
        ):
            result = await recipe_service.filter_recipes_by_difficulty(2)
            data = json.loads(result)

            assert data["difficulty_level"] == 2
            assert data["total_count"] == 1

    @pytest.mark.asyncio
    async def test_filter_recipes_invalid_difficulty(self, recipe_service):
        """测试无效难度参数"""
        result = await recipe_service.filter_recipes_by_difficulty(6)

        assert "难度等级必须在1-5之间" in result

    @pytest.mark.asyncio
    async def test_generate_shopping_list(self, recipe_service, sample_recipe):
        """测试生成购物清单"""
        with patch.object(
            recipe_service.repository, "fetch_all_recipes", return_value=[sample_recipe]
        ):
            result = await recipe_service.generate_shopping_list(["测试菜谱"], 2)
            data = json.loads(result)

            assert data["people_count"] == 2
            assert data["total_ingredients"] == 2
            assert len(data["selected_recipes"]) == 1

    @pytest.mark.asyncio
    async def test_get_ingredient_substitutes_found(self, recipe_service):
        """测试找到食材替代"""
        result = await recipe_service.get_ingredient_substitutes("生抽")
        data = json.loads(result)

        assert data["original_ingredient"] == "生抽"
        assert len(data["substitutes"]) > 0

    @pytest.mark.asyncio
    async def test_get_ingredient_substitutes_not_found(self, recipe_service):
        """测试未找到食材替代"""
        result = await recipe_service.get_ingredient_substitutes("不存在的食材")

        assert "暂未找到" in result
