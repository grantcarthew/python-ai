from typing import List, Dict

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
