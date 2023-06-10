from typing import List, Dict
from rich import print as rprint
from datetime import datetime
from lib import config
from lib.ai import io, pdf
from xml.dom.minidom import Document
import sys
from markdown import markdown

chat: List[Dict[str, str]] = []

html_boiler_plate = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    {{content}}
</body>
</html>
"""

def _get_chat_title():
    model_name = config.get_text_model_name()
    dt = datetime.now()
    date_str = dt.strftime('%Y-%m-%d')
    time_str = dt.strftime('%H:%M:%S')
    return f'ChatGPT | {model_name} | {date_str} | {time_str}\n'


def add_user_content(user_message: str) -> None:
    """
    Add a user message to the chat.

    :param user_message: The user message to be added.
    """
    global chat
    chat.append({'role': 'user', 'content': user_message})
    io.update_chat_log(role='User', content=user_message)


def add_assistant_content(assistant_message: str) -> None:
    """
    Add an assistant message to the chat.

    :param assistant_message: The assistant message to be added.
    """
    global chat
    chat.append({'role': 'assistant', 'content': assistant_message})
    io.update_chat_log(role='Assistant', content=assistant_message)


def reset_chat() -> None:
    """
    Removes all content from the chat.
    """
    global chat
    chat = list()


def restore_chat(chat_to_restore: List[Dict[str, str]]) -> None:
    """
    Replaces the current chat with the chat_to_restore.

    :param chat_to_restore: A loaded chat.
    """
    global chat
    chat = chat_to_restore

def ready_to_send() -> bool:
    """
    Returns True if the last message in the chat is a user role message.
    """
    global chat
    return len(chat) > 0 and chat[-1]['role'] == 'user'


def is_help_message(message: str) -> bool:
    """
    Returns True if the message is a string they could mean the user wants help

    :param message: The string under test to see if it is a help string
    """
    if message.lower() == 'help':
        return True
    if message.lower() == '/help':
        return True
    if message.lower() == '?':
        return True
    if message.lower() == '/?':
        return True
    if message.lower() == '/':
        return True
    return False

def is_exit_message(message: str) -> bool:
    """
    Returns True if the message is a string they could to exit the chat

    :param message: The string under test to see if it is an exit string
    """
    if message.lower() == 'exit':
        return True
    if message.lower() == '/exit':
        return True
    if message.lower() == 'quit':
        return True
    if message.lower() == '/quit':
        return True
    if message.lower() == ':q':
        return True
    return False


def get_chat_reverse_index(chat_index: int = 0) -> List:
    chat_index = int(chat_index)
    if chat_index == 0:
        return chat
    else:
        indexOffset = chat_index * 2
        return chat[-indexOffset:]



def convert_to_markdown(chat_index: int = 0):
    global chat

    def chat_to_markdown(chat_messages):
        doc = f'# {_get_chat_title()}'
        for part in chat_messages:
            if part['role'] == 'user':
                doc += f'\n---\n\n## User\n\n---\n\n'
            else:
                doc += f'\n---\n\n## Assistant\n\n---\n\n'
            doc += part['content']
            doc += '\n'
        return doc

    indexed_chat = get_chat_reverse_index(chat_index)
    return chat_to_markdown(indexed_chat)

def convert_to_html(chat_index: int = 0):
    md = convert_to_markdown(chat_index=chat_index)
    html = html_boiler_plate.replace('{{content}}', markdown(md))
    return html

def change_format(format_type: str = 'md', chat_index: int = 0) -> str:

    if format_type == 'md':
        return convert_to_markdown(chat_index=chat_index)
    if format_type == 'html':
        return convert_to_html(chat_index=chat_index)
    if format_type == 'pdf':
        indexed_chat = get_chat_reverse_index(chat_index)
        return pdf.convert_chat_to_pdf(indexed_chat)

    rprint('Error: invalid format')
    sys.exit(1)
