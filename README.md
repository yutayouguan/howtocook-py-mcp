# 🍳 HowToCook-py-MCP 🥘 -- 炫一周好饭，拒绝拼好饭

[English](./README_EN.md) | 简体中文

> 让 AI 助手变身私人大厨，为你的一日三餐出谋划策！

这是一个Python版的菜谱助手MCP服务，使用FastMCP库实现。基于[Anduin2017/HowToCook](https://github.com/Anduin2017/HowToCook)打造，让 AI 助手能够为你推荐菜谱、规划膳食，解决"今天吃什么"的世纪难题！

特别感谢[worryzyy/HowToCook-mcp](https://github.com/worryzyy/HowToCook-mcp)，这个Python版本是从那边模仿过来的😄！

## 📸 效果预览

![功能预览1](img/01.png)

## 🔌 支持的 MCP 客户端

本服务器已在以下客户端测试通过:

- 📝 Cursor

## ✨ 美味功能

该 MCP 服务器提供以下功能:

### 🔧 工具 (Tools)
1. **📚 获取所有菜谱** (`get_all_recipes`) - 返回所有可用菜谱的简化版数据，支持进度报告和性能监控
2. **🔍 按分类获取菜谱** (`get_recipes_by_category`) - 根据指定的分类查询菜谱，想吃水产？早餐？荤菜？主食？一键搞定！
3. **🎲 不知道吃什么** (`what_to_eat`) - 选择困难症福音！根据人数直接推荐今日菜单，再也不用纠结了
4. **🧩 推荐膳食计划** (`recommend_meals`) - 根据你的忌口、过敏原和用餐人数，为你规划整整一周的美味佳肴，支持进度跟踪

### 📊 资源 (Resources)
1. **📋 菜谱分类** (`howtocook://categories`) - 获取所有可用的菜谱分类列表
2. **📈 统计信息** (`howtocook://stats`) - 查看菜谱数据的统计信息，包括分类分布和难度分析
3. **🏥 健康检查** (`howtocook://health`) - 获取服务器健康状态、性能指标和系统信息

### 💬 提示模板 (Prompts)
1. **🍽️ 膳食计划助手** (`meal_planning_assistant`) - 专业营养师风格的膳食计划提示模板
2. **👨‍🍳 菜谱推荐** (`recipe_recommendation`) - 根据场合和技能水平推荐菜谱的提示模板

### 🛡️ 企业级特性
- **智能缓存**: 自动缓存菜谱数据，显著提升响应速度
- **实时日志**: 详细的操作日志和错误信息，支持多级别日志
- **进度跟踪**: 长时间操作的实时进度报告
- **性能监控**: 全面的性能指标收集和分析
- **健康检查**: 实时监控服务器和数据源状态
- **错误处理**: 智能的错误处理和恢复机制
- **配置管理**: 灵活的配置系统，支持环境变量
- **并发控制**: 智能的并发请求管理和限流

## 🚀 快速上手

### 📋 先决条件

- Python 3.12+ 🐍
- FastMCP 2.12.4+ 📦
- 稳定的网络连接（用于获取菜谱数据）

### 💻 安装步骤

1. 克隆美食仓库

```bash
git clone https://github.com/yutayouguan/howtocook-py-mcp.git
cd howtocook-py-mcp
```

2. 安装依赖（就像准备食材一样简单！）

```bash
pip install -r requirements.txt
```

### ❓ 为什么不用uv

你每天都忘记上千件事，为什么不把这件也忘了？

## 🍽️ 开始使用

### 🔥 启动服务器

```bash
# 确保在项目根目录下运行
python main.py
```

服务将通过标准输入输出(stdio)协议运行，符合FastMCP最佳实践。

### 🔧 配置 MCP 客户端

#### 使用 Cursor 快速体验

在 Cursor 设置中添加 MCP 服务器配置：

```json
{
  "mcpServers": {
    "howtocook-py-mcp": {
      "command": "python",
      "args": ["main.py"],
      "cwd": "/path/to/howtocook-py-mcp"
    }
  }
}
```

请将 `/path/to/howtocook-py-mcp` 替换为你的项目实际路径。

#### 其他 MCP 客户端

对于其他支持 MCP 协议的客户端，请参考各自的文档进行配置。

## 🧙‍♂️ 菜单魔法使用指南

以下是在各种 MCP 客户端中使用的示例提示语：

### 1. 📚 获取所有菜谱

无需参数，直接召唤美食全书！

```
请使用howtocook-py-mcp的MCP服务查询所有菜谱
```

### 2. 🔍 按分类获取菜谱

```
请使用howtocook-py-mcp的MCP服务查询水产类的菜谱
```

参数:

- `category`: 菜谱分类（水产、早餐、荤菜、主食等）

### 3. 🎲 不知道吃什么？

```
请使用howtocook-py-mcp的MCP服务为4人晚餐推荐菜单
```

参数:

- `people_count`: 用餐人数 (1-10)

### 4. 🧩 推荐膳食计划

```
请使用howtocook-py-mcp的MCP服务为3人推荐一周菜谱，我们家不吃香菜，对虾过敏
```

参数:

- `allergies`: 过敏原列表，如 ["大蒜", "虾"]
- `avoid_items`: 忌口食材，如 ["葱", "姜"]
- `people_count`: 用餐人数 (1-10)

## 🧪 测试服务器

运行完整的测试套件来验证所有功能：

```bash
python test_server.py
```

运行简单的功能示例：

```bash
python example_usage.py
```

## 📊 性能优化

### 缓存系统
- 自动缓存菜谱数据，默认缓存 1 小时
- 支持手动清理和统计查看
- 可通过环境变量 `CACHE_ENABLED` 控制

### 监控和健康检查
- 实时性能指标收集
- 自动健康状态监控
- 详细的错误日志和统计

### 配置选项
```bash
# 环境变量配置示例
export CACHE_ENABLED=true
export CACHE_TTL=3600
export LOG_LEVEL=INFO
export MAX_CONCURRENT_REQUESTS=10
```

## 📝 小贴士

- 本服务兼容所有支持 MCP 协议的 AI 助手和应用
- 首次使用时，AI 可能需要一点时间来熟悉如何使用这些工具（就像烧热锅一样）
- 使用资源功能可以快速了解可用的菜谱分类和统计信息
- 提示模板可以帮助 AI 更好地理解如何使用这些工具
- 健康检查资源可以实时监控服务器状态
- 缓存系统会自动优化重复请求的性能

## 📄 数据来源

菜谱数据来自远程JSON文件，URL：
`https://mp-bc8d1f0a-3356-4a4e-8592-f73a3371baa2.cdn.bspapp.com/all_recipes.json`

## 🤝 贡献

欢迎 Fork 和 Pull Request，让我们一起完善这个美食助手！

## 📄 许可

MIT License - 随意使用，就像分享美食配方一样慷慨！

---

> 🍴 美食即将开始，胃口准备好了吗？
