#!/bin/bash
# HowToCook MCP 服务器开发模式启动脚本

# 开发模式配置
export MCP_HOST="localhost"
export MCP_PORT="8000"
export MCP_PATH="/mcp"
export LOG_LEVEL="DEBUG"
export MCP_RELOAD="true"
export MCP_WORKERS="1"

# 缓存配置（开发模式使用较短的TTL）
export CACHE_ENABLED="true"
export CACHE_TTL="300"  # 5分钟

# 性能配置
export MAX_CONCURRENT_REQUESTS="5"
export REQUEST_TIMEOUT="30"

echo "启动 HowToCook MCP 服务器 (开发模式)..."
echo "配置信息:"
echo "  主机: $MCP_HOST"
echo "  端口: $MCP_PORT"
echo "  路径: $MCP_PATH"
echo "  日志级别: $LOG_LEVEL"
echo "  重载模式: $MCP_RELOAD"
echo "  缓存TTL: $CACHE_TTL 秒"
echo ""
echo "服务器将在 http://$MCP_HOST:$MCP_PORT$MCP_PATH 启动"
echo "按 Ctrl+C 停止服务器"
echo ""

# 启动服务器
python main.py