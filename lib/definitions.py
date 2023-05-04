import os
from pathlib import Path

AI_VERSION = '1.0.0'
AI_CONFIG_ROOT = Path.home() / '.config' / 'ai'
AI_CONFIG_PATH = str(AI_CONFIG_ROOT/ 'config')
AI_CACHE_PATH = str(AI_CONFIG_ROOT / 'cache')
AI_HISTORY_PATH = str(AI_CONFIG_ROOT / 'history')
AI_SAVE_PATH    = str(AI_CONFIG_ROOT / 'chats')
AI_PROMPTS_PATH = str(Path(__file__).resolve().parent.parent / 'prompts')

if not os.path.exists(AI_HISTORY_PATH):
    os.makedirs(os.path.dirname(AI_HISTORY_PATH), exist_ok=True)
    open(AI_HISTORY_PATH, 'a').close()

if not os.path.exists(AI_SAVE_PATH):
    os.makedirs(AI_SAVE_PATH, exist_ok=True)
