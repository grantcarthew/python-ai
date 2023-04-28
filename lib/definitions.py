import os
from pathlib import Path

AI_VERSION = '1.0.0'
AI_CONFIG_PATH = str(Path.home() / '.config' / 'aiconfig')
AI_CACHE_PATH = str(Path.home() / '.config' / 'aicache')
AI_HISTORY_PATH = str(Path.home() / '.config' / 'aihistory')
AI_PROMPTS_PATH = str(Path(__file__).resolve().parent.parent / 'prompts')

if not os.path.exists(AI_HISTORY_PATH):
    os.makedirs(os.path.dirname(AI_HISTORY_PATH), exist_ok=True)
    open(AI_HISTORY_PATH, 'a').close()
