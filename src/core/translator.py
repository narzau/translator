from deep_translator import GoogleTranslator
from typing import Dict
import logging

logger = logging.getLogger(__name__)

class TranslationService:
    def __init__(self):
        """Initialize the translation service"""
        self._translators = {}

    def translate(self, text: str, target_lang: str) -> Dict[str, str]:
        """
        Translate text from English to target language
        
        Args:
            text: English text to translate
            target_lang: Target language code
            
        Returns:
            Dictionary with original text and translation
        """
        if not text.strip():
            return {
                'text': '',
                'translation': ''
            }
        
        try:
            translator = self._get_translator('en', target_lang)
            translation = translator.translate(text)
            
            return {
                'text': text,
                'translation': translation
            }
            
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            raise
    
    def _get_translator(self, source_lang: str, target_lang: str) -> GoogleTranslator:
        """Get or create translator for language pair"""
        key = f"{source_lang}-{target_lang}"
        if key not in self._translators:
            self._translators[key] = GoogleTranslator(
                source=source_lang,
                target=target_lang
            )
        return self._translators[key]