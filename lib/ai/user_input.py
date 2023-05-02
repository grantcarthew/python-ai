from lib.ai.print import print_line
from lib.definitions import AI_HISTORY_PATH
from rich import print as rprint
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style

session = PromptSession(history=FileHistory(AI_HISTORY_PATH))

def initial_message():
    try:
        print_line()
        rprint('[cyan]Type a message to start a chat[/]')
        rprint('[cyan]Type a file path to send the file contents[/]')
        rprint('[cyan]Multiline input enabled[/]')
        print_line()
        rprint('[white]ESCAPE then ENTER to submit:[/]')
        return session.prompt('> ', multiline=True)
    except KeyboardInterrupt:
        sys.exit(0)
