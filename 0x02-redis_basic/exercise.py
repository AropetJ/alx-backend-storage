#!/usr/bin/env python3
'''exercise.py'''
import redis
import uuid
from typing import Union, Callable, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    '''
    Decorator function to count the number of times a method is called.
    '''
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    '''
    Decorator function to store the input and output history of a method.
    '''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = '{}:inputs'.format(method.__qualname__)
        output_key = '{}:outputs'.format(method.__qualname__)
        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))
        return output
    return wrapper


def replay(func: Callable) -> None:
    '''
    Prints the input and output history of a method.
    '''
    if func is None or not hasattr(func, '__self__'):
        return
    redis_client = getattr(func.__self__, '_redis', None)
    if not isinstance(redis_client, redis.Redis):
        return
    fxn_name = func.__qualname__
    in_key = '{}:inputs'.format(fxn_name)
    out_key = '{}:outputs'.format(fxn_name)
    fxn_call_count = 0
    if redis_client.exists(fxn_name) != 0:
        fxn_call_count = int(redis_client.get(fxn_name))
    print('{} was called {} times:'.format(fxn_name, fxn_call_count))
    fxn_inputs = redis_client.lrange(in_key, 0, -1)
    fxn_outputs = redis_client.lrange(out_key, 0, -1)
    for fxn_input, fxn_output in zip(fxn_inputs, fxn_outputs):
        print('{}(*{}) -> {}'.format(
            fxn_name,
            fxn_input.decode("utf-8"),
            fxn_output,
        ))


class Cache:
    '''
    Cache class for storing and retrieving data using Redis.
    '''
    def __init__(self):
        '''
        Initializes a new instance of the Cache class.
        '''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''
        Stores the given data in Redis and returns the generated key.
        '''
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Callable = None) -> Union[str, bytes, int, float]:
        '''
        Retrieves the data associated with the given key from Redis.
        '''
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        '''
        Retrieves the string data associated with the given key from Redis.
        '''
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        '''
        Retrieves the integer data associated with the given key from Redis.
        '''
        return self.get(key, fn=int)
