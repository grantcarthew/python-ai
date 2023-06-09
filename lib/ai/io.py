from pathlib import Path
from lib.definitions import AI_SAVE_PATH, AI_CHAT_LOG_PATH
from lib.ai import messages
from lib import config
from lib import utils
from rich import print as rprint
import json
import sys
import webbrowser
import os
import sys
import subprocess
from datetime import datetime


datetimeiso = utils.generate_iso_datetime()
chat_log_file_name = f'{datetimeiso}-chat-log.md'


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


def export_chat(format_type: str, doc: str, file_name: str = None) -> None:
    if not file_name:
        iso_date_time = utils.generate_iso_datetime()
        file_name = Path(f'{iso_date_time}-chat-export.{format_type}')

    file_path = config.get_export_path() / file_name
    if format_type in ['html', 'md']:
        file_path.write_text(doc)
    else:
        with open(str(file_path), 'wb') as f:
            f.write(bytearray(doc))

    open_file(str(file_path))


def update_chat_log(role: str, content: str) -> None:
    file_path = AI_CHAT_LOG_PATH / chat_log_file_name
    with file_path.open(mode='a') as log:
        log.write('\n\n---\n\n')
        log.write(f'# {role}')
        log.write('\n\n---\n\n')
        log.write(content)


def open_file(file_path: str) -> None:
    if sys.platform.startswith('darwin'):
        subprocess.call(('open', file_path))
    elif os.name == 'nt':
        os.startfile(file_path)
    elif os.name == 'posix':
        subprocess.call(('xdg-open', file_path))


def open_url(url: str) -> None:
    webbrowser.open(url)
