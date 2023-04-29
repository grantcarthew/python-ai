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
    parser.add_argument('-t', '--temperature', type=float, default=0,
                        help='Set the GPT temperature')

    args = parser.parse_args()
    argflags = {
        'change_model': False,
        'edit': False,
        'file': False,
        'interactive': False,
        'list': False,
        'prompt': False,
        'query': False,
        'synchronous': False,
        'temperature': 0,
        'verbose': False,
    }

    if args.change_model:
        argflags['change_model'] = True
    if args.interactive:
        argflags['interactive'] = True
    if args.synchronous:
        argflags['synchronous'] = True
    if args.verbose:
        argflags['verbose'] = True
    if args.temperature > 2 or args.temperature < 0:
        rprint('Error: Temperature must be between 0 and 2')
        sys.exit(1)
    else:
        argflags['temperature'] = args.temperature

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

    for arg_string in commands:
        if Path(arg_string).is_file():
            argflags['file'] = Path(arg_string)
            continue
        argflags['query'] = arg_string

    return argflags
