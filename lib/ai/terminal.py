from rich.console import Console
from rich.rule import Rule
from rich import print as rprint
import sys

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


def print_verbose_details(model_name, messages, flags, commands, parameters, prompt_name, tokens):
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
    for part in messages:
        rprint(f'[magenta]Role: {part["role"]}[/]')
        rprint(f'[cyan]{part["content"]}[/]')
        print_line()




def print_command_help(interactive: bool = False):
    if interactive:
        rprint(f'[cyan] Type "/" to enter a command[/]')
    rprint(f'[cyan] Available commands:[/]')
    rprint(f'[cyan]   config - Change command configuration[/]')
    rprint(f'[cyan]   edit   - Edit prepared prompts[/]')
    if interactive:
        rprint(f'[cyan]   export - Export current chat[/]')
    rprint(f'[cyan]   help   - Show this help[/]')
    rprint(f'[cyan]   list   - List modules or prompts[/]')
    rprint(f'[cyan]   load   - Load a saved chat[/]')
    if interactive:
        rprint(f'[cyan]   reset  - Drop memory from this chat[/]')
        rprint(f'[cyan]   save   - Save this chat[/]')

