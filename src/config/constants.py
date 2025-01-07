import os
from pathlib import Path

# Application paths
ROOT_DIR = Path(__file__).parent.parent.parent
DEBUG_DIR = ROOT_DIR / 'debug_images'
LOG_DIR = ROOT_DIR / 'logs'

# Language settings
AVAILABLE_LANGUAGES = {
    'English': 'en',
    'Portuguese': 'pt',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Italian': 'it',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Chinese (Simplified)': 'zh-CN',
    'Russian': 'ru'
}

# OCR settings
TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
OCR_CONFIG = r'--psm 6 --oem 1'

# Hotkey configurations
HOTKEYS = {
    'select_area': 'ctrl+alt+x',
    'toggle_overlay': 'ctrl+alt+c',
    'clear_fields': 'ctrl+alt+d'
}

# Debug settings
SAVE_DEBUG_IMAGES = False