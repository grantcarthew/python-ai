from lib.ai.print import print_line
from lib.definitions import AI_HISTORY_PATH
from rich import print as rprint
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.styles import Style
import sys

session = PromptSession(history=FileHistory(AI_HISTORY_PATH))

def initial_message():
    try:
        print_line()
        rprint('[cyan]Type a message to start a chat[/]')
        rprint('[cyan]Type a file path to send the file contents[/]')
        rprint('[cyan]Multiline input enabled[/]')
        print_line()
        bottom_toolbar = 'ESCAPE then ENTER to submit | CTRL + SHIFT + V to paste'
        return session.prompt(
            '> ',
            multiline=True,
            prompt_continuation='> ',
            mouse_support=True,
            bottom_toolbar=bottom_toolbar,
            auto_suggest=AutoSuggestFromHistory())
    except KeyboardInterrupt:
        sys.exit(0)
