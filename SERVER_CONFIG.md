# HowToCook MCP 服务器配置说明

## 服务器启动配置

HowToCook MCP 服务器现在支持通过环境变量进行灵活配置。

### 基本启动

```bash
python main.py
```

### 使用启动脚本

#### 生产模式
```bash
./start_server.sh
```

#### 开发模式
```bash
./start_dev.sh
```

## 环境变量配置

### 服务器配置

| 环境变量 | 默认值 | 说明 |
|---------|--------|------|
| `MCP_HOST` | `localhost` | 服务器绑定的主机地址 |
| `MCP_PORT` | `8000` | 服务器监听端口 |
| `MCP_PATH` | `/mcp` | MCP服务路径 |
| `MCP_RELOAD` | `false` | 是否启用自动重载（开发模式） |
| `MCP_WORKERS` | `1` | Uvicorn工作进程数量 |

### 日志配置

| 环境变量 | 默认值 | 说明 |
|---------|--------|------|
| `LOG_LEVEL` | `INFO` | 日志级别 (DEBUG, INFO, WARNING, ERROR) |

### 缓存配置

| 环境变量 | 默认值 | 说明 |
|---------|--------|------|
| `CACHE_ENABLED` | `true` | 是否启用缓存 |
| `CACHE_TTL` | `3600` | 缓存过期时间（秒） |

### 性能配置

| 环境变量 | 默认值 | 说明 |
|---------|--------|------|
| `MAX_CONCURRENT_REQUESTS` | `10` | 最大并发请求数 |
| `REQUEST_TIMEOUT` | `30` | 请求超时时间（秒） |

## 配置示例

### 1. 生产环境配置

```bash
export MCP_HOST="0.0.0.0"
export MCP_PORT="8080"
export LOG_LEVEL="WARNING"
export CACHE_TTL="7200"
export MAX_CONCURRENT_REQUESTS="20"
python main.py
```

### 2. 开发环境配置

```bash
export MCP_HOST="localhost"
export MCP_PORT="3000"
export LOG_LEVEL="DEBUG"
export MCP_RELOAD="true"
export CACHE_TTL="300"
python main.py
```

### 3. 使用 .env 文件

创建 `.env` 文件：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
MCP_HOST=localhost
MCP_PORT=8000
LOG_LEVEL=INFO
CACHE_ENABLED=true
CACHE_TTL=3600
```

然后使用 `python-dotenv` 加载：

```bash
pip install python-dotenv
```

## run_streamable_http_async 参数说明

服务器使用 FastMCP 的 `run_streamable_http_async` 方法启动，支持以下参数：

- **host**: 服务器绑定的主机地址
- **port**: 服务器监听端口
- **log_level**: 日志级别
- **path**: MCP服务路径
- **uvicorn_config**: Uvicorn配置字典
  - `access_log`: 是否启用访问日志
  - `use_colors`: 是否使用彩色日志
  - `reload`: 是否启用自动重载
  - `workers`: 工作进程数量

## 配置验证

启动服务器时，会显示当前配置信息：

```
启动 HowToCook MCP 服务器...
服务器地址: localhost:8000
MCP路径: /mcp
日志级别: INFO
```

## 故障排除

### 端口被占用
如果端口被占用，修改 `MCP_PORT` 环境变量：

```bash
export MCP_PORT=8001
python main.py
```

### 权限问题
如果需要绑定到特权端口（< 1024），需要管理员权限：

```bash
sudo MCP_PORT=80 python main.py
```

### 性能调优
对于高负载环境，可以调整以下参数：

```bash
export MCP_WORKERS=4
export MAX_CONCURRENT_REQUESTS=50
export CACHE_TTL=7200
```

## 监控和健康检查

服务器提供健康检查端点：

- 健康状态: `GET http://localhost:8000/mcp/health`
- 服务器信息: `GET http://localhost:8000/mcp/info`

可以通过这些端点监控服务器状态和性能指标。