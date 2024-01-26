#!/usr/bin/env python3
'''web.py
'''
import redis
import requests
from functools import wraps
from typing import Callable

redis_client = redis.Redis()


def cache_decorator(method: Callable) -> Callable:
    '''
    Decorator function that caches the response of a web page for 10 seconds
    and tracks the number of times a URL was accessed using Redis.
    '''
    @wraps(method)
    def wrapper(url) -> str:
        '''
        Wrapper function that checks if the response for a given URL is
        already cached in Redis.
        '''
        @wraps(method)
        def wrapper(url):
            """ Wrapper for decorator """
            redis_client.incr(f"count:{url}")
            cached_html = redis_client.get(f"cached:{url}")
            if cached_html:
                return cached_html.decode('utf-8')
            html = method(url)
            redis_client.setex(f"cached:{url}", 10, html)
            return html

        return wrapper


@cache_decorator
def get_page(url: str) -> str:
    '''
    Fetches the content of a web page.
    '''
    req = requests.get(url)
    return req.text
