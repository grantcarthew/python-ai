from lib import config
from lib.ai import io
from lib.ai import terminal
from lib.openai import models
from lib.definitions import AI_HISTORY_PATH
from rich import print as rprint
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.styles import Style
from prompt_toolkit.shortcuts import confirm
from pick import pick
import sys
from rich.color import Color
import tkinter as tk
from tkinter import filedialog

true_color = Color.parse('cyan').get_truecolor()
hex_color = f'#{true_color[0]:02x}{true_color[1]:02x}{true_color[2]:02x}'
style = Style.from_dict({'': hex_color})
session = PromptSession(
    '> ',
    prompt_continuation='> ',
    history=FileHistory(AI_HISTORY_PATH),
    style=style,
    complete_while_typing=True,
    mouse_support=False,
    auto_suggest=AutoSuggestFromHistory()
)


def interactive_prompt(command_completer) -> PromptSession:
    return session.prompt(completer=command_completer)


def initial_message():
    try:
        rprint('[cyan]Type a message to start a chat[/]')
        rprint('[cyan]Type a file path to send the file contents[/]')
        rprint('[cyan]Multiline input enabled[/]')
        terminal.print_line()
        bottom_toolbar = 'ESCAPE then ENTER to submit | CTRL + SHIFT + V to paste'
        return session.prompt(multiline=True, mouse_support=True, bottom_toolbar=bottom_toolbar)
    except KeyboardInterrupt:
        sys.exit(0)


def choose_saved_chat(filter: str = None):
    title = 'Choose a saved chat to load:'
    saved_chats = io.list_saved_chats(filter)
    if len(saved_chats) == 1:
        return saved_chats[0]
    if len(saved_chats) < 1:
        title = f'No chat matches filter {filter} | {title}'
        saved_chats = io.list_saved_chats()
    saved_chat = pick(saved_chats, title, indicator='>')[0]
    return saved_chat


def saved_chat_file_name():
    try:
        rprint('[cyan]Type a file name for saving this chat:[/]')
        terminal.print_line()
        return session.prompt()
    except KeyboardInterrupt:
        sys.exit(0)

def get_file_path() -> str:
    rprint(f'Type in the file path:')
    try:
        return session.prompt()
    except KeyboardInterrupt:
        sys.exit(0)


def get_directory_path() -> str:
    rprint(f'Type in the directory path:')
    try:
        return session.prompt()
    except KeyboardInterrupt:
        sys.exit(0)


def launch_file_browser() -> str:
    try:
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        file_path = filedialog.askopenfilename()
        return file_path
    except:
        return get_file_path()


def launch_directory_browser() -> str:
    try:
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        directory_path = filedialog.askdirectory()
        return directory_path
    except:
        return get_directory_path()

def change_text_model() -> None:
    current_model = config.get_text_model_name()
    rprint("Do you with to change the Text Model?")
    change_model = confirm()
    if change_model:
        chosen_model = models.choose_model(current_model)
        config.set_text_model_name(chosen_model)
    terminal.print_title()

