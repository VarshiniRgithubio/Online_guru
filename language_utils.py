"""
Language detection and handling utilities for multilingual support.
Supports English, Hindi, Telugu, and Kannada.
"""

from typing import Optional
from langdetect import detect, LangDetectException
from loguru import logger

from config import settings


# Language code mappings
LANGUAGE_NAMES = {
    "en": "English",
    "hi": "Hindi",
    "te": "Telugu",
    "kn": "Kannada"
}

# Langdetect to ISO 639-1 mapping
LANGDETECT_TO_ISO = {
    "en": "en",
    "hi": "hi",
    "te": "te",
    "kn": "kn"
}


class LanguageDetector:
    """Handles language detection for multilingual text."""
    
    def __init__(self):
        """Initialize language detector."""
        self.supported_languages = settings.supported_languages
        self.default_language = settings.default_language
    
    def detect_language(self, text: str) -> str:
        """
        Detect the language of input text.
        
        Args:
            text: Input text to detect language
        
        Returns:
            ISO 639-1 language code (en, hi, te, kn)
        """
        if not text or not text.strip():
            logger.warning("Empty text provided, using default language")
            return self.default_language
        
        try:
            detected = detect(text)
            
            # Map to ISO code
            iso_code = LANGDETECT_TO_ISO.get(detected, detected)
            
            # Check if supported
            if iso_code in self.supported_languages:
                logger.info(f"Detected language: {LANGUAGE_NAMES.get(iso_code, iso_code)}")
                return iso_code
            else:
                logger.warning(
                    f"Detected language '{iso_code}' not supported, "
                    f"using default: {self.default_language}"
                )
                return self.default_language
                
        except LangDetectException as e:
            logger.warning(f"Language detection failed: {str(e)}, using default")
            return self.default_language
        except Exception as e:
            logger.error(f"Unexpected error in language detection: {str(e)}")
            return self.default_language
    
    def get_language_name(self, lang_code: str) -> str:
        """
        Get full language name from code.
        
        Args:
            lang_code: ISO 639-1 language code
        
        Returns:
            Full language name
        """
        return LANGUAGE_NAMES.get(lang_code, lang_code)
    
    def is_supported_language(self, lang_code: str) -> bool:
        """
        Check if a language is supported.
        
        Args:
            lang_code: ISO 639-1 language code
        
        Returns:
            True if supported, False otherwise
        """
        return lang_code in self.supported_languages


def get_language_specific_prompt(language: str) -> str:
    """
    Get language-specific instruction for the AI model.
    
    Args:
        language: ISO 639-1 language code
    
    Returns:
        Language instruction string
    """
    instructions = {
        "en": "Respond in English.",
        "hi": "हिंदी में उत्तर दें। (Respond in Hindi.)",
        "te": "తెలుగులో ప్రతిస్పందించండి। (Respond in Telugu.)",
        "kn": "ಕನ್ನಡದಲ್ಲಿ ಪ್ರತಿಕ್ರಿಯಿಸಿ। (Respond in Kannada.)"
    }
    
    return instructions.get(language, instructions["en"])


def format_multilingual_response(answer: str, language: str) -> str:
    """
    Format response with language-specific enhancements.
    
    Args:
        answer: The answer text
        language: ISO 639-1 language code
    
    Returns:
        Formatted answer
    """
    # Ensure proper formatting based on language
    answer = answer.strip()
    
    # Add any language-specific formatting if needed
    if language in ["hi", "te", "kn"]:
        # Ensure proper Unicode normalization for Indic scripts
        import unicodedata
        answer = unicodedata.normalize('NFC', answer)
    
    return answer
