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

session = PromptSession(history=FileHistory(AI_HISTORY_PATH))


def interactive_session(model_name, messages, flags, commands, parameters):
    terminal.print_title(model_name)
    terminal.print_command_help(interactive=True)
    terminal.print_line()
    true_color = Color.parse('cyan').get_truecolor()
    hex_color = f'#{true_color[0]:02x}{true_color[1]:02x}{true_color[2]:02x}'
    style = Style.from_dict({'': hex_color})
    call_api = True
    while True:
        if flags['debug']:
            rprint(f'messages: {messages}')
            rprint(f'call_api: {call_api}')
        if len(messages) > 0  and messages[-1]['role'] == 'user' and call_api:
            response = text.call_gpt_async(model_name, messages, parameters)
            messages.append(
                {'role': 'assistant', 'content': response['content']})
            terminal.print_line()
        call_api = True
        try:
            user_message = session.prompt('> ', style=style)
            terminal.print_line()
        except KeyboardInterrupt:
            sys.exit(0)

        # A forward slash indicates a command rather than a message
        if user_message.lower().startswith('/'):
            if len(user_message) == 1:
                user_message = '/help'
            result = command_handler.action(command_data=user_message[1:], messages=messages, interactive=True)
            messages = result['messages']
            call_api = result['call_api']
            if result['continue']:
                continue

        if user_message.lower() == 'reset':
            messages = list()
            call_api = False
            rprint(f'[cyan] Session Reset | {model_name}')
            continue
        if user_message.lower() == 'save':
            io.save_chat('test_name', messages)
            rprint('Chat saved')
            call_api = False
            continue
        if user_message.lower() == 'load' or user_message.lower().startswith('load '):
            filter = None
            if user_message.lower().startswith('load '):
                words = user_message.lower().split()
                if len(words) > 2:
                    pass # TODO
                if len(words) == 2:
                   filter = words[1]
            user_input.choose_saved_chat(filter)
            messages = io.load_chat('test_name')
            rprint('Chat loaded')
            call_api = False
            continue
        if user_message.lower() == 'help':
            terminal.print_command_help(interactive=True)
            terminal.print_line()
            call_api = False
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
        rprint(f'[red]Finish Reason: {finish_reason} | {known_reasons[finish_reason]}[/]')
    else:
        rprint(
            f'[red]Model output stopped for an unknown reason: {finish_reason}[/]')

