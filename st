#!/usr/bin/python

import argparse
import openai
import os
import pyaudio
import rich
from rich.console import Console
import subprocess
import sys
import tempfile
import threading
import queue
import wave
from lib.openai.models import get_latest_model
from lib.openai.text import call_gpt_sync
console = Console()

description = """
Converts speech to text using the following steps:

- Records audio from the default mic
  - Press ENTER when you have finished recording
- Converts the wave file to mp3 format
- Sends the mp3 file to OpenAI for speech to text conversion
- Places the transcribed text on the clipboard
- Asks if you would like to submit it to ChatGPT
- If yes, ChatGPT will look for errors and rewrite it
- Places the updated text on the clipboard

"""
epilog = """

Example
-------------------------------------------------
This example will convert speech to text:
$ convert-speechtotext

"""
parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=description,
    epilog=epilog)
args = parser.parse_args()


def collect(que):
    msg = input()
    que.put(msg)


def send_to_clipboard(text):
    rich.print('[magenta]Putting the transcribed text on the clipboard[/]')
    subprocess.run(['xclip', '-selection', 'clipboard'],
                   input=text.encode('utf-8'))


def print_title(text):
    console.rule(f'[magenta]{text}[/]')


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1 if sys.platform == 'darwin' else 2
RATE = 44100
temp_wave_file = tempfile.mkstemp()[1] + '.wav'
temp_mp3_file = tempfile.mkstemp()[1] + '.mp3'

print_title('Convert Speech to Text')
rich.print(f'Temporary files WAV: {temp_wave_file} MP3: {temp_mp3_file}')

print_title('Recording the audio to a wave file')
with wave.open(temp_wave_file, 'wb') as wave_file:
    audio = pyaudio.PyAudio()
    wave_file.setnchannels(CHANNELS)
    wave_file.setsampwidth(audio.get_sample_size(FORMAT))
    wave_file.setframerate(RATE)

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True)

    que = queue.Queue()
    thread = threading.Thread(target=collect, args=[que])
    thread.start()

    rich.print('Recording...')
    rich.print("Press ENTER to finish")

    while thread.is_alive():
        wave_file.writeframes(stream.read(CHUNK))

    stream.close()
    audio.terminate()

print_title('Converting to mp3')
cmd = f'lame --preset insane {temp_wave_file} {temp_mp3_file}'
subprocess.call(cmd, shell=True)


print_title('Sending mp3 to Open AI')
openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = get_latest_model('whisper')
audio_file = open(temp_mp3_file, "rb")
transcript = openai.Audio.transcribe("whisper-1", audio_file)

rich.print('[magenta]JSON object from Open AI speech to text[/]')
rich.print(transcript)

rich.print('[megenta]Transcribed text follows:[/]')
rich.print(f'[cyan]{transcript.text}[/]')

send_to_clipboard(transcript.text)

print_title('Submit text to ChatGPT?')
while True:
    rich.print('[magenta]Submit this text to ChatGPT for re-write? [Y/n][/]')
    user_input = input().lower()
    if user_input in {"yes", "y", "", "default"}:
        break
    elif user_input in {"no", "n"}:
        print("Exiting...")
        exit()

if user_input in {"no", "n"}:
    rich.print('[magenta]Done![/]')
    sys.exit()

print_title('Sending text to ChatGPT')
response = rewrite_document(transcript.text)

rich.print('[magenta]JSON object from Open AI ChatGPT[/]')
rich.print(response)


rich.print('[magenta]Updated text follows[/]')
rich.print(f'[cyan]{response.choices[0].message.content}[/]')

send_to_clipboard(response.choices[0].message.content)

rich.print('[magenta]Done![/]')
