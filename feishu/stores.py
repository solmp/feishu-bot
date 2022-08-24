import time
from abc import ABC, abstractmethod
from typing import Optional

from .consts import TOKEN_EXPIRE_TIME, TOKEN_UPDATE_TIME

__all__ = ['TokenStore', 'MemoryStore', 'RedisStore']


class TokenStore(ABC):
    @abstractmethod
    def set(self, key: str, value: str, expire: float = TOKEN_EXPIRE_TIME):
        pass

    @abstractmethod
    def get(self, key: str):
        pass


class MemoryStore(TokenStore):
    """ 内存存储 """
    cache = {}
    timings = {}

    def set(self, key: str, value: str, expire: float = TOKEN_EXPIRE_TIME):
        expire -= TOKEN_UPDATE_TIME
        self.cache[key] = value
        self.timings[key] = time.time() + expire

    def get(self, key: str):
        expired_time = self.timings.get(key)
        if expired_time and expired_time < time.time():
            self.timings.pop(key, None)
            self.cache.pop(key, None)
        return self.cache.get(key)


class RedisStore(TokenStore):
    """ Redis存储 """

    def __init__(self, redis_url: Optional[str] = None):
        import redis
        if redis_url:
            self.client = redis.Redis.from_url(redis_url)
        else:
            self.client = redis.Redis()

    def set(self, key: str, value: str, expire: int = TOKEN_EXPIRE_TIME):
        expire -= TOKEN_UPDATE_TIME
        self.client.setex(key, expire, value)

    def get(self, key: str):
        self.client.get(key)
