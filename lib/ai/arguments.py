from argparse import ArgumentParser, RawDescriptionHelpFormatter
from pathlib import Path
from typing import Any, Dict, Union
from lib.openai.prompts import get_prompt_first_match, get_prompt_match
from lib.ai import terminal
from rich import print as rprint
import argparse
import sys


def list_type_check(list_type: str) -> Union[bool, str]:
    if list_type.lower() in 'models':
        return 'models'
    if list_type.lower() in 'prompts':
        return 'prompts'
    return True


def range_check(name, value, min, max):
    if value > max or value < min:
        rprint(f'Error: {name} must be between {min} and {max}')
        sys.exit(1)


def parse_logic_bias_input(input_str: str) -> Dict[int, int]:
    key_value_pairs = input_str.split(',')
    return {int(pair.split(':')[0]): int(pair.split(':')[1]) for pair in key_value_pairs}


def argument_parser() -> Dict[str, Union[bool, str, Path]]:
    pwd = Path(__file__).parent
    description = (pwd / 'help_description.txt').resolve().read_text()
    epilog = (pwd / 'help_epilog.txt').resolve().read_text()

    parser = ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter,
        description=description,
        epilog=epilog)

    parser.add_argument('command', nargs='*',
                        help='A variable number of values')
    parser.add_argument('-i', '--interactive', action='store_true',
                        help='Does not exit after the first response')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Shows metadata (synchronous forced)')
    parser.add_argument('-m', '--model', nargs='?', const=True, default=argparse.SUPPRESS,
                        help='Set the GPT model used')
    parser.add_argument('--synchronous', action='store_true',
                        help='Use synchronous calls to OpenAI')
    parser.add_argument('--temperature', type=float, default=0,
                        help='Set the GPT temperature')
    parser.add_argument('--presence-penalty', type=float, default=0,
                        help='Set the GPT presence penalty')
    parser.add_argument('--frequency-penalty', type=float, default=0,
                        help='Set the GPT frequency penalty')
    parser.add_argument('--logit-bias', type=dict, default=None,
                        help='Pass a logit bias to the GPT model')
    parser.add_argument('--debug', action='store_true',
                        help='Enables debug output')

    args = parser.parse_args()

    model = False
    if 'model' in args:
        model = args.model

    flags = {
        'model': model,
        'debug': args.debug,
        'interactive': args.interactive,
        'synchronous': args.synchronous,
        'verbose': args.verbose,
    }
    commands = {
        'config': False,
        'edit': False,
        'export': False,
        'file': False,
        'help': False,
        'list': False,
        'load': False,
        'prompt': False,
        'query': False,
        'save': False
    }
    parameters = {
        'frequency_penalty': 0,
        'logit_bias': {},
        'presence_penalty': 0,
        'temperature': 0
    }

    range_check('temperature', args.temperature, 0, 2)
    range_check('presence_penalty', args.presence_penalty, -2, 2)
    range_check('frequency_penalty', args.frequency_penalty, -2, 2)
    parameters['temperature'] = args.temperature
    parameters['presence_penalty'] = args.presence_penalty
    parameters['frequency_penalty'] = args.frequency_penalty
    if args.logit_bias:
        parameters['logit_bias'] = parse_logic_bias_input(
            args.logit_bias)

    command_count = len(args.command)
    command_list = args.command.copy()

    if command_count < 1:
        return (flags, commands, parameters)
    if command_list[0].lower() == 'config':
        commands['config'] = True
    if command_list[0].lower() == 'edit':
        commands['edit'] = True
        return (flags, commands, parameters)
    if command_list[0].lower() == 'export':
        commands['export'] = True
        return (flags, commands, parameters)
    if command_list[0].lower() == 'help':
        terminal.print_command_help()
        return (flags, commands, parameters)
    if command_list[0].lower() == 'list':
        if command_count > 1:
            commands['list'] = list_type_check(command_list[1])
            return (flags, commands, parameters)
        commands['list'] = True
        return (flags, commands, parameters)
        return (flags, commands, parameters)
    if command_list[0].lower() == 'load':
        commands['load'] = True
        return (flags, commands, parameters)

    prompt = get_prompt_match(command_list[0])
    if len(prompt) > 0:
        commands['prompt'] = prompt
        command_list.pop(0)

    # There may be 0 or more commands
    # If command is a file, read its contents
    # If command is not a file, save it as the query
    for arg_string in command_list:
        # Filesystem error management
        # Ignoring some errors and displaying unknown errors
        # All errors are non-blocking
        file_error = False
        try:
            if Path(arg_string).is_file():
                commands['file'] = Path(arg_string)
                continue
        except OSError as err:
            if 'File name too long' in str(err):
                # Ignoring file name too long, not a filesystem path
                pass
            else:
                file_error = err
        except Exception as err:
            file_error = err

        if file_error:
            rprint(f'[red]Non-blocking error:[/]')
            rprint(f'[red]{file_error}[/]')

        commands['query'] = arg_string

    return (flags, commands, parameters)
