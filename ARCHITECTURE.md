# HowToCook MCP 服务器 - 新架构说明

## 项目重构概述

本项目已完全重新组织，采用了清晰的分层架构，提高了代码的可维护性、可扩展性和可测试性。

## 新的目录结构

```
src/
├── core/                    # 核心业务逻辑
│   ├── __init__.py
│   ├── app.py              # 主应用入口
│   └── config.py           # 配置管理
├── domain/                  # 领域模型和业务逻辑
│   ├── __init__.py
│   ├── models/             # 数据模型
│   │   ├── __init__.py
│   │   ├── recipe.py       # 菜谱相关模型
│   │   ├── meal_plan.py    # 膳食计划模型
│   │   └── grocery.py      # 购物清单模型
│   ├── services/           # 业务服务
│   │   ├── __init__.py
│   │   ├── recipe_service.py        # 菜谱业务服务
│   │   ├── meal_service.py          # 膳食计划业务服务
│   │   └── recommendation_service.py # 推荐业务服务
│   └── repositories/       # 数据访问层
│       ├── __init__.py
│       └── recipe_repository.py     # 菜谱数据仓库
├── infrastructure/         # 基础设施层
│   ├── __init__.py
│   ├── cache/
│   │   ├── __init__.py
│   │   └── memory_cache.py          # 内存缓存实现
│   ├── monitoring/
│   │   ├── __init__.py
│   │   ├── health_checker.py        # 健康检查器
│   │   └── performance_monitor.py   # 性能监控器
│   └── middleware/
│       ├── __init__.py
│       ├── error_handler.py         # 错误处理中间件
│       └── timing_middleware.py     # 计时中间件
├── mcp/                    # MCP工具和接口
│   ├── __init__.py
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── recipe_tools.py          # 菜谱相关工具
│   │   ├── meal_tools.py            # 膳食计划工具
│   │   └── recommendation_tools.py  # 推荐工具
│   └── resources/
│       ├── __init__.py
│       └── api_resources.py         # API资源
├── ai/                     # AI相关功能
│   ├── __init__.py
│   ├── prompts/
│   │   ├── __init__.py
│   │   ├── meal_planning.py         # 膳食计划提示
│   │   └── recipe_recommendation.py # 菜谱推荐提示
│   └── processors/
│       └── __init__.py
└── shared/                 # 共享工具和常量
    ├── __init__.py
    ├── constants.py                 # 共享常量
    └── utils.py                     # 工具函数
```

## 架构层次说明

### 1. 核心层 (Core)
- **职责**: 应用程序的核心配置和入口点
- **包含**: 应用配置、主应用实例创建
- **特点**: 不依赖其他业务层，提供基础配置服务

### 2. 领域层 (Domain)
- **职责**: 业务逻辑和数据模型
- **包含**: 
  - **Models**: 数据模型定义（Recipe, MealPlan, GroceryList等）
  - **Services**: 业务服务（菜谱服务、膳食计划服务、推荐服务）
  - **Repositories**: 数据访问抽象层
- **特点**: 包含核心业务逻辑，不依赖外部框架

### 3. 基础设施层 (Infrastructure)
- **职责**: 技术实现和外部依赖
- **包含**:
  - **Cache**: 缓存实现
  - **Monitoring**: 监控和健康检查
  - **Middleware**: 中间件实现
- **特点**: 提供技术支持，可以被替换而不影响业务逻辑

### 4. MCP层 (MCP)
- **职责**: MCP协议相关的工具和资源
- **包含**:
  - **Tools**: MCP工具注册和实现
  - **Resources**: MCP资源提供
- **特点**: 专门处理MCP协议相关功能

### 5. AI层 (AI)
- **职责**: AI相关功能
- **包含**:
  - **Prompts**: 提示模板
  - **Processors**: AI响应处理器（预留）
- **特点**: 集中管理AI相关功能

### 6. 共享层 (Shared)
- **职责**: 跨层共享的工具和常量
- **包含**: 工具函数、常量定义
- **特点**: 被其他层使用，不依赖业务逻辑

## 主要改进

### 1. 清晰的职责分离
- 每个层次都有明确的职责
- 减少了模块间的耦合
- 提高了代码的可维护性

### 2. 更好的可测试性
- 业务逻辑与技术实现分离
- 依赖注入友好的设计
- 便于单元测试和集成测试

### 3. 更强的可扩展性
- 新功能可以轻松添加到相应层次
- 技术栈可以独立升级
- 支持插件化扩展

### 4. 更好的代码组织
- 相关功能聚合在一起
- 减少了文件查找时间
- 提高了开发效率

## 迁移说明

### 旧文件映射
- `src/app.py` → `src/core/app.py`
- `src/config.py` → `src/core/config.py`
- `src/types/models.py` → `src/domain/models/`
- `src/data/recipes.py` → `src/domain/repositories/recipe_repository.py`
- `src/tools/` → `src/mcp/tools/`
- `src/cache.py` → `src/infrastructure/cache/memory_cache.py`
- `src/health.py` → `src/infrastructure/monitoring/health_checker.py`
- `src/monitoring.py` → `src/infrastructure/monitoring/performance_monitor.py`
- `src/middleware.py` → `src/infrastructure/middleware/`
- `src/prompts.py` → `src/ai/prompts/`
- `src/utils/recipe_utils.py` → `src/shared/utils.py`

### 导入路径更新
所有导入路径都已更新以反映新的架构。主要入口点仍然是 `main.py`，但现在使用 `src.core.app`。

## 使用方式

### 启动服务器
```bash
python main.py
```

### 导入应用
```python
from src.core import app, get_config
```

### 扩展功能
1. 添加新的数据模型：在 `src/domain/models/` 中创建
2. 添加新的业务服务：在 `src/domain/services/` 中创建
3. 添加新的MCP工具：在 `src/mcp/tools/` 中创建
4. 添加新的基础设施：在 `src/infrastructure/` 中创建

## 配置管理

配置系统已经重构，现在使用更清晰的dataclass结构：

```python
from src.core import get_config

config = get_config()
print(config.server.name)
print(config.cache.enabled)
```

## 总结

新架构提供了：
- ✅ 清晰的分层结构
- ✅ 更好的代码组织
- ✅ 提高的可维护性
- ✅ 增强的可测试性
- ✅ 更强的可扩展性
- ✅ 向后兼容的API

这个重构为项目的长期发展奠定了坚实的基础。