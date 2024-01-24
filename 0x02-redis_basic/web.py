#!/usr/bin/env python3
'''web.py'''

import requests
import functools
import time


def cache_decorator(func):
    '''
    Decorator function that caches the response of a web page for 10 seconds.
    Args:
        func (function): The function to be decorated.
    Returns:
        function: The decorated function.
    '''
    cache = {}

    @functools.wraps(func)
    def wrapper(url):
        '''
        Wrapper function that checks if the response for a given URL is already
        cached. If it is, it returns the cached response. Otherwise, it calls
        the original function to fetch the response, caches it, and returns it.
        Args:
            url (str): The URL of the web page.
        Returns:
            str: The content of the web page.
        '''
        if url in cache and cache[url]['expiration'] > time.time():
            return cache[url]['content']

        response = func(url)
        cache[url] = {
            'content': response,
            'expiration': time.time() + 10
        }
        return response

    return wrapper


@cache_decorator
def get_page(url):
    '''
    Fetches the content of a web page.
    Args:
        url (str): The URL of the web page.
    Returns:
        str: The content of the web page.
    '''
    response = requests.get(url)
    return response.text
