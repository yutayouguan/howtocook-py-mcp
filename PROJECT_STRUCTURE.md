# 📁 项目结构说明

## 🏗️ 目录结构

```
howtocook-py-mcp/
├── 📁 src/                    # 源代码
│   ├── 📁 core/              # 核心应用和配置
│   ├── 📁 domain/            # 业务逻辑层
│   ├── 📁 infrastructure/    # 基础设施层
│   ├── 📁 mcp/              # MCP 工具和资源
│   └── 📁 shared/           # 共享工具和常量
├── 📁 tests/                 # 测试代码
│   ├── 📁 unit/             # 单元测试
│   └── 📁 integration/      # 集成测试
├── 📁 docs/                 # 技术文档
├── 📁 img/                  # 图片资源
├── 📄 README.md             # 项目概览
├── 📄 CHANGELOG.md          # 更新日志
├── 📄 Makefile              # 项目管理
└── ⚙️ 配置文件...
```

## 📋 文件说明

### 🔧 核心文件
- `main.py` - 主启动文件
- `server.py` - FastMCP 兼容启动文件
- `pyproject.toml` - 项目配置和依赖
- `requirements.txt` - Python 依赖列表

### 🧪 测试文件
- `tests/integration/test_server.py` - 完整功能测试
- `tests/integration/test_mcp_server.py` - MCP 协议测试
- `tests/unit/test_recipe_service.py` - 单元测试
- `example_usage.py` - 功能演示

### 🛠️ 开发工具
- `Makefile` - 项目管理命令
- `.pre-commit-config.yaml` - 代码质量检查
- `pytest.ini` - 测试配置
- `.gitignore` - Git 忽略规则

### 📚 文档文件

#### 根目录文档
- `README.md` - 项目主页和快速开始
- `CHANGELOG.md` - 版本更新记录

#### docs/ 技术文档
- `docs/README.md` - 文档中心索引
- `docs/FEATURES.md` - 功能详细说明
- `docs/DEVELOPER_GUIDE.md` - 开发者指南
- `docs/ARCHITECTURE.md` - 架构设计
- `docs/OPTIMIZATION.md` - 优化报告
- `docs/CONFIGURATION_SUMMARY.md` - 配置说明
- `docs/API.md` - API 接口文档
- `docs/DEPLOYMENT.md` - 部署指南

## 🎯 设计原则

### 📁 目录组织
- **简洁根目录**: 只保留最重要的文件
- **分类明确**: 代码、测试、文档分离
- **层次清晰**: 按功能和用途分组

### 📄 文档组织
- **用户优先**: 重要文档放在根目录
- **开发友好**: 技术文档集中在 docs/
- **易于导航**: 提供清晰的索引和链接

### 🔧 配置管理
- **标准化**: 使用标准的配置文件格式
- **自动化**: 支持自动化工具和流程
- **可扩展**: 便于添加新的配置选项

## 🚀 快速导航

### 我想...

#### 🔰 **了解项目**
→ 阅读 [`README.md`](README.md)

#### 🛠️ **开始开发**
→ 查看 [`docs/DEVELOPER_GUIDE.md`](docs/DEVELOPER_GUIDE.md)

#### 📖 **查看功能**
→ 阅读 [`docs/FEATURES.md`](docs/FEATURES.md)

#### ⚙️ **配置服务**
→ 参考 [`docs/CONFIGURATION_SUMMARY.md`](docs/CONFIGURATION_SUMMARY.md)

#### 🚀 **部署上线**
→ 查看 [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md)

---

💡 **提示**: 这个结构遵循了 Python 项目的最佳实践，便于维护和扩展。