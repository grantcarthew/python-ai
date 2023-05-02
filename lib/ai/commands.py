import sys
import subprocess
from pick import pick
from lib.openai import prompts
from lib.openai import models
from lib.desktop.apps import open_vscode
from rich import print as rprint

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
                prompt_name = pick(prompt_command, 'Choose a prepared prompt:', indicator='>')[0]
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
