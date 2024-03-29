import sys
import subprocess
import json
from pick import pick
from lib import config
from lib.openai import prompts
from lib.openai import models
from lib.desktop.apps import open_vscode
from rich import print as rprint
from lib.definitions import AI_SAVE_PATH
from lib.ai import io
from lib.ai import pdf
from lib.ai import user_input
from lib.ai import terminal
from lib.ai import messages
from pathlib import Path
from typing import List


def get_commands(interactive: bool = False) -> List[dict]:
    commands = [
        {
            'name': '3',
            'description': 'Change model to gpt-3.5-turbo',
            'option_help': '',
            'interactive': True,
            'passive': True
        },
        {
            'name': '4',
            'description': 'Change model to gpt-4',
            'option_help': '',
            'interactive': True,
            'passive': True
        },
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


def action(command_data: list[str], interactive: bool = False) -> dict:
    terminal.print_line()
    model_name = config.get_text_model_name()
    command_list = command_data.split()

    if command_list[0] == '3':
        config.set_text_model_name('gpt-3.5-turbo')
        terminal.print_title()
        return False

    if command_list[0] == '4':
        config.set_text_model_name('gpt-4')
        terminal.print_title()
        return False

    if command_list[0] == 'help':
        help_command(interactive)
        return False

    if command_list[0] == 'show':
        terminal.print_messages(report_if_none=True)
        return False

    if command_list[0] == 'exit':
        sys.exit(0)

    if command_list[0] == 'reset':
        messages.reset_chat()
        terminal.print_session_reset()
        return False

    if command_list[0] == 'save':
        save_chat(command_list[1:])
        return False

    if command_list[0] == 'load':
        load_chat(command_list[1:])
        return False

    if command_list[0] == 'import':
        file_imported = import_file(command_list[1:])
        if file_imported:
            return True
        return False

    if command_list[0] == 'export':
        export_chat(command_list[1:])
        return False

    if command_list[0] == 'config':
        configure_system(command_list[1:])
        return False

    terminal.print_not_a_command(command_data)
    help_command(interactive=interactive)
    return False


def help_command(interactive: bool) -> None:
    command_list = get_commands(interactive=interactive)
    terminal.print_command_help(
        command_list=command_list, interactive=interactive)


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


def edit_prompts() -> None:
    prompts_path = prompts.get_prompts_path()
    rprint('[cyan]Opening prepared prompts for editing[/]')
    rprint(f'[cyan]Path: "{prompts_path}"[/]')
    open_vscode(prompts_path)
    sys.exit(0)


def get_prompt(prompt_list: str) -> None:
    if len(prompt_list) == 0:
        return (None, None)

    if len(prompt_list) > 1:
        try:
            prompt_name = pick(
                prompt_list, 'Choose a prepared prompt:', indicator='>')[0]
        except KeyboardInterrupt:
            sys.exit(0)
    if len(prompt_list) == 1:
        prompt_name = prompt_list[0]

    prompt = prompts.get_prompt_content(prompt_name)

    if prompt is None:
        rprint(f'Error: Prompt "{prompt_name}" does not exist')
        sys.exit(1)

    return (prompt_name, prompt)


def file_content(file_path: str) -> None:
    return io.get_file_content(file_path)


def save_chat(command_data: List[str]) -> None:
    if len(command_data) < 1:
        file_name = 'default'

    if len(command_data) > 0:
        if messages.is_help_message(command_data[0]):
            terminal.print_save_help()
            return
        file_name = '-'.join(command_data)

    io.save_chat(file_name)
    terminal.print_chat_saved(file_name)


def load_chat(command_data: List[str]) -> None:
    if len(command_data) < 1:
        file_name = 'default'

    if len(command_data) > 0:
        if messages.is_help_message(command_data[0]):
            terminal.print_load_help()
            return

        if command_data[0] == '.':
            file_name = user_input.choose_saved_chat()
        else:
            file_name = '-'.join(command_data)
        file_name = user_input.choose_saved_chat(file_name)

    loaded_chat = io.load_chat(file_name)

    messages.restore_chat(loaded_chat)
    terminal.print_chat_loaded(file_name)


def import_file(command_data: List[str] = None) -> str:
    if len(command_data) < 1:
        file_path = user_input.launch_file_browser()
        rprint(type(file_path))
        if not isinstance(file_path, str):
            return False
    else:
        file_path = command_data[0]
    file_content = io.get_file_content(file_path)
    messages.add_user_content(file_content)
    return True


def export_chat(command_data: List[str]) -> None:
    doc = False
    format_type = 'md'
    chat_index = 0
    command_data_length = len(command_data)

    if command_data_length < 1:
        # TODO - Look up default format from config
        doc = messages.convert_to_markdown()
        io.export_chat(format_type, doc)
        return

    if messages.is_help_message(command_data[0]):
        terminal.print_export_help()
        return

    if command_data[0] in ['pdf', 'html', 'md']:
        format_type = command_data[0]

    if command_data[0].isdigit():
        chat_index = command_data[0]

    if command_data_length > 1 and command_data[1].isdigit():
        chat_index = command_data[1]

    doc = messages.change_format(
        format_type=format_type, chat_index=chat_index)
    io.export_chat(format_type=format_type, doc=doc)


def configure_system(command_list: List[str]) -> None:
    user_input.change_text_model()
