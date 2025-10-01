"""
内存缓存实现
"""

import time
import asyncio
from typing import Any, Dict, Optional, Callable, Awaitable
from ...core.config import get_config


class MemoryCache:
    """简单的内存缓存实现"""

    def __init__(self, enabled: bool = None, default_ttl: int = None):
        """
        初始化缓存

        Args:
            enabled: 是否启用缓存，如果为 None 则使用配置文件设置
            default_ttl: 默认过期时间（秒），如果为 None 则使用配置文件设置
        """
        config = get_config()
        self.enabled = enabled if enabled is not None else config.cache.enabled
        self.default_ttl = default_ttl if default_ttl is not None else config.cache.ttl
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[Any]:
        """
        获取缓存值

        Args:
            key: 缓存键

        Returns:
            Optional[Any]: 缓存值，如果不存在或已过期则返回 None
        """
        if not self.enabled:
            return None

        async with self._lock:
            if key not in self._cache:
                return None

            cache_item = self._cache[key]
            if time.time() > cache_item["expires_at"]:
                del self._cache[key]
                return None

            return cache_item["value"]

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """
        设置缓存值

        Args:
            key: 缓存键
            value: 缓存值
            ttl: 过期时间（秒），如果为 None 则使用默认值
        """
        if not self.enabled:
            return

        ttl = ttl or self.default_ttl
        expires_at = time.time() + ttl

        async with self._lock:
            self._cache[key] = {
                "value": value,
                "expires_at": expires_at,
                "created_at": time.time(),
            }

    async def delete(self, key: str) -> None:
        """
        删除缓存值

        Args:
            key: 缓存键
        """
        if not self.enabled:
            return

        async with self._lock:
            self._cache.pop(key, None)

    async def clear(self) -> None:
        """清空所有缓存"""
        if not self.enabled:
            return

        async with self._lock:
            self._cache.clear()

    async def cleanup_expired(self) -> int:
        """
        清理过期的缓存项

        Returns:
            int: 清理的项目数量
        """
        if not self.enabled:
            return 0

        current_time = time.time()
        expired_keys = []

        async with self._lock:
            for key, cache_item in self._cache.items():
                if current_time > cache_item["expires_at"]:
                    expired_keys.append(key)

            for key in expired_keys:
                del self._cache[key]

        return len(expired_keys)

    def get_stats(self) -> Dict[str, Any]:
        """
        获取缓存统计信息

        Returns:
            Dict[str, Any]: 缓存统计信息
        """
        if not self.enabled:
            return {"enabled": False}

        return {
            "enabled": True,
            "total_items": len(self._cache),
            "default_ttl": self.default_ttl,
        }


# 全局缓存实例
_cache = MemoryCache()


def cached(ttl: Optional[int] = None, key_prefix: str = ""):
    """
    缓存装饰器

    Args:
        ttl: 缓存过期时间（秒）
        key_prefix: 缓存键前缀
    """

    def decorator(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
        async def wrapper(*args, **kwargs) -> Any:
            # 生成缓存键
            cache_key = f"{key_prefix}:{func.__name__}:{hash(str(args) + str(sorted(kwargs.items())))}"

            # 尝试从缓存获取
            cached_result = await _cache.get(cache_key)
            if cached_result is not None:
                return cached_result

            # 执行函数并缓存结果
            result = await func(*args, **kwargs)
            await _cache.set(cache_key, result, ttl)

            return result

        return wrapper

    return decorator


def get_cache() -> MemoryCache:
    """获取全局缓存实例"""
    return _cache
