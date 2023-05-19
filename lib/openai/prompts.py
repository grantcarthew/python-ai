from lib.definitions import AI_PROMPTS_PATH
from pathlib import Path
from pick import pick
from typing import Optional
import os
import rich
import sys
from rich.console import Console
from rich.table import Table


def get_prompt_content(prompt_name: str) -> Optional[str]:
    footer_path = (AI_PROMPTS_PATH / 'footer.md')
    prompt_file = (AI_PROMPTS_PATH / f'{prompt_name}.md')
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
    prompts = list()
    for prompt in AI_PROMPTS_PATH.glob('**/*.md'):
        prompts.append(str(prompt.relative_to(AI_PROMPTS_PATH)).replace('.md', ''))
    return sorted(prompts)


def get_prompt_first_match(filter):
    if not filter:
        return None
    return next((p for p in list_prompts() if filter in p), None)

def get_prompt_match(filter):
    print(filter)
    if not filter:
        return list()

    results = [p for p in list_prompts() if filter in p]
    if len(results) < 1 and '/' in filter:
        filter = filter.split('/')[0]
        results = [p for p in list_prompts() if filter in p]
    return results

def get_prompts_path():
    return AI_PROMPTS_PATH

def show_prompt_list():
    table = Table()
    table.add_column('[cyan]Prepared Prompts[/]',
                     style='magenta', no_wrap=True)
    for p in list_prompts():
        table.add_row(p)
    rich.print(table)

