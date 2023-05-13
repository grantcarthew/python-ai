from rich.console import Console
from rich.rule import Rule
from rich import print as rprint
import sys
from typing import List
from rich import print
from rich.table import Table
from lib.ai import messages


console = Console()
console_stderr = Console(file=sys.stderr)


def print_line(to_stderr: bool = False):
    if to_stderr:
        console_stderr.print(Rule(style='blue'))
        return
    console.print(Rule(style='blue'))


def print_title(model_name, to_stderr: bool = False):
    print_line(to_stderr)
    title = f'[cyan]ChatGPT | {model_name}[/]'
    if to_stderr:
        rprint(title, file=sys.stderr)
    else:
        rprint(title)
    print_line(to_stderr)


def print_verbose(model_name, flags, commands, parameters, prompt_name, tokens):
    rprint('[bold yellow]Session Details[/]')
    print_line()
    rprint('Command line arguments:')
    print_line()
    rprint('Flag arguments:')
    rprint(flags)
    print_line()
    rprint('Command arguments:')
    rprint(commands)
    print_line()
    rprint('Parameter arguments:')
    rprint(parameters)
    print_line()
    rprint('[yellow]Metadata[/]')
    print_line()
    rprint(f'[magenta]Model: [cyan]{model_name}[/]')
    rprint(f'[magenta]Prompt: [cyan]{prompt_name}[/]')
    if tokens:
        rprint(f'[magenta]Tokens:[/]')
        rprint(f'[magenta]  Prompt: [cyan]{tokens["prompt"]}[/]')
        rprint(f'[magenta]  Completion: [cyan]{tokens["completion"]}[/]')
        rprint(f'[magenta]  Total: [cyan]{tokens["total"]}[/]')
    print_line()
    rprint('[yellow]Messages[/]')
    print_line()
    print_messages()




def print_command_help(command_list: List[dict], interactive: bool = False) -> None:
    title='Available Commands'
    if interactive:
        title += " (type '/' to enter commands)"

    table = Table(title=title)

    table.add_column('Command', justify='left', style='cyan', no_wrap=True)
    # table.add_column('Options', justify='right', style='magenta')
    table.add_column('Description', justify='left', style='green')
    for command in command_list:
        table.add_row(f'{command["name"]} {command["option_help"]}', command['description'])
    print(table)
    print_line()


def print_not_a_command(user_message: str) -> None:
    rprint(f'[red]This is not a command: {user_message}[/]')
    print_line()


def print_messages():
    if len(messages.chat) == 0:
        rprint(f'[magenta]No chat messages to display[/]')
    for part in messages.chat:
        rprint(f'[magenta]  Role: {part["role"]}[/]')
        if part['role'] == 'user':
            rprint(f'[cyan]    {part["content"]}[/]')
        else:
            rprint(f'[white]    {part["content"]}[/]')
    print_line()

def print_chat_saved(file_name):
    rprint(f'Chat saved: {file_name}')
    print_line()

def print_save_help():
    title='Save Command Options'
    table = Table(title=title)

    table.add_column('Command', justify='left', style='cyan', no_wrap=True)
    table.add_column('Description', justify='left', style='green')
    table.add_row(f'/save', 'Save the current chat under the name "default"')
    table.add_row(f'/save \[save-name]', 'Save the current chat under the supplied name')
    table.add_row(f'/save help', 'Display this help message')
    print(table)
    rprint('[magenta]Examples:[/]')
    rprint('[green]This example will save the chat under the name cooking:[/]')
    rprint('[cyan]/save cooking[/]')
    rprint('[green]This example will save the chat under a directory or category:[/]')
    rprint('[cyan]/save recipe/curried egg[/]')
    rprint('[green]Just using the save command will save the chat under the name "default":[/]')
    rprint('[cyan]/save[/]')
    print_line()