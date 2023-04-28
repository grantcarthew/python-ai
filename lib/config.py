import json
import os
import rich
from lib.definitions import AI_CONFIG_PATH

def save_config(config):
    # Save the config as JSON
    with open(os.path.expanduser(AI_CONFIG_PATH), 'w') as config_file:
        json.dump(config, config_file)

def load_config():
    # Load the config
    config_file = os.path.expanduser(AI_CONFIG_PATH)
    if os.path.exists(config_file):
        with open(config_file) as config_file:
            config = json.load(config_file)
    else:
        config = {}

    # Save the config if any property was missing
    save_config(config)
    return config

