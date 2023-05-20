from datetime import datetime, timedelta
from functools import lru_cache
from lib.definitions import AI_CONFIG_PATH
from lib.definitions import AI_CONFIG_PATH, AI_VERSION
from lib.openai import models
from pathlib import Path
from threading import Lock
import json
import os
import rich
import shelve
mutex = Lock()

default_export_path = Path.home() / 'Downloads'


export_path_key = 'export_path'
text_model_name_key = 'text_model_name'


def __assert_config(config):
    """ Ensures the config is in a stable state """
    key = 'ai_version'
    if key in config:
        config_data = config[key]
        if config_data == AI_VERSION:
            return

    for key_to_clear in list(config.keys()):
        del config[key_to_clear]
    config[key] = AI_VERSION


def set_value(key: str, value: any) -> None:
    """ Sets a config value """
    get_value.cache_clear()
    with mutex, shelve.open(str(AI_CONFIG_PATH)) as config:
        __assert_config(config)
        config[key] = value
    return None


@lru_cache(maxsize=None)
def get_value(key: str) -> any:
    """ Gets a value from the config """
    with mutex, shelve.open(str(AI_CONFIG_PATH)) as config:
        __assert_config(config)
        if key not in config:
            return None
        return config[key]


def clear_config() -> None:
    """ Deletes all keys from the config """
    with mutex, shelve.open(str(AI_CONFIG_PATH)) as config:
        for key in list(config.keys()):
            del config[key]
    return None


def get_text_model_name() -> str:
    """ Gets the text model name from the config """
    text_model_name = get_value(text_model_name_key)
    if not text_model_name:
        text_model_name = models.choose_model()
        set_value(text_model_name_key, text_model_name)
    return text_model_name


def set_text_model_name(text_model_name: str) -> None:
    """ Sets the text model name in the config """
    set_value(text_model_name_key, text_model_name)


def get_export_path() -> str:
    """ Gets the export path from the config """
    export_path = get_value(export_path_key)
    if not export_path:
        export_path = default_export_path
        set_value(export_path_key, export_path)
    return export_path


def set_export_path(export_path: str) -> None:
    """ Sets the export path in the config """
    set_value(export_path_key, export_path)
