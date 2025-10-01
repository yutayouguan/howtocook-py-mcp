#!/bin/bash
# HowToCook MCP 服务器启动脚本

# 设置环境变量
export MCP_HOST=${MCP_HOST:-"0.0.0.0"}
export MCP_PORT=${MCP_PORT:-"8000"}
export MCP_PATH=${MCP_PATH:-"/mcp"}
export LOG_LEVEL=${LOG_LEVEL:-"INFO"}
export MCP_RELOAD=${MCP_RELOAD:-"false"}
export MCP_WORKERS=${MCP_WORKERS:-"1"}

# 缓存配置
export CACHE_ENABLED=${CACHE_ENABLED:-"true"}
export CACHE_TTL=${CACHE_TTL:-"3600"}

# 性能配置
export MAX_CONCURRENT_REQUESTS=${MAX_CONCURRENT_REQUESTS:-"10"}
export REQUEST_TIMEOUT=${REQUEST_TIMEOUT:-"30"}

echo "启动 HowToCook MCP 服务器..."
echo "配置信息:"
echo "  主机: $MCP_HOST"
echo "  端口: $MCP_PORT"
echo "  路径: $MCP_PATH"
echo "  日志级别: $LOG_LEVEL"
echo "  重载模式: $MCP_RELOAD"
echo "  工作进程: $MCP_WORKERS"
echo "  缓存启用: $CACHE_ENABLED"
echo ""

# 启动服务器
python main.py