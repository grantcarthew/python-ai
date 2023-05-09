import sys
import subprocess
import json
from pick import pick
from lib.openai import prompts
from lib.openai import models
from lib.desktop.apps import open_vscode
from rich import print as rprint
from lib.definitions import AI_SAVE_PATH
from lib.ai import io
from lib.ai import user_input
from lib.ai import terminal
from lib.ai import messages
from pathlib import Path
from typing import List

def get_commands(interactive: bool = False) -> List[dict]:
    commands = [
        {
            'name': 'config',
            'description': 'Change ai configuration',
            'option_help': '',
            'interactive': True,
            'passive': True
        },
        {
            'name': 'edit',
            'description': 'Opens the prompts file in the default editor',
            'option_help': '',
            'interactive': True,
            'passive': True
        },
        {
            'name': 'import',
            'description': 'Import the contents of a file into the chat',
            'option_help': '\[file-path]',
            'interactive': True,
            'passive': False
        },
        {
            'name': 'export',
            'description': 'Export the current chat (md, pdf, txt)',
            'option_help': '\[file-path] \[file-type]',
            'interactive': True,
            'passive': False
        },
        {
            'name': 'help',
            'description': 'Shows this help message',
            'option_help': '',
            'interactive': True,
            'passive': True
        },
        {
            'name': 'list',
            'description': 'Lists available resources',
            'option_help': '\[prompts] or \[modules]',
            'interactive': True,
            'passive': True
        },
        {
            'name': 'load',
            'description': 'Load a saved chat',
            'option_help': '\[session-name]',
            'interactive': True,
            'passive': False
        },
        {
            'name': 'model',
            'description': 'Change the GPT model being used',
            'option_help': '\[model-name]',
            'interactive': True,
            'passive': True
        },
        {
            'name': 'prompt',
            'description': 'Opens the prompts file in the default editor',
            'option_help': '\[prompt-name]',
            'interactive': True,
            'passive': False
        },
        {
            'name': 'reset',
            'description': 'Resets the session',
            'option_help': '',
            'interactive': True,
            'passive': False
        },
        {
            'name': 'save',
            'description': 'Saves the session',
            'option_help': '\[session-name]',
            'interactive': True,
            'passive': False
        },
        {
            'name': 'show',
            'description': 'Shows the current chat',
            'option_help': '',
            'interactive': True,
            'passive': False
        }
    ]
    if interactive:
        return [command for command in commands if command['interactive']]
    return [command for command in commands if command['passive']]

def action(command_data: list[str], model_name: str, interactive: bool = False) -> dict:
    command_list = command_data.split()

    result = {
        'call_api': False,
        'continue': True
    }

    if command_list[0] == 'help':
        help(interactive)
        terminal.print_line()
        return result

    if command_list[0] == 'show':
        terminal.print_messages()
        return result

    if command_list[0] == 'exit':
        sys.exit(0)

    if command_list[0] == 'reset':
        messages.reset_chat()
        rprint(f'[cyan]Session Reset | {model_name}[/]')
        terminal.print_line()
        return result

    if command_list[0] == 'save':
        save_chat()
        return result

    if command_list[0] == 'load':
        return result

    if command_list[0] == 'import':
        file_imported = import_file(command_list[1:])
        if file_imported:
            result['call_api'] = True
            return result
        return result

    if command_list[0] == 'export':
        return result

    result['call_api'] = True
    result['continue'] = False
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


def edit_prompts(edit_command: str) -> None:
    prompts_path = prompts.get_prompts_path()
    rprint('[cyan]Opening prepared prompts for editing[/]')
    rprint(f'[cyan]Path: "{prompts_path}"[/]')
    open_vscode(prompts_path)
    sys.exit(0)


def get_prompt(prompt_command: str) -> None:
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


def file_content(file_path: str) -> None:
    return io.get_file_content(file_path)


def save_chat(command_data: List[str]) -> None:
            # io.save_chat('test_name', messages)
            # rprint('Chat saved')
            # call_api = False
            # continue
    sys.exit(0)


def load_chat(filter):
    file_path = user_input.get_file_path()
    file_content = io.get_file_content(file_path)
    messages.add_user_content(file_content)
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

def import_file(command_list: str = None) -> str:
    if len(command_list) < 1:
        file_path = user_input.launch_file_browser()
        rprint(type(file_path))
        if not isinstance(file_path, str):
            return False
    else:
        file_path = command_list[0]
    file_content = io.get_file_content(file_path)
    messages.add_user_content(file_content)
    return True
