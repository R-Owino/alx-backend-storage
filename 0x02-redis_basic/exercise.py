#!/usr/bin/env python3
"""
This module contains a class Cache
"""

import redis
import uuid
from typing import Union


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
