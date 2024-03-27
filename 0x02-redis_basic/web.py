#!/usr/bin/env python3
"""Implements a web cache and tracker"""

import redis
import requests
from functools import wraps

r = redis.Redis()


def url_access_counter(method):
    """Tracks how many times a particular URL was accessed"""
    @wraps(method)
    def wrapper(url):
        key = "cached:" + url
        data = r.get(key)

        if data:
            return data.decode("utf-8")

        count_key = "count:" + url
        html = method(url)

        r.incr(count_key)
        r.set(key, html)
        r.expire(key, 10)
        return html

    return wrapper


@url_access_counter
def get_page(url: str) -> str:
    """Obtains the HTML content of a URL"""
    result = requests.get(url)
    return result.text
