import subprocess
import rich

def send_to_clipboard(text):
    try:
        subprocess.run(['xclip', '-selection', 'clipboard'], input=text.encode('utf-8'))
    except:
        rich.print('[red]Unable to send content to the clipboard[/]')

