"""
性能监控器实现
"""

import time
import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from collections import defaultdict, deque


@dataclass
class PerformanceMetric:
    """性能指标数据类"""

    name: str
    duration: float
    timestamp: float
    success: bool
    error_message: Optional[str] = None


class PerformanceMonitor:
    """性能监控器"""

    def __init__(self, max_history: int = 1000):
        """
        初始化性能监控器

        Args:
            max_history: 保留的历史记录最大数量
        """
        self.max_history = max_history
        self.metrics: Dict[str, deque] = defaultdict(lambda: deque(maxlen=max_history))
        self._lock = asyncio.Lock()

    async def record_metric(
        self,
        name: str,
        duration: float,
        success: bool = True,
        error_message: Optional[str] = None,
    ):
        """
        记录性能指标

        Args:
            name: 指标名称
            duration: 执行时间（秒）
            success: 是否成功
            error_message: 错误信息（如果有）
        """
        metric = PerformanceMetric(
            name=name,
            duration=duration,
            timestamp=time.time(),
            success=success,
            error_message=error_message,
        )

        async with self._lock:
            self.metrics[name].append(metric)

    async def get_stats(self, name: Optional[str] = None) -> Dict[str, Any]:
        """
        获取性能统计信息

        Args:
            name: 指标名称，如果为 None 则返回所有指标的统计

        Returns:
            Dict[str, Any]: 统计信息
        """
        async with self._lock:
            if name:
                return self._calculate_stats(name, self.metrics[name])
            else:
                return {
                    metric_name: self._calculate_stats(metric_name, metrics)
                    for metric_name, metrics in self.metrics.items()
                }

    def _calculate_stats(self, name: str, metrics: deque) -> Dict[str, Any]:
        """
        计算单个指标的统计信息

        Args:
            name: 指标名称
            metrics: 指标数据队列

        Returns:
            Dict[str, Any]: 统计信息
        """
        if not metrics:
            return {
                "name": name,
                "count": 0,
                "success_rate": 0.0,
                "avg_duration": 0.0,
                "min_duration": 0.0,
                "max_duration": 0.0,
            }

        durations = [m.duration for m in metrics]
        successes = [m.success for m in metrics]

        return {
            "name": name,
            "count": len(metrics),
            "success_rate": sum(successes) / len(successes) * 100,
            "avg_duration": sum(durations) / len(durations),
            "min_duration": min(durations),
            "max_duration": max(durations),
            "recent_errors": [
                m.error_message
                for m in list(metrics)[-10:]
                if not m.success and m.error_message
            ],
        }

    async def clear_metrics(self, name: Optional[str] = None):
        """
        清除性能指标

        Args:
            name: 指标名称，如果为 None 则清除所有指标
        """
        async with self._lock:
            if name:
                self.metrics[name].clear()
            else:
                self.metrics.clear()


# 全局性能监控器实例
_monitor = PerformanceMonitor()


def performance_tracked(name: Optional[str] = None):
    """
    性能跟踪装饰器

    Args:
        name: 指标名称，如果为 None 则使用函数名
    """

    def decorator(func):
        async def wrapper(*args, **kwargs):
            metric_name = name or func.__name__
            start_time = time.time()
            success = True
            error_message = None

            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                success = False
                error_message = str(e)
                raise
            finally:
                duration = time.time() - start_time
                await _monitor.record_metric(
                    metric_name, duration, success, error_message
                )

        return wrapper

    return decorator


def get_monitor() -> PerformanceMonitor:
    """获取全局性能监控器实例"""
    return _monitor
