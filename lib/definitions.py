from pathlib import Path

AI_VERSION = '1.0.0'
AI_CONFIG_ROOT = Path.home() / '.config' / 'ai'
AI_CONFIG_PATH = AI_CONFIG_ROOT / 'config'
AI_CACHE_PATH = AI_CONFIG_ROOT / 'cache'
AI_HISTORY_PATH = AI_CONFIG_ROOT / 'history'
AI_SAVE_PATH = AI_CONFIG_ROOT / 'chats'
AI_PROMPTS_PATH = Path(__file__).resolve().parent.parent / 'prompts'

# Create the paths and files if they don't exist
AI_CONFIG_ROOT.parent.mkdir(parents=True, exist_ok=True)
AI_CONFIG_ROOT.mkdir(parents=True, exist_ok=True)
AI_HISTORY_PATH.touch(exist_ok=True)
AI_SAVE_PATH.mkdir(parents=True, exist_ok=True)
AI_PROMPTS_PATH.mkdir(parents=True, exist_ok=True)