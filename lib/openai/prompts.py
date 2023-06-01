from lib.definitions import AI_PROMPTS_PATH
from pathlib import Path
from pick import pick
from typing import Optional
import os
import sys
from rich import print as rprint
from rich.console import Console
from rich.table import Table


def get_prompt_content(prompt_name: str) -> Optional[str]:
    footer_path = (AI_PROMPTS_PATH / 'footer.md')
    prompt_file = (AI_PROMPTS_PATH / f'{prompt_name}.md')

    prompt_content = None

    if not prompt_file.is_file():
        return prompt_content

    with prompt_file.open('r') as f:
        prompt_content = f.read()

    if footer_path.is_file():
        if "## footer" in prompt_content.lower():
            with footer_path.open('r') as f:
                prompt_content += f'\n\n{f.read()}'
    else:
        rprint(
            f'[red][Error] The following prompt document is missing: {footer_path}[/]')
        sys.exit(1)

    return prompt_content


def list_prompts():
    prompts = list()
    for prompt in AI_PROMPTS_PATH.glob('**/*.md'):
        prompts.append(str(prompt.relative_to(
            AI_PROMPTS_PATH)).replace('.md', ''))
    return sorted(prompts)


def get_prompt_first_match(filter):
    if not filter:
        return None
    return next((p for p in list_prompts() if filter in p), None)


def get_prompt_match(filter):
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
    rprint(table)
