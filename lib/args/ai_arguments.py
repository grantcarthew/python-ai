from argparse import ArgumentParser, RawDescriptionHelpFormatter
from pathlib import Path
from typing import Any, Dict, Union
from lib.openai.prompts import get_prompt_first_match, get_prompt_match
from rich import print as rprint
import sys


def list_type_check(list_type: str) -> Union[bool, str]:
    if list_type.lower() in 'models':
        return 'models'
    if list_type.lower() in 'prompts':
        return 'prompts'
    return True


def parse_logic_bias_input(input_str: str) -> Dict[int, int]:
    key_value_pairs = input_str.split(',')
    return {int(pair.split(':')[0]): int(pair.split(':')[1]) for pair in key_value_pairs}


def argument_parser() -> Dict[str, Union[bool, str, Path]]:
    pwd = Path(__file__).parent
    description = (pwd / 'ai_help/description.txt').resolve().read_text()
    epilog = (pwd / 'ai_help/epilog.txt').resolve().read_text()

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
    parser.add_argument('-s', '--synchronous', action='store_true',
                        help='Use synchronous calls to OpenAI')
    parser.add_argument('-c', '--change-model', action='store_true',
                        help='Select GPT model used')
    parser.add_argument('--temperature', type=float, default=0,
                        help='Set the GPT temperature')
    parser.add_argument('--presence-penalty', type=float, default=0,
                        help='Set the GPT presence penalty')
    parser.add_argument('--frequency-penalty', type=float, default=0,
                        help='Set the GPT frequency penalty')
    parser.add_argument('--logit-bias', type=dict, default=None,
                        help='Pass a logit bias to the GPT model')

    args = parser.parse_args()
    argflags = {
        'change_model': False,
        'edit': False,
        'file': False,
        'frequency_penalty': 0,
        'interactive': False,
        'list': False,
        'logit_bias': {},
        'presence_penalty': 0,
        'prompt': False,
        'query': False,
        'synchronous': False,
        'temperature': 0,
        'verbose': False,
    }

    def range_check(name, value, min, max):
        if value > max or value < min:
            rprint(f'Error: {name} must be between {min} and {max}')
            sys.exit(1)

    if args.change_model:
        argflags['change_model'] = True
    if args.interactive:
        argflags['interactive'] = True
    if args.synchronous:
        argflags['synchronous'] = True
    if args.verbose:
        argflags['verbose'] = True
    range_check('temperature', args.temperature, 0, 2)
    range_check('presence_penalty', args.presence_penalty, -2, 2)
    range_check('frequency_penalty', args.frequency_penalty, -2, 2)
    argflags['temperature'] = args.temperature
    argflags['presence_penalty'] = args.presence_penalty
    argflags['frequency_penalty'] = args.frequency_penalty
    if args.logit_bias:
        argflags['logit_bias'] = parse_logic_bias_input(args.logit_bias)

    commands_length = len(args.command)
    commands = args.command.copy()

    if commands_length < 1:
        return argflags
    if commands[0].lower() == 'edit':
        argflags['edit'] = True
        return argflags
    if commands[0].lower() == 'list':
        if commands_length > 1:
            argflags['list'] = list_type_check(commands[1])
            return argflags
        argflags['list'] = True
        return argflags

    prompt = get_prompt_match(commands[0])
    if len(prompt) > 0:
        argflags['prompt'] = prompt
        commands.pop(0)

    # If command is a file, read its contents
    # If command is not a file, save it as the query
    for arg_string in commands:
        # Filesystem error management
        # Ignoring some errors and displaying unknown errors
        # All errors are non-blocking
        file_error = False
        try:
            if Path(arg_string).is_file():
                argflags['file'] = Path(arg_string)
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

        argflags['query'] = arg_string

    return argflags
