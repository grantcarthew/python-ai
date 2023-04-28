import openai
import os
from datetime import datetime, timedelta
from pick import pick
from typing import List, Optional
from lib.definitions import AI_CACHE_PATH
from lib import cache
from rich.console import Console
from rich.table import Table
import rich

openai.api_key = os.environ.get('OPENAI_API_KEY', None)

def assert_openai_api_key():
    if not openai.api_key:
        rich.print('Please set the OPENAI_API_KEY environment variable')
        sys.exit(1)


def list_models() -> List:
    """Return a list of OpenAI models."""
    cache_key = 'openai_list_models'
    cache_data = cache.get_value(cache_key)
    if cache_data:
        return cache_data

    models = openai.Model.list()
    cache.set_value(cache_key, models, cache.ONE_DAY)
    return models


def list_models_simple(sort_by_created: bool = False) -> List[dict]:
    """
    Return a simplified list of OpenAI models, sorted by name or creation date.

    :param sort_by_created: Sort by creation date if True, sort by name otherwise.
    :return: A list of dictionaries containing model names and creation dates.
    """
    models = list_models().data
    models_simple = [{'name': m.id, 'created': datetime.fromtimestamp(
        m.created).isoformat()} for m in models]
    sort_key = 'created' if sort_by_created else 'name'
    return sorted(models_simple, key=lambda x: x[sort_key], reverse=sort_by_created)


def filter_models(filter: str) -> List[dict]:
    """
    Filter OpenAI models by a given string.

    :param filter: String to filter the models by.
    :return: A list of dictionaries containing matching model names and creation dates.
    """
    models = list_models_simple(sort_by_created=True)
    return [m for m in models if filter.lower() in m['name'].lower()]


def choose_model():
    models = [m['name'] for m in filter_models('gpt')]
    try:
        chosen_model = pick(models, 'Choose a model:', indicator='>')[0]
    except KeyboardInterrupt:
        sys.exit(0)
    return chosen_model


def get_latest_model(filter: str) -> Optional[str]:
    """
    Get the latest OpenAI model by a given string.

    :param filter: String to filter the models by.
    :return: The name of the latest matching model, or None if no match is found.
    """
    models = filter_models(filter)
    if len(models) == 0:
        return None
    return models[0]['name']

def show_model_list():
    table = Table()
    table.add_column('[cyan]OpenAI Models[/]', style='magenta', no_wrap=True)
    table.add_column('[cyan]Created Date[/]', style='magenta', no_wrap=True)
    for m in list_models_simple():
        table.add_row(m['name'], m['created'])
    rich.print(table)

