# HowToCook MCP API 文档

## 概述

HowToCook MCP 服务器提供了一套完整的菜谱管理和膳食计划 API，基于 FastMCP 框架构建。服务器包含 **14个专业工具**，覆盖从菜谱搜索到营养分析的完整烹饪流程。

## 工具 (Tools) - 14个

### 📚 基础菜谱功能 (3个)

#### 1. get_all_recipes
获取所有菜谱的简化信息。

**参数**: 无

**返回**: JSON 格式的菜谱列表，包含名称和描述

**示例**:
```json
[
  {
    "name": "宫保鸡丁的做法",
    "description": "老派川菜的简单做法分享"
  }
]
```

#### 2. get_recipes_by_category
根据分类查询菜谱。

**参数**:
- `category` (string): 菜谱分类名称

**返回**: 该分类下所有菜谱的详细信息

#### 3. get_recipe_details
获取指定菜谱的详细做法。

**参数**:
- `recipe_name` (string): 菜谱名称

**返回**: 完整的菜谱信息，包括食材、步骤、小贴士

**示例**:
```json
{
  "id": "dishes-meat_dish-宫保鸡丁-宫保鸡丁",
  "name": "宫保鸡丁的做法",
  "description": "老派川菜的简单做法分享",
  "ingredients": [...],
  "steps": [...],
  "difficulty": 4,
  "servings": 2
}
```

### 🔍 智能搜索功能 (6个)

#### 4. search_recipes_by_ingredients
根据现有食材搜索可以制作的菜谱。

**参数**:
- `ingredients` (array): 现有食材列表

**返回**: 按匹配度排序的菜谱列表

**示例**:
```json
{
  "searched_ingredients": ["鸡肉", "土豆"],
  "total_found": 25,
  "recipes": [...]
}
```

#### 5. filter_recipes_by_difficulty
按烹饪难度筛选菜谱。

**参数**:
- `difficulty` (integer): 烹饪难度等级 (1-5星)

**返回**: 指定难度等级的菜谱列表

#### 6. search_recipes_by_time
按制作时间筛选菜谱。

**参数**:
- `max_time_minutes` (integer): 最大制作时间（分钟）

**返回**: 在指定时间内能完成的菜谱列表

#### 7. search_recipes_by_cuisine
按菜系搜索菜谱。

**参数**:
- `cuisine_type` (string): 菜系类型（川菜、粤菜等）

**返回**: 指定菜系的菜谱列表

#### 8. search_recipes_by_tags
按标签搜索菜谱。

**参数**:
- `tags` (array): 标签列表

**返回**: 包含指定标签的菜谱列表

#### 9. get_seasonal_recommendations
获取季节性菜谱推荐。

**参数**:
- `season` (string): 季节 (spring/summer/autumn/winter/current)

**返回**: 适合该季节的菜谱推荐

### 🛠️ 实用辅助功能 (2个)

#### 10. generate_shopping_list
根据菜谱生成购物清单。

**参数**:
- `recipe_names` (array): 菜谱名称列表
- `people_count` (integer): 用餐人数

**返回**: 按分类整理的购物清单

**示例**:
```json
{
  "selected_recipes": ["宫保鸡丁", "麻婆豆腐"],
  "people_count": 4,
  "shopping_list": {
    "调料香料": [...],
    "生鲜食材": [...],
    "主食干货": [...],
    "其他": [...]
  },
  "total_ingredients": 28
}
```

#### 11. get_ingredient_substitutes
获取食材的替代建议。

**参数**:
- `ingredient_name` (string): 需要替代的食材名称

**返回**: 该食材的替代方案和使用建议

### 📊 营养分析功能 (1个)

#### 12. analyze_recipe_nutrition
分析菜谱营养成分。

**参数**:
- `recipe_name` (string): 菜谱名称

**返回**: 菜谱的营养分析，包括卡路里、蛋白质等

**示例**:
```json
{
  "recipe_name": "宫保鸡丁的做法",
  "servings": 2,
  "total_nutrition": {
    "calories": 449.5,
    "protein_g": 28.3,
    "fat_g": 15.2,
    "carbs_g": 45.1
  },
  "per_serving_nutrition": {...}
}
```

### 🤖 智能推荐功能 (2个)

#### 13. what_to_eat
根据用餐人数推荐菜品组合。

**参数**:
- `people_count` (integer): 用餐人数 (1-10)

**返回**: 推荐的菜品组合

#### 14. recommend_meals
创建一周的膳食计划。

**参数**:
- `people_count` (integer): 用餐人数 (1-10)
- `allergies` (array, 可选): 过敏原列表
- `avoid_items` (array, 可选): 忌口食材列表

**返回**: 一周的膳食计划

## 资源 (Resources)

### 1. howtocook://categories

获取所有可用的菜谱分类。

**返回**:
```json
{
  "categories": ["水产", "早餐", "荤菜", "主食"],
  "total_count": 4,
  "description": "所有可用的菜谱分类"
}
```

### 2. howtocook://stats

获取菜谱统计信息。

**返回**:
```json
{
  "total_recipes": 294,
  "categories": {
    "荤菜": 88,
    "水产": 23
  },
  "difficulty_distribution": {
    "1": 50,
    "2": 100
  }
}
```

### 3. howtocook://health

获取服务器健康状态。

**返回**:
```json
{
  "overall_status": "healthy",
  "system_info": {...},
  "data_source": {...},
  "cache_system": {...},
  "performance": {...}
}
```

## 提示模板 (Prompts)

### 1. meal_planning_assistant

专业营养师风格的膳食计划助手。

**参数**:
- `people_count` (required): 用餐人数
- `dietary_restrictions` (optional): 饮食限制
- `cuisine_preferences` (optional): 菜系偏好
- `budget_level` (optional): 预算水平

### 2. recipe_recommendation

根据场合和技能水平推荐菜谱。

**参数**:
- `occasion` (required): 用餐场合
- `cooking_time` (optional): 可用烹饪时间
- `skill_level` (optional): 烹饪技能水平

## 错误处理

所有 API 调用都包含适当的错误处理：

- **参数验证错误**: 当提供的参数不符合要求时
- **数据源错误**: 当无法获取菜谱数据时
- **网络错误**: 当远程数据源不可用时

## 性能特性

- **智能缓存**: 自动缓存菜谱数据，显著提升响应速度
- **并发控制**: 智能的并发请求管理和限流
- **性能监控**: 全面的性能指标收集和分析，每个工具都有执行时间追踪
- **健康检查**: 实时监控服务器和数据源状态
- **错误恢复**: 智能的错误处理和恢复机制
- **中间件系统**: 使用FastMCP内置中间件进行日志、计时、错误处理

## 技术特色

### 智能算法
- **模糊匹配**: 支持菜谱名称和食材的模糊搜索
- **相似度排序**: 按匹配度对搜索结果排序
- **营养估算**: 基于食材数据库的营养成分计算
- **季节识别**: 自动识别当前季节推荐时令菜谱

### 数据处理
- **食材分类**: 智能识别调料、生鲜、主食等类别
- **用量调整**: 根据人数自动调整食材用量
- **去重合并**: 购物清单中重复食材的智能合并
- **菜系识别**: 基于关键词的菜系智能识别

## 配置选项

服务器支持多种配置选项：

### 基础配置
- **服务器配置**: 主机、端口、路径设置
- **缓存设置**: TTL、启用/禁用、缓存策略
- **日志配置**: 级别、格式、输出方式

### 性能配置
- **并发控制**: 最大并发请求数、超时时间
- **推荐算法**: 人数限制、菜品比例、优先级设置
- **膳食计划**: 工作日/周末配置、营养比例

### 数据配置
- **数据源**: 菜谱数据URL、更新频率
- **营养数据**: 食材营养成分数据库
- **替代方案**: 食材替代关系配置

## 使用统计

- **总工具数**: 14个专业工具
- **搜索维度**: 6个不同的搜索和筛选方式
- **支持菜系**: 川粤鲁苏浙闽湘徽八大菜系
- **营养数据**: 覆盖常见食材的营养成分
- **替代方案**: 15种常用食材的替代建议
- **季节食材**: 四季时令食材推荐数据库