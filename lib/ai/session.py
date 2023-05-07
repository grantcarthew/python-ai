import sys
from rich import print as rprint
from rich.color import Color
from lib.ai import terminal
from lib.openai import text
from lib.definitions import AI_HISTORY_PATH
from lib.ai import io
from lib.ai import user_input
from lib.ai import command_handler
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import WordCompleter


def interactive_session(model_name, messages, flags, commands, parameters):
    terminal.print_title(model_name)
    command_handler.help(interactive=True)
    terminal.print_line()
    call_api = True
    while True:
        if flags['debug']:
            rprint(f'messages: {messages}')
            rprint(f'call_api: {call_api}')
        if len(messages) > 0 and messages[-1]['role'] == 'user' and call_api:
            response = text.call_gpt_async(model_name, messages, parameters)
            messages.append(
                {'role': 'assistant', 'content': response['content']})
            terminal.print_line()
        call_api = True
        try:
            command_items = command_handler.get_commands(interactive=True)
            command_names = [f'/{c["name"]}' for c in command_items]
            command_completer = WordCompleter(command_names, ignore_case=True)
            user_message = user_input.interactive_prompt(command_completer)
            terminal.print_line()
        except KeyboardInterrupt:
            sys.exit(0)

        # No message entered, user just hit ENTER
        if not user_message:
            call_api = False
            continue

        # Alternate options for displaying the command help
        # A single ? or / or the word help
        if len(user_message) == 1:
            if user_message.startswith('?') or user_message.startswith('/'):
                user_message = '/help'
        if user_message == 'help':
            user_message = '/help'

        # A forward slash indicates a command rather than a message
        if user_message.lower().startswith('/'):
            result = command_handler.action(
                command_data=user_message[1:], model_name=model_name, messages=messages, interactive=True)
            messages = result['messages']
            call_api = result['call_api']
            if result['continue']:
                continue

        messages.append({'role': 'user', 'content': user_message})


def passive_session(model_name, messages, flags, commands, parameters) -> dict:
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
        response = text.call_gpt_sync(model_name, messages, parameters)
        session_data['finish_reason'] = response['choices'][0]['finish_reason']
        session_data['tokens']['prompt'] = response['usage']['prompt_tokens']
        session_data['tokens']['completion'] = response['usage']['completion_tokens']
        session_data['tokens']['total'] = response['usage']['total_tokens']
        session_data['content'] = response['choices'][0]['message']['content']
    else:
        response = text.call_gpt_async(model_name, messages, parameters)
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
