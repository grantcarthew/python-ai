import json
from pathlib import Path
from lib.definitions import AI_CONFIG_PATH

def save_config(config):
    # Save the config as JSON
    with AI_CONFIG_PATH.open('w') as config_file:
        json.dump(config, config_file)

def load_config():
    # Load the config
    try:
        with AI_CONFIG_PATH.open() as config_file:
            config = json.load(config_file)
    except json.JSONDecodeError:
        config = {}

    # Save the config if any property was missing
    save_config(config)
    return config
