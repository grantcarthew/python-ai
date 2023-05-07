from rich.console import Console
from rich.rule import Rule
from rich import print as rprint
import sys
from typing import List

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


def print_verbose(model_name, messages, flags, commands, parameters, prompt_name, tokens):
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
    print_messages(messages)




def print_command_help(command_list: List[dict], interactive: bool = False) -> None:
    if interactive:
        rprint(f'[cyan] Type "/" to enter a command[/]')
    rprint(f'[cyan] Available commands:[/]')
    for command in command_list:
        rprint(f'[cyan]   {command["name"]} - {command["description"]}[/]')

def print_messages(messages: List[dict]):
    if len(messages) == 0:
        rprint(f'[magenta]No chat messages to display[/]')
    for part in messages:
        rprint(f'[magenta]  Role: {part["role"]}[/]')
        if part['role'] == 'user':
            rprint(f'[cyan]    {part["content"]}[/]')
        else:
            rprint(f'[white]    {part["content"]}[/]')
    print_line()
