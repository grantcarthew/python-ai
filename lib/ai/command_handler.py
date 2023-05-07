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

def get_commands(interactive: bool = False) -> List[dict]:
    commands = [
        {
            'name': 'config',
            'description': 'Change ai configuration',
            'interactive': True,
            'passive': True
        },
        {
            'name': 'edit',
            'description': 'Opens the prompts file in the default editor',
            'interactive': True,
            'passive': True
        },
        {
            'name': 'export',
            'description': 'Export the current chat',
            'interactive': True,
            'passive': False
        },
        {
            'name': 'help',
            'description': 'Shows this help message',
            'interactive': True,
            'passive': True
        },
        {
            'name': 'list',
            'description': 'Lists available resources',
            'interactive': True,
            'passive': True
        },
        {
            'name': 'load',
            'description': 'Load a saved chat',
            'interactive': True,
            'passive': False
        },
        {
            'name': 'model',
            'description': 'Change the GPT model being used',
            'interactive': True,
            'passive': True
        },
        {
            'name': 'prompt',
            'description': 'Opens the prompts file in the default editor',
            'interactive': True,
            'passive': False
        },
        {
            'name': 'reset',
            'description': 'Resets the session',
            'interactive': True,
            'passive': False
        },
        {
            'name': 'save',
            'description': 'Saves the session',
            'interactive': True,
            'passive': False
        },
        {
            'name': 'show',
            'description': 'Shows the current chat',
            'interactive': True,
            'passive': False
        }
    ]
    if interactive:
        return [command for command in commands if command['interactive']]
    return [command for command in commands if command['passive']]

def action(command_data: list[str], model_name: str, messages: list[dict], interactive: bool = False) -> dict:
    command_list = command_data.split()

    result = {
        'messages': messages,
        'call_api': False,
        'continue': True
    }

    if command_list[0] == 'help':
        help(interactive)
        return result

    if command_list[0] == 'show':
        terminal.print_messages(messages)
        return result

    if command_list[0] == 'exit':
        sys.exit(0)

    if command_list[0] == 'reset':
        result['messages'] = list()
        rprint(f'[cyan]Session Reset | {model_name}[/]')
        terminal.print_line()
        return result

    if command_list[0] == 'save':
        save(messages)
        return result

    if command_list[0] == 'load':
        result['messages'] = load(command_data)
        return result


def help(interactive: bool) -> None:
    command_list = get_commands(interactive=interactive)
    terminal.print_command_help(command_list=command_list, interactive=interactive)


def list_command(list_command: str) -> None:
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
            # io.save_chat('test_name', messages)
            # rprint('Chat saved')
            # call_api = False
            # continue
    sys.exit(0)


def load(filter):
            # filter = None
            # if user_message.lower().startswith('load '):
            #     words = user_message.lower().split()
            #     if len(words) > 2:
            #         pass # TODO
            #     if len(words) == 2:
            #        filter = words[1]
            # user_input.choose_saved_chat(filter)
            # messages = io.load_chat('test_name')
            # rprint('Chat loaded')
            # call_api = False
            # continue
    return user_input.choose_saved_chat(filter)
