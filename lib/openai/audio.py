import openai
import os
import rich
from datetime import datetime
from models import get_latest_model


def call_whisper(messages: list, temperature: int = 0) -> dict:
    MODEL = get_latest_model('gpt')
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=messages,
        temperature=0,
    )

    return response

def rewrite_document(document: str) -> dict:
    messages=[
        {"role": "system", "content": "You are an expert assistant that reviews text looking for any errors and fixing them."},
        {"role": "user", "content": f"Rewrite the following text speech to text document. Do not change the meaning of the text. Do not reply to this prompt with anything except the updated text: '{document}'"}
    ]
    return call_gpt(messages)



openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = get_latest_model('whisper')
audio_file = open(temp_mp3_file, "rb")
transcript = openai.Audio.transcribe("whisper-1", audio_file)

rich.print('[magenta]JSON object from Open AI speech to text[/]')
rich.print(transcript)

rich.print('[megenta]Transcribed text follows:[/]')
rich.print(f'[cyan]{transcript.text}[/]')

