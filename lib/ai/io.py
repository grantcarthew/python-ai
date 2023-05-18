from pathlib import Path
from lib.definitions import AI_SAVE_PATH
from lib.ai import messages
from rich import print as rprint
import json
import sys


def get_saved_chats_path():
    return AI_SAVE_PATH


def list_saved_chats(filter: str = None) -> list:
    saved_chats = list()
    for saved_chat in Path(AI_SAVE_PATH).glob('**/*.json'):
        saved_chats.append(str(saved_chat.relative_to(
            AI_SAVE_PATH)).replace('.json', ''))
    if type(filter) == str:
        saved_chats = [chat for chat in saved_chats if filter in chat]
    return sorted(saved_chats)


def save_chat(file_name: str) -> None:
    if file_name.startswith('/'):
        file_name = file_name[1:]
    file_name = file_name.replace(' ', '-')
    save_path = (AI_SAVE_PATH / f'{file_name}.json')

    if '/' in file_name:
        save_path.parent.mkdir(parents=True, exist_ok=True)

    with open(save_path, 'w') as f:
        json.dump(messages.chat, f, indent=4)


def load_chat(file_name):
    load_path = (AI_SAVE_PATH / f'{file_name}.json')
    with open(load_path, 'r') as f:
        return json.load(f)


def get_file_content(file_path):
    if not file_path:
        return False
    try:
        if Path.is_file(file_path):
            return Path(file_path).resolve().read_text()
        rprint(f'[red]Error: Invalid file path: {file_path}[/]')
    except Exception as err:
        rprint(f'Error: {err}')
        sys.exit(0)

def export_chat(doc: str) -> None:
    file_path = Path.home() / 'Downloads' / 'chat_default.md'
    file_path.write_text(doc)

