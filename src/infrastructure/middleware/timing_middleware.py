"""
计时中间件实现
"""

import time
from typing import Any, Callable, Awaitable
from fastmcp.server.middleware import Middleware
from fastmcp.server.context import Context


class TimingMiddleware(Middleware):
    """记录工具执行时间的中间件"""

    async def __call__(
        self, request: Any, call_next: Callable[[Any], Awaitable[Any]], ctx: Context
    ) -> Any:
        start_time = time.time()

        try:
            response = await call_next(request)
            execution_time = time.time() - start_time

            if hasattr(request, "method") and request.method == "tools/call":
                tool_name = getattr(request.params, "name", "unknown")
                await ctx.log_info(
                    f"工具 '{tool_name}' 执行完成，耗时 {execution_time:.2f} 秒"
                )

            return response

        except Exception as e:
            execution_time = time.time() - start_time
            await ctx.log_error(f"请求执行失败，耗时 {execution_time:.2f} 秒: {str(e)}")
            raise
