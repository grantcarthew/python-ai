"""

This module provides a persistent cache for any type of object or value.
It is built on top of the Python shelve module.

For the functions with AWS in their name, the cache is dependent on
the AWS Account keys assigned in the terminal.

Usage:

    from lib import cache

    key = 'name of a thing'
    value = 'something expensive to get'
    ttl = 86400000 # 1 day in milliseconds

    cache.set_value(key, value, ttl) # 'None'
    cache.get_value(key) # 'None' if key does not exist
    cache.remove_value(key) # 'True' if the value existed, otherwise 'False'

    cache.clear_cache()

    # AWS Account ID functions
    cache.setAwsValue(key, value, ttl)
    cache.getAwsValue(key)
    cache.removeAwsValue(key)

Notes:

    get_value:
    - Will return the original value for a cache hit.
    - Will return 'None' for a cache miss.
    - Will return 'None' if the value is past the TTL.

    set_value:
    - Assigns the value to the supplied key in the cache.
    - The TTL value is in milliseconds.
    - The default TTL value is 0.
    - Any TTL value less than 1 will never expire.
    - Returns 'None'

    remove_value:
    - Deletes the key from the cache if it exists.
    - Returns 'True' if the key did exist.
    - Returns 'False' if the key did not exist.

"""

import os
import shelve
import rich
from threading import Lock
from pathlib import Path
from datetime import datetime, timedelta
from lib.definitions import AI_CACHE_PATH, AI_VERSION
mutex = Lock()

ONE_MINUTE = 60000
FIVE_MINUTES = 300000
TEN_MINUTES = 600000
TWENTY_MINUTES = 1200000
THIRTY_MINUTES = 1800000
FOURTY_MINUTES = 2400000
FIFTY_MINUTES = 3000000
ONE_HOUR = 3600000
ONE_DAY = 86400000
ONE_WEEK = 604800000
TWO_WEEKS = 1209600000
ONE_MONTH = 2629800000
SIX_MONTHS = 15778800000
ONE_YEAR = 31557600000


def __assert_cache(cache):
    """ Ensures the cache is in a stable state """
    key = 'ai_version'
    if key in cache:
        cacheData = cache[key]
        if cacheData == AI_VERSION:
            return

    for keyToClear in list(cache.keys()):
        del cache[keyToClear]
    cache[key] = AI_VERSION


def set_value(key: str, value: any, ttl: int = 0) -> None:
    """ Sets an AWS Account cache key to a value with optional TTL """
    with mutex, shelve.open(str(AI_CACHE_PATH)) as cache:
        __assert_cache(cache)
        if ttl > 0:
            ttl = datetime.now() + timedelta(milliseconds=ttl)
        cache[key] = {
            'value': value,
            'ttl': ttl
        }
    return None


def get_value(key: str) -> any:
    """ Gets a value from the AWS Account cache if exists and within TTL """
    with mutex, shelve.open(str(AI_CACHE_PATH)) as cache:
        __assert_cache(cache)
        if key not in cache:
            return None
        cacheData = cache[key]

    if type(cacheData['ttl']) != datetime:
        return cacheData['value']
    if cacheData['ttl'] < datetime.now():
        return None
    return cacheData['value']


def remove_value(key: str) -> bool:
    """ Deletes a specific key from the cache """
    with mutex, shelve.open(str(AI_CACHE_PATH)) as cache:
        __assert_cache(cache)
        if key:
            del cache[key]
            return True
    return False


def clear_cache() -> None:
    """ Deletes all keys from the cache including AWS Account related keys """
    with mutex, shelve.open(str(AI_CACHE_PATH)) as cache:
        for key in list(cache.keys()):
            del cache[key]
    return None
