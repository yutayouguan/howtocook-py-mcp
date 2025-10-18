# 🛠️ HowToCook MCP 开发者指南

## 🚀 快速开始

### 环境准备
```bash
# 克隆项目
git clone https://github.com/yutayouguan/howtocook-py-mcp.git
cd howtocook-py-mcp

# 安装开发环境
make dev

# 验证安装
make test
```

### 项目结构
```
howtocook-py-mcp/
├── src/                    # 源代码
│   ├── core/              # 核心应用和配置
│   ├── domain/            # 业务逻辑层
│   ├── infrastructure/    # 基础设施层
│   ├── mcp/              # MCP 工具和资源
│   └── shared/           # 共享工具和常量
├── tests/                 # 测试代码
│   ├── unit/             # 单元测试
│   └── integration/      # 集成测试
├── docs/                 # 文档
└── 配置文件...
```

## 🔧 开发工作流

### 1. 代码开发
```bash
# 创建功能分支
git checkout -b feature/new-tool

# 开发代码...

# 格式化代码
make format

# 检查代码质量
make lint

# 运行测试
make test
```

### 2. 提交代码
```bash
# pre-commit hooks 会自动运行检查
git add .
git commit -m "feat: add new recipe tool"

# 推送到远程
git push origin feature/new-tool
```

### 3. 测试验证
```bash
# 运行完整测试套件
python test_server.py

# 运行功能演示
python example_usage.py

# 检查服务器配置
make inspect
```

## 🏗️ 架构设计

### 分层架构
```
┌─────────────────┐
│   MCP Layer     │  ← 工具、资源、提示
├─────────────────┤
│  Domain Layer   │  ← 业务逻辑、服务
├─────────────────┤
│Infrastructure   │  ← 缓存、监控、中间件
├─────────────────┤
│   Core Layer    │  ← 应用配置、启动
└─────────────────┘
```

### 核心组件

#### 1. MCP 工具 (`src/mcp/tools/`)
```python
@server.tool()
async def new_tool(param: str) -> str:
    """新工具描述"""
    service = SomeService()
    return await service.process(param)
```

#### 2. 业务服务 (`src/domain/services/`)
```python
class NewService:
    @performance_tracked("method_name")
    async def process(self, param: str) -> str:
        # 业务逻辑实现
        return result
```

#### 3. 数据模型 (`src/domain/models/`)
```python
class NewModel(BaseModel):
    field1: str
    field2: int
    field3: Optional[List[str]] = None
```

## 🧪 测试指南

### 单元测试
```python
# tests/unit/test_new_service.py
import pytest
from src.domain.services import NewService

class TestNewService:
    @pytest.mark.asyncio
    async def test_process_success(self):
        service = NewService()
        result = await service.process("test")
        assert result == "expected"
```

### 集成测试
```python
# 在 test_server.py 中添加
async def test_new_tool():
    service = NewService()
    result = await service.process("test")
    print(f"✅ 新工具测试: {result}")
```

### 测试最佳实践
- 使用 `pytest.mark.asyncio` 标记异步测试
- 使用 `unittest.mock` 模拟外部依赖
- 测试正常流程和异常情况
- 保持测试独立和可重复

## 📊 性能优化

### 缓存策略
```python
from ...infrastructure.cache import cached

@cached(ttl=3600)  # 缓存1小时
async def expensive_operation():
    # 耗时操作
    return result
```

### 性能监控
```python
from ...infrastructure.monitoring.performance_monitor import performance_tracked

@performance_tracked("operation_name")
async def monitored_operation():
    # 被监控的操作
    return result
```

### 优化建议
- 使用缓存减少重复计算
- 异步处理提高并发性能
- 合理设置超时和重试
- 监控关键指标

## 🔍 代码质量

### 代码风格
```python
# 使用 Black 格式化
# 行长度: 88 字符
# 字符串引号: 双引号优先

def function_name(param1: str, param2: int) -> str:
    """函数文档字符串"""
    result = f"处理 {param1} 和 {param2}"
    return result
```

### 类型注解
```python
from typing import List, Optional, Dict, Any

async def typed_function(
    items: List[str],
    config: Optional[Dict[str, Any]] = None
) -> Dict[str, int]:
    """完整的类型注解"""
    return {"count": len(items)}
```

### 错误处理
```python
try:
    result = await risky_operation()
except (ValueError, TypeError) as e:
    logger.error(f"参数错误: {e}")
    raise
except Exception as e:
    logger.error(f"未知错误: {e}")
    raise
```

## 🔧 工具配置

### Black 配置 (`pyproject.toml`)
```toml
[tool.black]
line-length = 88
target-version = ['py312']
```

### isort 配置
```toml
[tool.isort]
profile = "black"
line_length = 88
```

### mypy 配置
```toml
[tool.mypy]
python_version = "3.12"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

### pytest 配置 (`pytest.ini`)
```ini
[tool:pytest]
testpaths = tests
addopts = -v --tb=short --asyncio-mode=auto
```

## 📝 文档规范

### 代码文档
```python
async def example_function(param: str) -> Dict[str, Any]:
    """
    函数简短描述
    
    Args:
        param: 参数描述
        
    Returns:
        返回值描述
        
    Raises:
        ValueError: 参数无效时抛出
    """
```

### API 文档
- 使用 docstring 描述工具功能
- 提供清晰的参数说明
- 包含使用示例
- 说明返回格式

## 🚀 部署指南

### 本地开发
```bash
# 启动开发服务器
make dev-server

# 或使用 FastMCP CLI
fastmcp dev server.py
```

### 生产部署
```bash
# 构建项目
make build

# 启动生产服务器
make run

# 或使用 FastMCP CLI
fastmcp run server.py --transport http --port 8000
```

### 环境变量
```bash
# .env 文件
MCP_HOST=localhost
MCP_PORT=8000
LOG_LEVEL=INFO
CACHE_ENABLED=true
CACHE_TTL=3600
```

## 🤝 贡献指南

### 提交规范
```
feat: 新功能
fix: 修复问题
docs: 文档更新
style: 代码格式
refactor: 重构
test: 测试相关
chore: 构建/工具相关
```

### Pull Request 流程
1. Fork 项目
2. 创建功能分支
3. 开发和测试
4. 提交 PR
5. 代码审查
6. 合并主分支

### 代码审查要点
- 功能完整性和正确性
- 代码质量和风格
- 测试覆盖率
- 文档完整性
- 性能影响

## 📚 学习资源

### 相关技术
- [FastMCP 文档](https://gofastmcp.com)
- [Pydantic 文档](https://docs.pydantic.dev)
- [pytest 文档](https://docs.pytest.org)
- [Black 文档](https://black.readthedocs.io)

### 项目文档
- [功能说明](FEATURES.md)
- [架构设计](ARCHITECTURE.md)
- [优化报告](OPTIMIZATION.md)
- [更新日志](CHANGELOG.md)

---

💡 **开发愉快！如有问题，请查看文档或提交 Issue。**