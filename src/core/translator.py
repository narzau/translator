from deep_translator import GoogleTranslator
from langdetect import detect
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class TranslationService:
    def __init__(self):
        self._translators = {}
    
    def translate(self, text: str, target_lang: str = 'en') -> Dict[str, str]:
        """
        Translate text to target language
        
        Args:
            text: Text to translate
            target_lang: Target language code
            
        Returns:
            Dictionary with original text, translation, and language info
        """
        if not text.strip():
            return {
                'text': '',
                'translation': '',
                'source_lang': None,
                'target_lang': target_lang
            }
        
        try:
            source_lang = self.detect_language(text)
            
            # Don't translate if already in target language
            if source_lang == target_lang:
                return {
                    'text': text,
                    'translation': text,
                    'source_lang': source_lang,
                    'target_lang': target_lang
                }
            
            translator = self._get_translator(source_lang, target_lang)
            translation = translator.translate(text)
            
            return {
                'text': text,
                'translation': translation,
                'source_lang': source_lang,
                'target_lang': target_lang
            }
            
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            raise
    
    def detect_language(self, text: str) -> str:
        """Detect language of input text"""
        try:
            return detect(text)
        except:
            logger.warning("Language detection failed, defaulting to English")
            return 'en'
    
    def _get_translator(self, source_lang: str, target_lang: str) -> GoogleTranslator:
        """Get or create translator for language pair"""
        key = f"{source_lang}-{target_lang}"
        if key not in self._translators:
            self._translators[key] = GoogleTranslator(
                source=source_lang,
                target=target_lang
            )
        return self._translators[key]