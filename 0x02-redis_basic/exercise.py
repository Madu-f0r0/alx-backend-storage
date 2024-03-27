#!/usr/bin/env python3
"""Contains the class `Cache`"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Counts how many times methods of `Cache` are called"""
    key = method.__qualname__

    @wraps(method)
    def counter_func(self, *args, **kwargs):
        """Increments the count for a key everytime the method is called"""
        self.__redis.incr(key)
        return method(self, *args, **kwargs)

    return counter_func


class Cache:
    """Class Definition"""
    def __init__(self):
        """The constructor method of the class Cache"""
        self._redis = redis.Redis(host="localhost", port=6379, db=0)
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Inputs data in redis using a random key and returns the key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """Converts data back to the desired format"""
        redis_value = self._redis.get(key)
        if fn:
            redis_value = fn(redis_value)
        return redis_value

    def get_str(self, key: str) -> str:
        """Parameterizes Cache.get with the correct conversion function"""
        redis_value = self._redis.get(key)
        return redis_value.decode("utf-8")

    def get_int(self, key: str) -> int:
        """Parameterizes Cache.get result to an int"""
        redis_value = self._redis.get(key)
        try:
            redis_value = int(redis_value.decode("utf-8"))
        except Exception:
            redis_value = 0
        return redis_value
