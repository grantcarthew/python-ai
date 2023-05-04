from pathlib import Path
from lib.definitions import AI_SAVE_PATH
import json


def get_saved_chats_path():
    return AI_SAVE_PATH


def list_saved_chats(filter: str = None) -> list:
    saved_chats = list()
    for saved_chat in Path(AI_SAVE_PATH).glob('**/*.json'):
        saved_chats.append(str(saved_chat.relative_to(
            AI_SAVE_PATH)).replace('.json', ''))
    if filter:
        saved_chats = [chat for chat in saved_chats if filter in chat]
    return sorted(saved_chats)


def save_chat(file_name, messages):
    save_path = Path(AI_SAVE_PATH) / f'{file_name}.json'
    with open(save_path, 'w') as f:
        json.dump(messages, f, indent=4)


def load_chat(file_name):
    load_path = Path(AI_SAVE_PATH) / f'{file_name}.json'
    with open(load_path, 'r') as f:
        return json.load(f)
