import os
import platform
import subprocess
from typing import Optional

def open_file_explorer(path: Optional[str] = None) -> None:
    if path is None:
        path = os.getcwd()

    system = platform.system()

    if system == 'Windows':
        subprocess.run(['explorer', path])
    elif system == 'Linux':
        subprocess.run(['xdg-open', path])
    elif system == 'Darwin':
        subprocess.run(['open', path])
    else:
        raise NotImplementedError(f'Unsupported platform: {system}')

def open_vscode(path: Optional[str] = None) -> None:
    try:
        subprocess.check_call(['code', path])
    except:
        open_file_explorer(path)
