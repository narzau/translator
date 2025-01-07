import json
from pathlib import Path
from typing import Dict, Any
from src.config.constants import ROOT_DIR

class Settings:
    def __init__(self):
        self.settings_file = ROOT_DIR / 'settings.json'
        self._settings = self._load_settings()
    
    def _load_settings(self) -> Dict[str, Any]:
        if self.settings_file.exists():
            with open(self.settings_file, 'r') as f:
                return json.load(f)
        return self._get_default_settings()
    
    def _get_default_settings(self) -> Dict[str, Any]:
        return {
            'tesseract_path': r'C:\Program Files\Tesseract-OCR\tesseract.exe',
            'default_source_lang': 'pt',
            'default_target_lang': 'en',
            'save_debug_images': False,
            'overlay_opacity': 0.8,
            'overlay_position': {'x': 100, 'y': 100}
        }
    
    def save(self):
        with open(self.settings_file, 'w') as f:
            json.dump(self._settings, f, indent=4)
    
    @property
    def tesseract_path(self) -> str:
        return self._settings['tesseract_path']
    
    @property
    def default_source_lang(self) -> str:
        return self._settings['default_source_lang']
    
    @property
    def default_target_lang(self) -> str:
        return self._settings['default_target_lang']
    
    @property
    def save_debug_images(self) -> bool:
        return self._settings['save_debug_images']
    
    @property
    def overlay_opacity(self) -> float:
        return self._settings['overlay_opacity']
    
    @property
    def overlay_position(self) -> Dict[str, int]:
        return self._settings['overlay_position']