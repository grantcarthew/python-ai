from typing import List, Dict
from rich import print as rprint
from datetime import datetime
from lib import config
from lib.ai import io

chat: List[Dict[str, str]] = []


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


def convert_to_markdown(chat_index: int = 0):
    global chat
    model_name = config.get_text_model_name()
    dt = datetime.now()
    date_str = dt.strftime('%Y-%m-%d')
    time_str = dt.strftime('%H:%M:%S')
    doc = f'# ChatGPT | {model_name} | {date_str} | {time_str}\n'

    if chat_index == 0:
        for part in chat:
            if part['role'] == 'user':
                doc += f'\n---\n\n## User\n\n---\n\n'
            else:
                doc += f'\n---\n\n## Assistant\n\n---\n\n'
            doc += part['content']
            doc += '\n'
    return doc

