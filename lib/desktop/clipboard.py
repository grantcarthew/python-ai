import subprocess
import rich
import pyperclip

def send_to_clipboard(text):
    try:
        pyperclip.copy(text)
    except:
        rich.print('[red]Unable to send content to the clipboard[/]')

