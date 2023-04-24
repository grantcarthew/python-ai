from os import path
from pathlib import Path

AI_VERSION = '1.0.0'
AI_CONFIG_PATH = str(Path.home() / '.config' / 'aiconfig')
AI_CACHE_PATH = str(Path.home() / '.config' / 'aicache')
AI_PROMPTS_PATH = str(Path(__file__).resolve().parent.parent / 'prompts')
