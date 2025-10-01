#!/usr/bin/env python
"""
HowToCook MCP 服务器 - 独立启动文件
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.core.app import app

# 导出应用实例供 FastMCP CLI 使用
mcp = app

if __name__ == "__main__":
    import asyncio
    from src.core.config import get_config

    async def main():
        config = get_config()
        server_config = config.server_config

        print(f"启动 HowToCook MCP 服务器 v{config.server.version}")
        print(f"服务器地址: {server_config.host}:{server_config.port}")
        print(f"MCP路径: {server_config.path}")

        await app.run_http_async(
            host=server_config.host,
            port=server_config.port,
            path=server_config.path,
        )

    asyncio.run(main())
