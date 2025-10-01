# HowToCook MCP API 文档

## 概述

HowToCook MCP 服务器提供了一套完整的菜谱管理和膳食计划 API，基于 FastMCP 框架构建。

## 工具 (Tools)

### 1. get_all_recipes

获取所有菜谱的简化信息。

**参数**: 无

**返回**: JSON 格式的菜谱列表，包含名称和描述

**示例**:
```json
[
  {
    "name": "宫保鸡丁",
    "description": "经典川菜，酸甜可口"
  }
]
```

### 2. get_recipes_by_category

根据分类查询菜谱。

**参数**:
- `category` (string): 菜谱分类名称

**返回**: 该分类下所有菜谱的详细信息

**示例**:
```json
[
  {
    "id": "recipe_001",
    "name": "红烧鱼",
    "description": "鲜美的红烧鱼",
    "ingredients": [
      {
        "name": "鱼",
        "text_quantity": "1条"
      }
    ]
  }
]
```

### 3. what_to_eat

根据用餐人数推荐菜品组合。

**参数**:
- `people_count` (integer): 用餐人数 (1-10)

**返回**: 推荐的菜品组合

**示例**:
```json
{
  "people_count": 4,
  "meat_dish_count": 2,
  "vegetable_dish_count": 2,
  "dishes": [...],
  "message": "为4人推荐的菜品，包含2个荤菜和2个素菜。"
}
```

### 4. recommend_meals

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

- **缓存系统**: 自动缓存菜谱数据，提高响应速度
- **进度跟踪**: 长时间操作提供实时进度更新
- **性能监控**: 自动记录和分析 API 性能指标
- **健康检查**: 实时监控服务器和数据源状态

## 配置选项

服务器支持多种配置选项：

- 缓存设置 (TTL, 启用/禁用)
- 性能限制 (并发请求数, 超时时间)
- 推荐算法参数
- 日志级别和格式