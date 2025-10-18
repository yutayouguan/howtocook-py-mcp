# HowToCook MCP 部署指南

## 概述

本文档提供了 HowToCook MCP 服务器的详细部署指南，包括本地开发、生产环境部署和容器化部署。

**项目特色**:
- 🍳 **14个专业工具**: 覆盖完整烹饪流程
- 🔍 **6维度搜索**: 食材、难度、时间、菜系、标签、季节
- 📊 **营养分析**: 智能营养成分计算
- 🛒 **购物助手**: 自动生成分类购物清单
- 🧪 **企业级质量**: 80%+ 测试覆盖率，完整的代码质量保证

## 本地开发部署

### 1. 环境准备

```bash
# 克隆项目
git clone https://github.com/yutayouguan/howtocook-py-mcp.git
cd howtocook-py-mcp

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件：

```bash
# 缓存配置
CACHE_ENABLED=true
CACHE_TTL=3600

# 日志配置
LOG_LEVEL=INFO

# 性能配置
MAX_CONCURRENT_REQUESTS=10
REQUEST_TIMEOUT=30
```

### 3. 启动服务

```bash
# 使用 Makefile（推荐）
make run

# 直接启动
python main.py

# 使用 FastMCP CLI
fastmcp run server.py

# 开发模式
make dev-server
# 或
fastmcp dev server.py
```

### 4. 验证部署

```bash
# 检查服务器配置
make inspect
# 或
fastmcp inspect server.py

# 运行测试套件
make test
# 或
python tests/integration/test_server.py

# 运行功能演示
python example_usage.py
```

## 生产环境部署

### 1. 系统要求

- **Python**: 3.12+ (必需)
- **内存**: 最少 512MB，推荐 1GB+ (支持14个工具和缓存)
- **存储**: 最少 200MB (包含依赖和缓存)
- **网络**: 稳定的互联网连接 (获取菜谱数据)
- **CPU**: 单核即可，多核可提升并发性能

#### 依赖要求

**核心依赖**:
- fastmcp>=2.12.4
- httpx>=0.28.1  
- pydantic>=2.7.2

**开发依赖** (可选):
- pytest>=7.0.0 (测试)
- black>=23.0.0 (代码格式化)
- isort>=5.12.0 (导入排序)
- mypy>=1.0.0 (类型检查)

### 2. 安全配置

```bash
# 设置生产环境变量
export PYTHONPATH=/path/to/howtocook-py-mcp
export LOG_LEVEL=WARNING
export CACHE_ENABLED=true
export MAX_CONCURRENT_REQUESTS=50
```

### 3. 进程管理

使用 systemd 管理服务：

```ini
# /etc/systemd/system/howtocook-mcp.service
[Unit]
Description=HowToCook MCP Server
After=network.target

[Service]
Type=simple
User=mcp
WorkingDirectory=/opt/howtocook-py-mcp
Environment=PYTHONPATH=/opt/howtocook-py-mcp
Environment=LOG_LEVEL=INFO
Environment=CACHE_ENABLED=true
ExecStart=/opt/howtocook-py-mcp/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl enable howtocook-mcp
sudo systemctl start howtocook-mcp
sudo systemctl status howtocook-mcp
```

## 容器化部署

### 1. Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 设置环境变量
ENV PYTHONPATH=/app
ENV LOG_LEVEL=INFO
ENV CACHE_ENABLED=true

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import asyncio; from src.health import health_checker; print(asyncio.run(health_checker.check_data_source()))"

# 暴露端口（如果需要）
EXPOSE 8000

# 启动命令
CMD ["python", "main.py"]
```

### 2. Docker Compose

```yaml
version: '3.8'

services:
  howtocook-mcp:
    build: .
    container_name: howtocook-mcp
    restart: unless-stopped
    environment:
      - LOG_LEVEL=INFO
      - CACHE_ENABLED=true
      - CACHE_TTL=3600
      - MAX_CONCURRENT_REQUESTS=20
    volumes:
      - ./logs:/app/logs
    healthcheck:
      test: ["CMD", "python", "-c", "import asyncio; from src.health import health_checker; asyncio.run(health_checker.check_data_source())"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

构建和运行：

```bash
# 构建镜像
docker build -t howtocook-mcp .

# 运行容器
docker run -d --name howtocook-mcp \
  -e LOG_LEVEL=INFO \
  -e CACHE_ENABLED=true \
  howtocook-mcp

# 或使用 docker-compose
docker-compose up -d
```

## 监控和维护

### 1. 日志管理

```bash
# 查看日志
tail -f /var/log/howtocook-mcp.log

# 或使用 journalctl
journalctl -u howtocook-mcp -f

# Docker 日志
docker logs -f howtocook-mcp
```

### 2. 性能监控

```bash
# 检查服务器配置和状态
make inspect
fastmcp inspect server.py

# 运行完整测试套件（包含性能测试）
make test
python tests/integration/test_server.py

# 查看缓存统计
python -c "
from src.infrastructure.cache import get_cache
cache = get_cache()
print(cache.get_stats())
"

# 检查健康状态（如果使用HTTP传输）
curl -s http://localhost:8000/mcp/health | jq
```

### 3. 缓存管理

```bash
# 清理缓存
python -c "
import asyncio
from src.infrastructure.cache import get_cache
cache = get_cache()
asyncio.run(cache.clear())
print('缓存已清理')
"

# 查看缓存统计
python -c "
from src.infrastructure.cache import get_cache
cache = get_cache()
print(cache.get_stats())
"

# 测试缓存功能
python -c "
import asyncio
from src.infrastructure.cache import get_cache
async def test_cache():
    cache = get_cache()
    await cache.set('test', 'value', 60)
    result = await cache.get('test')
    print(f'缓存测试: {result}')
asyncio.run(test_cache())
"
```

## 故障排除

### 常见问题

1. **数据源连接失败**
   - 检查网络连接
   - 验证 RECIPES_URL 是否可访问
   - 查看错误日志

2. **内存使用过高**
   - 调整缓存 TTL
   - 减少 MAX_CONCURRENT_REQUESTS
   - 定期清理缓存

3. **响应时间过长**
   - 启用缓存系统
   - 检查网络延迟
   - 优化并发设置

### 调试模式

```bash
# 启用调试日志
export LOG_LEVEL=DEBUG
make run

# 禁用缓存进行测试
export CACHE_ENABLED=false
python main.py

# 使用开发模式（自动重载）
make dev-server

# 运行代码质量检查
make lint

# 运行代码格式化
make format

# 清理缓存文件
make clean
```

## 安全建议

1. **网络安全**
   - 使用防火墙限制访问
   - 配置 HTTPS（如果需要）
   - 定期更新依赖

2. **访问控制**
   - 限制服务器访问权限
   - 使用专用用户运行服务
   - 定期审查日志

3. **数据安全**
   - 定期备份配置
   - 监控异常访问
   - 保护敏感配置信息

## 扩展部署

### 负载均衡

```nginx
# Nginx 配置示例
upstream howtocook_mcp {
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
}

server {
    listen 80;
    server_name howtocook-mcp.example.com;
    
    location / {
        proxy_pass http://howtocook_mcp;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 集群部署

使用 Kubernetes 进行集群部署：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: howtocook-mcp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: howtocook-mcp
  template:
    metadata:
      labels:
        app: howtocook-mcp
    spec:
      containers:
      - name: howtocook-mcp
        image: howtocook-mcp:latest
        ports:
        - containerPort: 8000
        env:
        - name: LOG_LEVEL
          value: "INFO"
        - name: CACHE_ENABLED
          value: "true"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```
## 功能验证


### 验证14个工具

部署完成后，可以验证所有14个工具是否正常工作：

```bash
# 运行完整功能测试
python tests/integration/test_server.py

# 运行MCP协议测试
python tests/integration/test_mcp_server.py

# 运行功能演示
python example_usage.py

# 检查工具数量
fastmcp inspect server.py | grep "Tools:"
# 应该显示: Tools: 14
```

### 功能分类测试

```bash
# 测试基础菜谱功能
python -c "
import asyncio
from src.domain.services import RecipeService
async def test():
    service = RecipeService()
    # 测试获取所有菜谱
    result = await service.get_all_recipes()
    print('✅ 基础功能正常')
asyncio.run(test())
"

# 测试智能搜索功能
python -c "
import asyncio
from src.domain.services import RecipeService
async def test():
    service = RecipeService()
    # 测试按食材搜索
    result = await service.search_recipes_by_ingredients(['鸡肉'])
    print('✅ 搜索功能正常')
asyncio.run(test())
"

# 测试营养分析功能
python -c "
import asyncio
from src.domain.services import RecipeService
async def test():
    service = RecipeService()
    # 测试营养分析
    result = await service.analyze_recipe_nutrition('宫保鸡丁')
    print('✅ 营养分析正常')
asyncio.run(test())
"
```

## 性能优化建议

### 生产环境优化

1. **缓存配置**
   ```bash
   export CACHE_ENABLED=true
   export CACHE_TTL=7200  # 2小时缓存
   ```

2. **并发设置**
   ```bash
   export MAX_CONCURRENT_REQUESTS=50
   export REQUEST_TIMEOUT=60
   ```

3. **日志级别**
   ```bash
   export LOG_LEVEL=WARNING  # 生产环境减少日志
   ```

### 监控指标

关键监控指标：
- **工具调用成功率**: 应该 > 95%
- **平均响应时间**: 应该 < 2秒
- **缓存命中率**: 应该 > 80%
- **内存使用**: 应该 < 1GB
- **数据源可用性**: 应该 > 99%

### 扩展建议

1. **水平扩展**: 可以运行多个实例进行负载均衡
2. **缓存优化**: 考虑使用 Redis 替代内存缓存
3. **数据源**: 可以配置本地数据源提高可靠性
4. **监控**: 集成 Prometheus + Grafana 进行监控

## 版本升级

### 升级步骤

1. **备份配置**
   ```bash
   cp .env .env.backup
   cp -r logs logs.backup
   ```

2. **更新代码**
   ```bash
   git pull origin main
   pip install -r requirements.txt
   ```

3. **运行测试**
   ```bash
   make test
   ```

4. **重启服务**
   ```bash
   sudo systemctl restart howtocook-mcp
   ```

### 版本兼容性

- **v0.2.0**: 当前版本，14个工具，完整功能
- **v0.1.0**: 旧版本，4个工具，基础功能

升级到 v0.2.0 的主要变化：
- 工具数量从 4个 增加到 14个
- 新增 6维度智能搜索
- 新增营养分析功能
- 新增购物清单生成
- 完善的测试和质量保证体系

---

💡 **部署提示**: 建议先在测试环境验证所有功能正常后再部署到生产环境。