import openai
import os
import rich
import sys
from datetime import datetime
from lib.openai.models import get_latest_model
from lib.openai.prompts import get_prompt_content
import json



def call_gpt_async(model: str, messages: list, parameters: dict) -> dict:
    # rich.print(messages)
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=parameters['temperature'],
        frequency_penalty=parameters['frequency_penalty'],
        presence_penalty=parameters['presence_penalty'],
        logit_bias=parameters['logit_bias'],
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
    except Exception as err:
        rich.print(f'[red]Error:[/] {err}')

    # rich.print(''.join(json.dumps(collected_chunks)))
    full_reply_content = ''.join(collected_content)
    finish_reason = collected_chunks[-1]['choices'][0]['finish_reason']

    return {'content': full_reply_content, 'finish_reason': finish_reason}


def call_gpt_sync(model: str, messages: list, parameters: dict) -> dict:
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=parameters['temperature'],
            frequency_penalty=parameters['frequency_penalty'],
            presence_penalty=parameters['presence_penalty'],
            logit_bias=parameters['logit_bias'],
        )
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as err:
        rich.print(f'[red]Error:[/] {err}')

    return response


def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo":
        print("Warning: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301")
    elif model == "gpt-4":
        print(
            "Warning: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.")
        return num_tokens_from_messages(messages, model="gpt-4-0314")
    elif model == "gpt-3.5-turbo-0301":
        # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_message = 4
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif model == "gpt-4-0314":
        tokens_per_message = 3
        tokens_per_name = 1
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens


