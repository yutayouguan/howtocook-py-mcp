"""
健康检查器实现
"""

import time
import asyncio
from typing import Dict, Any
from ...domain.repositories import RecipeRepository
from ...infrastructure.cache import get_cache
from ...core.config import get_config
from .performance_monitor import get_monitor


class HealthChecker:
    """健康检查器"""

    def __init__(self):
        """初始化健康检查器"""
        self.start_time = time.time()
        self.recipe_repo = RecipeRepository()

    async def check_data_source(self) -> Dict[str, Any]:
        """
        检查数据源健康状态

        Returns:
            Dict[str, Any]: 数据源健康状态
        """
        try:
            start_time = time.time()
            recipes = await self.recipe_repo.fetch_all_recipes()
            response_time = time.time() - start_time

            return {
                "status": "healthy" if recipes else "unhealthy",
                "recipe_count": len(recipes),
                "response_time": response_time,
                "error": None,
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "recipe_count": 0,
                "response_time": 0,
                "error": str(e),
            }

    async def check_cache_system(self) -> Dict[str, Any]:
        """
        检查缓存系统健康状态

        Returns:
            Dict[str, Any]: 缓存系统健康状态
        """
        try:
            cache = get_cache()
            # 测试缓存读写
            test_key = "health_check_test"
            test_value = f"test_{time.time()}"

            await cache.set(test_key, test_value, 60)
            cached_value = await cache.get(test_key)
            await cache.delete(test_key)

            cache_stats = cache.get_stats()

            return {
                "status": "healthy" if cached_value == test_value else "unhealthy",
                "enabled": cache_stats.get("enabled", False),
                "total_items": cache_stats.get("total_items", 0),
                "error": None,
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "enabled": False,
                "total_items": 0,
                "error": str(e),
            }

    async def get_performance_summary(self) -> Dict[str, Any]:
        """
        获取性能摘要

        Returns:
            Dict[str, Any]: 性能摘要信息
        """
        try:
            monitor = get_monitor()
            stats = await monitor.get_stats()

            # 计算总体统计
            total_requests = sum(stat.get("count", 0) for stat in stats.values())
            avg_success_rate = (
                sum(stat.get("success_rate", 0) for stat in stats.values()) / len(stats)
                if stats
                else 0
            )

            return {
                "total_requests": total_requests,
                "avg_success_rate": avg_success_rate,
                "monitored_functions": list(stats.keys()),
                "detailed_stats": stats,
            }
        except Exception as e:
            return {"error": str(e)}

    async def get_system_info(self) -> Dict[str, Any]:
        """
        获取系统信息

        Returns:
            Dict[str, Any]: 系统信息
        """
        config = get_config()
        uptime = time.time() - self.start_time

        return {
            "server_name": config.server.name,
            "server_version": config.server.version,
            "uptime_seconds": uptime,
            "uptime_formatted": self._format_uptime(uptime),
            "configuration": {
                "cache_enabled": config.cache.enabled,
                "max_concurrent_requests": config.performance.max_concurrent_requests,
                "request_timeout": config.performance.request_timeout,
            },
        }

    def _format_uptime(self, uptime_seconds: float) -> str:
        """
        格式化运行时间

        Args:
            uptime_seconds: 运行时间（秒）

        Returns:
            str: 格式化的运行时间
        """
        hours = int(uptime_seconds // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        seconds = int(uptime_seconds % 60)

        return f"{hours}小时 {minutes}分钟 {seconds}秒"

    async def full_health_check(self) -> Dict[str, Any]:
        """
        执行完整的健康检查

        Returns:
            Dict[str, Any]: 完整的健康检查结果
        """
        # 并行执行各项检查
        (
            data_source_check,
            cache_check,
            performance_summary,
            system_info,
        ) = await asyncio.gather(
            self.check_data_source(),
            self.check_cache_system(),
            self.get_performance_summary(),
            self.get_system_info(),
            return_exceptions=True,
        )

        # 计算总体健康状态
        overall_status = "healthy"
        if (
            isinstance(data_source_check, dict)
            and data_source_check.get("status") != "healthy"
        ) or (isinstance(cache_check, dict) and cache_check.get("status") != "healthy"):
            overall_status = "degraded"

        if isinstance(data_source_check, Exception) or isinstance(
            cache_check, Exception
        ):
            overall_status = "unhealthy"

        return {
            "timestamp": time.time(),
            "overall_status": overall_status,
            "system_info": system_info
            if not isinstance(system_info, Exception)
            else {"error": str(system_info)},
            "data_source": data_source_check
            if not isinstance(data_source_check, Exception)
            else {"error": str(data_source_check)},
            "cache_system": cache_check
            if not isinstance(cache_check, Exception)
            else {"error": str(cache_check)},
            "performance": performance_summary
            if not isinstance(performance_summary, Exception)
            else {"error": str(performance_summary)},
        }


# 全局健康检查器实例
_health_checker = HealthChecker()


def get_health_checker() -> HealthChecker:
    """获取全局健康检查器实例"""
    return _health_checker
