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
    def wrapper(self, *args, **kwargs)-> Any:
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


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

    def call_history(method: Callable) -> Callable:
        '''
        Decorator function to store the input and output history of a method.
        '''
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            input_key = method.__qualname__ + ":inputs"
            output_key = method.__qualname__ + ":outputs"
            self._redis.rpush(input_key, str(args))
            output = method(self, *args, **kwargs)
            self._redis.rpush(output_key, str(output))
            return output
        return wrapper

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''
        Stores the given data in Redis and returns the generated key.
        Args:
            data: The data to be stored.
        Returns:
            The generated key for the stored data.
        '''
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Callable = None) -> Union[str, bytes, int, float]:
        '''
        Retrieves the data associated with the given key from Redis.
        Args:
            key: The key to retrieve the data for.
            fn: Optional function to apply on the retrieved data.
        Returns:
            The retrieved data, optionally transformed by the provided function.
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
        Args:
            key: The key to retrieve the string data for.
        Returns:
            The retrieved string data.
        '''
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        '''
        Retrieves the integer data associated with the given key from Redis.
        Args:
            key: The key to retrieve the integer data for.
        Returns:
            The retrieved integer data.
        '''
        return self.get(key, fn=int)

    def replay(self, func):
        '''
        Prints the input and output history of a method.
        Args:
            func: The method to replay the history for.
        '''
        key = func.__qualname__ + ":inputs"
        inputs = self._redis.lrange(key, 0, -1)
        key = func.__qualname__ + ":outputs"
        outputs = self._redis.lrange(key, 0, -1)
        print(f"{func.__qualname__} was called {len(inputs)} times:")
        for i in range(len(inputs)):
            input_str = inputs[i].decode("utf-8")
            output_str = outputs[i].decode("utf-8")
            print(f"{func.__qualname__}(*{input_str}) -> {output_str}")
