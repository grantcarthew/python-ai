from argparse import ArgumentParser, RawDescriptionHelpFormatter
from pathlib import Path
from typing import Any, Dict, Union
from lib.openai.prompts import get_prompt_first_match, get_prompt_match
from rich import print as rprint
import argparse
import sys


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

    parser.add_argument('-i', '--interactive', action='store_true',
                        help='Does not exit after the first response')
    parser.add_argument('-f', '--file', type=Path,
                        help='A file you will to supply with your query')
    parser.add_argument('-l', '--load', nargs='?', const=True, default=argparse.SUPPRESS,
                        help='Load a saved chat')
    parser.add_argument('-m', '--model', nargs='?', const=True, default=argparse.SUPPRESS,
                        help='Set the GPT model used')
    parser.add_argument('-e', '--edit', action='store_true',
                        help='Opens the prepared prompts for editing')
    parser.add_argument('-p', '--prompt-list', action='store_true',
                        help='List the prepared prompts')
    parser.add_argument('--config', action='store_true',
                        help='Runs the configuration wizard')
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
    parser.add_argument('--verbose', action='store_true',
                        help='Shows metadata (synchronous forced)')
    parser.add_argument('--debug', action='store_true',
                        help='Enables debug output')
    parser.add_argument('prompt', nargs='?',
                        help='The name of a prompt or part thereof')
    parser.add_argument(
        'query', nargs='?', help='The question, request, or query you have')

    args = parser.parse_args()

    load = False
    if 'load' in args:
        load = args.load

    model = False
    if 'model' in args:
        model = args.model

    file = False
    if 'file' in args:
        file = args.file

    flags = {
        'config': args.config,
        'debug': args.debug,
        'edit': args.edit,
        'file': file,
        'interactive': args.interactive,
        'load': load,
        'model': model,
        'synchronous': args.synchronous,
        'verbose': args.verbose,
    }

    parameters = {
        'frequency_penalty': 0,
        'logit_bias': {},
        'presence_penalty': 0,
        'temperature': 0
    }

    query = args.query

    range_check('temperature', args.temperature, 0, 2)
    range_check('presence_penalty', args.presence_penalty, -2, 2)
    range_check('frequency_penalty', args.frequency_penalty, -2, 2)
    parameters['temperature'] = args.temperature
    parameters['presence_penalty'] = args.presence_penalty
    parameters['frequency_penalty'] = args.frequency_penalty
    if args.logit_bias:
        parameters['logit_bias'] = parse_logic_bias_input(
            args.logit_bias)

    prompt_list = get_prompt_match(args.prompt)

    if flags['file']:
        # Filesystem error management
        # Ignoring some errors and displaying unknown errors
        # All errors are non-blocking
        file_error = False
        try:
            if Path(flags['file']).is_file():
                flags['file'] = Path(flags['file'])
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

    return (flags, parameters, prompt_list, query)
