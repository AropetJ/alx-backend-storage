#!/usr/bin/env python3
'''web.py'''

import requests
import functools
import time
import redis

redis_client = redis.Redis()

def cache_decorator(func):
    '''
    Decorator function that caches the response of a web page for 10 seconds
    and tracks the number of times a URL was accessed using Redis.
    Args:
        func (function): The function to be decorated.
    Returns:
        function: The decorated function.
    '''
    @functools.wraps(func)
    def wrapper(url) -> str:
        '''
        Wrapper function that checks if the response for a given URL is already
        cached in Redis. If it is, it returns the cached response. Otherwise, it calls
        the original function to fetch the response, caches it in Redis, and returns it.
        It also tracks the number of times the URL was accessed in Redis.
        Args:
            url (str): The URL of the web page.
        Returns:
            str: The content of the web page.
        '''
        count_key = f'count:{url}'
        cached_response = redis_client.get(url)
        if cached_response:
            redis_client.incr(count_key)
            return cached_response.decode()

        response = func(url)
        redis_client.setex(url, 10, response)
        redis_client.incr(count_key)
        return response

    return wrapper


@cache_decorator
def get_page(url: str) -> str:
    '''
    Fetches the content of a web page.
    Args:
        url (str): The URL of the web page.
    Returns:
        str: The content of the web page.
    '''
    response = requests.get(url)
    return response.text
