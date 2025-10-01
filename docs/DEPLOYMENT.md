# HowToCook MCP 部署指南

## 概述

本文档提供了 HowToCook MCP 服务器的详细部署指南，包括本地开发、生产环境部署和容器化部署。

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
# 直接启动
python main.py

# 或使用 uvx（推荐）
uvx howtocook-py-mcp
```

## 生产环境部署

### 1. 系统要求

- Python 3.12+
- 内存: 最少 512MB，推荐 1GB+
- 存储: 最少 100MB
- 网络: 稳定的互联网连接

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
# 检查健康状态
curl -s http://localhost:8000/health | jq

# 查看性能指标
python -c "
import asyncio
from src.monitoring import monitor
print(asyncio.run(monitor.get_stats()))
"
```

### 3. 缓存管理

```bash
# 清理缓存
python -c "
import asyncio
from src.cache import cache
asyncio.run(cache.clear())
print('缓存已清理')
"

# 查看缓存统计
python -c "
from src.cache import cache
print(cache.get_stats())
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
python main.py

# 禁用缓存进行测试
export CACHE_ENABLED=false
python main.py
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