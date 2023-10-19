#!/usr/bin/env python3
"""
This module contains get_page function
"""

import redis
from functools import wraps
from typing import Callable
from requests import get


r = redis.Redis()


def cache_http_request(fxn: Callable) -> Callable:
    """
    Decorator that caches a http request in Redis
    """
    @wraps(fxn)
    def wrapper(url):
        r.incr(f"count:{url}")
        response = r.get(f"cached:{url}")
        if response:
            return response.decode("utf-8")
        result = fxn(url)
        r.setex(f"cached:{url}", 10, result)
        return result

    return wrapper


@cache_http_request
def get_page(url: str) -> str:
    """
    obtain the HTML content of a particular URL and returns it
    """
    return get(url).text
