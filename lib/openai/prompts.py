from lib.definitions import AI_PROMPTS_PATH
from pathlib import Path
from pick import pick
from typing import Optional
import os
import rich
import sys
prompts_root = Path(AI_PROMPTS_PATH)


def get_prompt_content(prompt_name: str) -> Optional[str]:
    footer_path = prompts_root / 'footer.md'
    prompt_file = prompts_root / f'{prompt_name}.md'
    footer_content = ''

    if not footer_path.is_file():
        rich.print(
            f'[red][Error] The following prompt document is missing: {footer_path}[/]')
        sys.exit(1)
    with footer_path.open('r') as f:
        footer_content = f.read()

    if not prompt_file.is_file():
        return None
    with prompt_file.open('r') as f:
        return f'{f.read()}\n{footer_content}'


def list_prompts():
    return sorted([p.stem for p in prompts_root.glob('*.md')])


def get_prompt_first_match(filter):
    if not filter:
        return None
    return next((p for p in list_prompts() if filter in p), None)


def get_prompts_path():
    return prompts_root
