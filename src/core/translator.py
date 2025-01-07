from deep_translator import GoogleTranslator
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
from typing import Dict
import logging
import re

logger = logging.getLogger(__name__)

class TranslationService:
    def __init__(self):
        self._translators = {}
        # Common Portuguese gaming abbreviations and slang
        self._pt_patterns = [
            r'\b(vc|voce)\b',  # você (you)
            r'\b(mt|mto|muito)\b',  # muito (very/much)
            r'\b(tmb|tb|tambem)\b',  # também (also)
            r'\bmano\b',  # brother/dude
            r'\b(blz|beleza)\b',  # beleza (okay/cool)
            r'\b(flw|falou)\b',  # falou (bye)
            r'\b(qq|qualquer)\b',  # qualquer (any)
            r'\b(pvp|pve)\b',  # gaming terms
            r'\b(cls|classe)\b',  # classe (class)
            r'\b(bg|boa game)\b',  # good game
            r'\b(cmd|comendo)\b',  # eating/consuming
            r'\b(fds|fim de semana)\b',  # weekend
        ]
        self._pt_pattern = re.compile('|'.join(self._pt_patterns), re.IGNORECASE)
        
    def _is_likely_portuguese(self, text: str) -> bool:
        """
        Check if text contains common Portuguese gaming slang/abbreviations
        """
        return bool(self._pt_pattern.search(text))

    def detect_language(self, text: str) -> str:
        """
        Detect language of input text with improved handling of Portuguese gaming slang
        """
        try:
            # First check for Portuguese gaming patterns
            if self._is_likely_portuguese(text):
                return 'pt'
            
            # Use langdetect with fallback options
            try:
                detected = detect(text)
                # If detected as Romanian but contains Portuguese patterns, override to Portuguese
                if detected == 'ro' and self._is_likely_portuguese(text):
                    return 'pt'
                return detected
            except LangDetectException:
                # If detection fails, check for Portuguese patterns again
                if self._is_likely_portuguese(text):
                    return 'pt'
                logger.warning("Language detection failed, defaulting to English")
                return 'en'
                
        except Exception as e:
            logger.error(f"Language detection error: {e}")
            return 'en'

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
    
    def _get_translator(self, source_lang: str, target_lang: str) -> GoogleTranslator:
        """Get or create translator for language pair"""
        key = f"{source_lang}-{target_lang}"
        if key not in self._translators:
            self._translators[key] = GoogleTranslator(
                source=source_lang,
                target=target_lang
            )
        return self._translators[key]