from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent
DEBUG_DIR = ROOT_DIR / 'debug_images'
LOG_DIR = ROOT_DIR / 'logs'

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

TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
OCR_CONFIG = r'--psm 6 --oem 1'

HOTKEYS = {
    'select_area': 'ctrl+alt+x',
    'toggle_overlay': 'ctrl+alt+c',
    'clear_fields': 'ctrl+alt+d'
}

SAVE_DEBUG_IMAGES = False