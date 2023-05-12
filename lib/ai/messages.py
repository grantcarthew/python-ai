from typing import List, Dict
from rich import print as rprint

chat: List[Dict[str, str]] = []


def add_user_content(user_message: str) -> None:
    """
    Add a user message to the chat.

    :param user_message: The user message to be added.
    """
    chat.append({'role': 'user', 'content': user_message})


def add_assistant_content(assistant_message: str) -> None:
    """
    Add an assistant message to the chat.

    :param assistant_message: The assistant message to be added.
    """
    chat.append({'role': 'assistant', 'content': assistant_message})


def reset_chat() -> None:
    """
    Removes all content from the chat.
    """
    chat = list()


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
