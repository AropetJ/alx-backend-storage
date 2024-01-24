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
        Wrapper function that checks if the response for a given URL is already
        cached in Redis.
        '''
        redis_client.incr(f'count:{url}')
        cached_response = redis_client.get(f'cached:{url}')
        if cached_response:
            return cached_response.decode('utf-8')

        cached_response = func(url)
        redis_client.set(f'count:{url}', 0)
        redis_client.setex(f'result:{url}', 10, cached_response)
        return cached_response
    return wrapper


@cache_decorator
def get_page(url: str) -> str:
    '''
    Fetches the content of a web page.
    '''
    return requests.get(url).text
