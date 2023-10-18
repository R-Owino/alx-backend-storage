#!/usr/bin/env python3
"""
This module contains a class Cache
"""

import redis
import uuid
from typing import Union, Callable


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
