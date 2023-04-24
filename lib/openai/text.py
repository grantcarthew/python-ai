import openai
import os
import rich
import sys
from datetime import datetime
from lib.openai.models import get_latest_model
from lib.openai.prompts import get_prompt_content
import json


def call_gpt_async(model: str, messages: list, temperature: int = 0) -> dict:
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        stream=True
    )

    collected_chunks = []
    collected_content = []

    try:
        for chunk in response:
            collected_chunks.append(chunk)
            if 'content' in chunk['choices'][0]['delta']:
                chunk_content = chunk['choices'][0]['delta']['content']
                print(chunk_content, end='', flush=True)
                collected_content.append(chunk_content)
        print()
    except KeyboardInterrupt:
        print()
        sys.exit(0)
    except Exception as err:
        rich.print(f'[red]Error:[/] {err}')

    # rich.print(''.join(json.dumps(collected_chunks)))
    full_reply_content = ''.join(collected_content)
    finish_reason = collected_chunks[-1]['choices'][0]['finish_reason']

    return {'content': full_reply_content, 'finish_reason': finish_reason}


def call_gpt_sync(model: str, messages: list, temperature: int = 0) -> dict:
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature
        )
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as err:
        rich.print(f'[red]Error:[/] {err}')

    return response
