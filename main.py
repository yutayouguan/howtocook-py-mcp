#!/usr/bin/env python
"""
HowToCook Python MCP 服务器
一个菜谱助手 MCP 服务器，提供烹饪推荐和膳食计划功能
"""

import asyncio
import logging
from src.core import app, get_config

logger = logging.getLogger(__name__)


async def main():
    """MCP 服务器的主入口点"""
    try:
        config = get_config()
        server_config = config.server_config

        logger.info("启动 HowToCook MCP 服务器...")
        logger.info(f"服务器地址: {server_config.host}:{server_config.port}")
        logger.info(f"MCP路径: {server_config.path}")
        logger.info(f"日志级别: {config.logging.level}")

        # Uvicorn配置
        uvicorn_config = {
            "access_log": True,
            "use_colors": True,
            "reload": server_config.reload,
            "workers": server_config.workers,
        }

        await app.run_streamable_http_async(
            host=server_config.host,
            port=server_config.port,
            log_level=config.logging.level.lower(),
            path=server_config.path,
            uvicorn_config=uvicorn_config,
        )
    except KeyboardInterrupt:
        logger.info("服务器已停止")
    except Exception as e:
        logger.error(f"服务器启动失败: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
