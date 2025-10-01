"""
错误处理中间件实现
"""

import logging
from typing import Any, Callable, Awaitable
from fastmcp.server.middleware import Middleware
from fastmcp.server.context import Context

logger = logging.getLogger(__name__)


class ErrorHandlingMiddleware(Middleware):
    """集中错误处理的中间件"""

    async def __call__(
        self, request: Any, call_next: Callable[[Any], Awaitable[Any]], ctx: Context
    ) -> Any:
        try:
            return await call_next(request)
        except ValueError as e:
            await ctx.log_error(f"参数错误: {str(e)}")
            raise
        except ConnectionError as e:
            await ctx.log_error(f"网络连接错误: {str(e)}")
            raise
        except Exception as e:
            await ctx.log_error(f"未知错误: {str(e)}")
            logger.exception("Unexpected error in middleware")
            raise
