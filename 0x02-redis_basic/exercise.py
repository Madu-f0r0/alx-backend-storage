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
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return counter_func


def call_history(method: Callable) -> Callable:
    """Stores the history of inputs and outputs for a particular function"""
    @wraps(method)
    def store_history(self, *args, **kwargs):
        """Performs the actual storage"""
        input = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input)

        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output)
        return output
    return store_history


def replay(fn: Callable):
    """Displays the history of calls of a particular function"""
    r = redis.Redis()
    fxn_name = fn.__qualname__
    value = r.get(fxn_name)
    try:
        value = int(value.decode("utf-8"))
    except Exception:
        value = 0

    print("{} was called {} tmes".format(fxn_name, value))

    inputs = r.lrange("{}:inputs".format(fxn_name), 0, -1)
    outputs = r.lrange("{}:outputs".format(fxn_name), 0, -1)
    fr input, output in zip(inputs, outputs):
        try:
            input = input.decode("utf-8")
        except Exception:
            input = ""
        try:
            output = output.decode("utf-8")
        except Exception:
            output = ""
        print("{}(*{}) -> {}".format(fxn_name, input, output))


class Cache:
    """Class Definition"""
    def __init__(self):
        """The constructor method of the class Cache"""
        self._redis = redis.Redis(host="localhost", port=6379, db=0)
        self._redis.flushdb()

    @call_history
    @count_calls
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
