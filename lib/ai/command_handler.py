import sys
import subprocess
import json
from pick import pick
from lib.openai import prompts
from lib.openai import models
from lib.desktop.apps import open_vscode
from rich import print as rprint
from lib.definitions import AI_SAVE_PATH
from lib.ai.io import list_saved_chats, load_chat, save_chat
from lib.ai import user_input
from lib.ai import terminal
from pathlib import Path
from typing import List


def action(command_data: list[str], messages: list[dict], interactive: bool = False) -> dict:
    rprint('action')
    command_list = command_data.split()

    result = {
        'messages': messages,
        'call_api': False,
        'continue': True
    }

    if command_list[0] == 'help':
        help(interactive)
        return result

    if command_list[0] == 'exit':
        sys.exit(0)

    if command_list[0] == 'reset':
        result['messsages'] = list()
        return result

    if command_list[0] == 'save':
        save(messages)
        return result

    if command_list[0] == 'load':
        result['messages'] = load(command_data)
        return result


def help(interactive: bool) -> None:
    terminal.print_command_help(interactive)
    terminal.print_line()


def list(list_command: str) -> None:
    if list_command == True:
        try:
            list_command = pick(
                ['prompts', 'models'], 'What would you like to list:', indicator='>')[0]
        except KeyboardInterrupt:
            sys.exit(0)
    if list_command == 'prompts':
        prompts.show_prompt_list()
    if list_command == 'models':
        models.show_model_list()
    sys.exit(0)


def edit(edit_command: str) -> None:
    prompts_path = prompts.get_prompts_path()
    rprint('[cyan]Opening prepared prompts for editing[/]')
    rprint(f'[cyan]Path: "{prompts_path}"[/]')
    open_vscode(prompts_path)
    sys.exit(0)


def prompt(prompt_command: str) -> None:
    if prompt_command:
        if len(prompt_command) > 1:
            try:
                prompt_name = pick(
                    prompt_command, 'Choose a prepared prompt:', indicator='>')[0]
            except KeyboardInterrupt:
                sys.exit(0)
        if len(prompt_command) == 1:
            prompt_name = prompt_command[0]

        prompt = prompts.get_prompt_content(prompt_name)

        if prompt is None:
            rprint(f'Error: Prompt "{prompt_name}" does not exist')
            sys.exit(1)

        return (prompt_name, prompt)
    return (None, None)


def file(file_command: str) -> None:
    if file_command:
        return file_command.read_text()
    return None


def save(command_data: List[str], messages: List[dict]) -> None:
    # save_chat(messages)
    sys.exit(0)


def load(filter):
    return user_input.choose_saved_chat(filter)
