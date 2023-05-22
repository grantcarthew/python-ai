import sys
from rich import print as rprint
from rich.color import Color
from lib import config
from lib.ai import terminal
from lib.openai import text
from lib.ai import io
from lib.ai import user_input
from lib.ai import command_handler
from lib.ai import messages
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import WordCompleter


def interactive_session(flags, commands, parameters):
    terminal.print_interactive_title()
    call_api = True
    while True:
        model_name = config.get_text_model_name()
        if flags['debug']:
            rprint(f'   model: {model_name}')
            rprint(f'call_api: {call_api}')
            rprint(f'messages: {messages.chat}')
        if len(messages.chat) > 0 and messages.chat[-1]['role'] == 'user' and call_api:
            terminal.print_line()
            response = text.call_gpt_async(model_name, messages.chat, parameters)
            messages.add_assistant_content(response['content'])
            terminal.print_line()
        call_api = True
        try:
            command_items = command_handler.get_commands(interactive=True)
            command_names = [f'/{c["name"]}' for c in command_items]
            command_completer = WordCompleter(command_names, ignore_case=True)
            user_message = user_input.interactive_prompt(command_completer)
        except KeyboardInterrupt:
            sys.exit(0)

        # No message entered, user just hit ENTER
        if not user_message:
            call_api = False
            continue

        # Alternate options for commands
        # A single ? or / or the word help
        if len(user_message) > 0 and messages.is_help_message(user_message):
            user_message = '/help'
        # VIM quit
        if user_message == ':q':
            user_message = '/exit'

        # A forward slash indicates a command rather than a message
        if user_message.lower().startswith('/') or user_message.lower().startswith(':'):
            call_api = command_handler.action(command_data=user_message[1:], interactive=True)
            continue
        messages.add_user_content(user_message)


def passive_session(flags, commands, parameters) -> dict:
    model_name = config.get_text_model_name()
    session_data = {
        'finish_reason': None,
        'content': None,
        'tokens': {
            'prompt': 0,
            'completion': 0,
            'total': 0
        }
    }

    if flags['synchronous'] or flags['verbose']:
        response = text.call_gpt_sync(model_name, messages.chat, parameters)
        session_data['finish_reason'] = response['choices'][0]['finish_reason']
        session_data['tokens']['prompt'] = response['usage']['prompt_tokens']
        session_data['tokens']['completion'] = response['usage']['completion_tokens']
        session_data['tokens']['total'] = response['usage']['total_tokens']
        session_data['content'] = response['choices'][0]['message']['content']
    else:
        response = text.call_gpt_async(model_name, messages.chat, parameters)
        session_data['finish_reason'] = response['finish_reason']
        session_data['content'] = response['content']

    if flags['debug']:
        rprint(response)
        rprint(session_data)
    return session_data


def finish_reason_check(finish_reason) -> bool:
    if finish_reason == 'stop':
        return True
    known_reasons = {
        'length': 'Incomplete model output due to max_tokens parameter or token limit',
        'content_filter': 'Omitted content due to a flag from our content filters',
        'null': 'API response still in progress or incomplete'
    }
    if finish_reason in known_reasons.keys():
        rprint(
            f'[red]Finish Reason: {finish_reason} | {known_reasons[finish_reason]}[/]')
    else:
        rprint(
            f'[red]Model output stopped for an unknown reason: {finish_reason}[/]')
