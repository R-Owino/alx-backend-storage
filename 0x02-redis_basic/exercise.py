#!/usr/bin/env python3
"""
This module contains a class Cache
"""

import redis
import uuid
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    A decorator to count how many times a method is called.
    It uses the method's qualified name as a key in Redis.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = f"{method.__qualname__}"
        self._redis.incr(key)  # Increment the call count
        return method(self, *args, **kwargs)  # Call the original method

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    A decorator to store the history of inputs and outputs
    for a specific function

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped method that records input arguments and outputs
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Create keys for input and output lists
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, output)

        return output

    return wrapper


def replay(fxn: Callable) -> None:
    """
    Display the history of calls for a particular function
    using Redis input and output lists.

    Args:
        fxn (Callable): The function for which the call history
        should be displayed.

    Returns:
        None
    """
    mem = Redis()
    func_name_qual = fxn.__qualname__
    value = int(mem.get(func_name_qual) or b"0")
    print(f"{func_name_qual} was called {value} times:")
    inputs = mem.lrange(f"{func_name_qual}:inputs", 0, -1)
    outputs = mem.lrange(f"{func_name_qual}:outputs", 0, -1)

    for input_bytes, output_bytes in zip(inputs, outputs):
        input_string = input_bytes.decode("utf-8")
        output_string = output_bytes.decode("utf-8")
        print(f"{func_name_qual}(*{input_string}) -> {output_string}")


class Cache:
    """
    A class Cache
    """
    def __init__(self, host='localhost', port=6379, db=0):
        """
        Initialize the Cache object by connecting to a Redis server
        and flushing the database.

        Args:
            host (str): The Redis server host.
            port (int): The Redis server port.
            db (int): The Redis database number to use.
        """
        self._redis = redis.Redis(host=host, port=port, db=db)
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis and return a random key.

        Args:
            data (Union[str, bytes, int, float]): The data to be stored

        Returns:
            str: A randomly generated key under which the data is stored
        """
        # Generate a random key using uuid
        key = str(uuid.uuid4())

        # Store the data in Redis using the random key
        if isinstance(data, (int, float)):
            self._redis.set(key, str(data))
        elif isinstance(data, (str, bytes)):
            self._redis.set(key, data)

        return key

    def get(self, key: str, fn: Callable[[bytes],
            Union[str, int, None]] = None) -> Union[str, int, None]:
        """
        Get a value by key and optionally apply a conversion function

        Args:
            key (str): The key under which the data is stored
            fn (Callable[[bytes], Union[str, int, None]]): A callable function
            to convert the data

        Returns:
            Union[str, int, None]: The retrieved data
        """
        data = self._redis.get(key)
        if data is not None:
            if fn is not None:
                return fn(data)
            else:
                return data
        else:
            return None

    def get_str(self, key: str) -> str:
        """
        Get a string value from Redis by key

        Args:
            key (str): The key under which the data is stored

        Returns:
            str: The retrieved string data
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """
        Get an integer value from Redis by key

        Args:
            key (str): The key under which the data is stored

        Returns:
            int: The retrieved integer data
        """
        return self.get(key, fn=lambda d: int(d))
