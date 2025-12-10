"""
Multilingual Speech-to-Text conversion module using OpenAI Whisper.
Supports English, Hindi, Telugu, and Kannada audio transcription.
"""

import os
import re
from pathlib import Path
from typing import List, Optional, Dict
import whisper
import torch
from pydub import AudioSegment
from loguru import logger

from config import settings


# Language code mapping
LANGUAGE_MAP = {
    "en": "english",
    "hi": "hindi",
    "te": "telugu",
    "kn": "kannada"
}


class MultilingualSpeechToTextConverter:
    """Handles multilingual audio file transcription using Whisper model."""
    
    def __init__(self, model_size: str = "base"):
        """
        Initialize the Whisper model for multilingual transcription.
        
        Args:
            model_size: Whisper model size (tiny, base, small, medium, large)
        """
        self.model_size = model_size
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Loading Whisper model '{model_size}' on device '{self.device}'")
        self.model = whisper.load_model(model_size, device=self.device)
        self.supported_languages = settings.supported_languages
        logger.info(f"Multilingual support enabled for: {', '.join(self.supported_languages)}")
        logger.success("Whisper model loaded successfully")
    
    def detect_language(self, audio_path: str) -> str:
        """
        Detect the language of an audio file.
        
        Args:
            audio_path: Path to the audio file
        
        Returns:
            Detected language code (en, hi, te, kn)
        """
        try:
            # Load audio and pad/trim it to fit 30 seconds
            audio = whisper.load_audio(audio_path)
            audio = whisper.pad_or_trim(audio)
            
            # Make log-Mel spectrogram and move to the same device as the model
            mel = whisper.log_mel_spectrogram(audio).to(self.model.device)
            
            # Detect the spoken language
            _, probs = self.model.detect_language(mel)
            detected_lang = max(probs, key=probs.get)
            
            # Map to supported languages
            if detected_lang in self.supported_languages:
                logger.info(f"Detected language: {detected_lang} ({LANGUAGE_MAP.get(detected_lang, detected_lang)})")
                return detected_lang
            else:
                logger.warning(f"Detected language {detected_lang} not in supported list, defaulting to English")
                return "en"
        except Exception as e:
            logger.error(f"Error detecting language: {str(e)}")
            return "en"
    
    def transcribe_audio(
        self, 
        audio_path: str, 
        language: Optional[str] = None,
        auto_detect: bool = True
    ) -> Dict[str, str]:
        """
        Transcribe a single audio file to text with language detection.
        
        Args:
            audio_path: Path to the audio file
            language: Language code (en, hi, te, kn). If None, auto-detect
            auto_detect: Whether to auto-detect language
        
        Returns:
            Dictionary with 'text' and 'language' keys
        """
        try:
            logger.info(f"Transcribing audio file: {audio_path}")
            
            # Detect language if not specified
            if language is None and auto_detect:
                language = self.detect_language(audio_path)
            elif language is None:
                language = settings.default_language
            
            # Ensure language is supported
            if language not in self.supported_languages:
                logger.warning(f"Language {language} not supported, using {settings.default_language}")
                language = settings.default_language
            
            # Transcribe
            result = self.model.transcribe(
                audio_path,
                language=language,
                task="transcribe",
                fp16=False  # Use fp32 for CPU compatibility
            )
            
            text = result["text"]
            detected_lang = result.get("language", language)
            
            logger.success(f"Transcription completed for: {audio_path} (Language: {detected_lang})")
            
            return {
                "text": text,
                "language": detected_lang
            }
        except Exception as e:
            logger.error(f"Error transcribing {audio_path}: {str(e)}")
            raise
    
    @staticmethod
    def clean_transcript(text: str, language: str = "en") -> str:
        """
        Clean transcribed text by removing timestamps, filler words, and noise.
        Preserves the original language.
        
        Args:
            text: Raw transcribed text
            language: Language code for language-specific cleaning
        
        Returns:
            Cleaned text
        """
        # Remove timestamps (e.g., [00:12:34])
        text = re.sub(r'\[\d+:\d+:\d+\]', '', text)
        text = re.sub(r'\d+:\d+:\d+', '', text)
        
        # Language-specific filler words
        fillers_by_lang = {
            "en": ['um', 'uh', 'er', 'ah', 'hmm', 'like', 'you know'],
            "hi": ['उम्', 'अह', 'हम्म', 'वो', 'यानी', 'मतलब'],
            "te": ['అమ్మో', 'ఓహో', 'ఉహూం'],
            "kn": ['ಅಮ್ಮೋ', 'ಓಹೋ']
        }
        
        fillers = fillers_by_lang.get(language, fillers_by_lang["en"])
        
        # Remove filler words (case-insensitive for English)
        if language == "en":
            for filler in fillers:
                pattern = r'\b' + re.escape(filler) + r'\b'
                text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Remove speaker labels (e.g., "Speaker 1:")
        text = re.sub(r'Speaker\s*\d+\s*:', '', text, flags=re.IGNORECASE)
        text = re.sub(r'स्पीकर\s*\d+\s*:', '', text)  # Hindi
        
        # Remove noise markers
        noise_markers = [
            '[inaudible]', '[music]', '[noise]', '[applause]', '[laughter]',
            '[अस्पष्ट]', '[संगीत]', '[शोर]'  # Hindi markers
        ]
        for marker in noise_markers:
            text = text.replace(marker, '')
        
        # Clean up punctuation
        text = re.sub(r'\s+([.,!?;:])', r'\1', text)
        
        # Trim whitespace
        text = text.strip()
        
        return text
    
    @staticmethod
    def convert_audio_format(input_path: str, output_path: str, format: str = "wav") -> str:
        """
        Convert audio file to a different format.
        
        Args:
            input_path: Path to input audio file
            output_path: Path to save converted file
            format: Target format (wav, mp3)
        
        Returns:
            Path to converted file
        """
        try:
            logger.info(f"Converting {input_path} to {format}")
            audio = AudioSegment.from_file(input_path)
            audio.export(output_path, format=format)
            logger.success(f"Converted to: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error converting audio format: {str(e)}")
            raise
    
    def process_audio_file(
        self,
        audio_path: str,
        output_txt_path: Optional[str] = None,
        language: Optional[str] = None,
        auto_detect: bool = True
    ) -> Dict[str, str]:
        """
        Process a single audio file: transcribe and clean.
        
        Args:
            audio_path: Path to audio file
            output_txt_path: Path to save cleaned transcript (optional)
            language: Language code (if known)
            auto_detect: Whether to auto-detect language
        
        Returns:
            Dictionary with 'text' and 'language'
        """
        # Transcribe
        result = self.transcribe_audio(audio_path, language, auto_detect)
        
        # Clean
        cleaned_text = self.clean_transcript(result["text"], result["language"])
        
        # Save if output path provided
        if output_txt_path:
            Path(output_txt_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_txt_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_text)
            logger.info(f"Cleaned transcript saved to: {output_txt_path}")
        
        return {
            "text": cleaned_text,
            "language": result["language"]
        }
    
    def process_audio_folder(
        self,
        audio_folder: Optional[str] = None,
        output_folder: Optional[str] = None,
        auto_detect: bool = True
    ) -> List[Dict[str, str]]:
        """
        Process all audio files in a folder with multilingual support.
        
        Args:
            audio_folder: Path to folder containing audio files
            output_folder: Path to save transcripts (saved to data folder)
            auto_detect: Whether to auto-detect language for each file
        
        Returns:
            List of dictionaries with transcript info
        """
        audio_folder = audio_folder or settings.audio_folder
        output_folder = output_folder or settings.data_folder  # Save to data folder
        
        audio_folder_path = Path(audio_folder)
        output_folder_path = Path(output_folder)
        output_folder_path.mkdir(parents=True, exist_ok=True)
        
        # Supported audio formats
        audio_extensions = ['.mp3', '.wav', '.m4a', '.flac', '.ogg']
        audio_files = [
            f for f in audio_folder_path.iterdir()
            if f.suffix.lower() in audio_extensions
        ]
        
        if not audio_files:
            logger.warning(f"No audio files found in {audio_folder}")
            return []
        
        logger.info(f"Found {len(audio_files)} audio files to process")
        
        transcript_info = []
        for audio_file in audio_files:
            try:
                output_txt = output_folder_path / f"{audio_file.stem}.txt"
                result = self.process_audio_file(
                    str(audio_file),
                    str(output_txt),
                    auto_detect=auto_detect
                )
                transcript_info.append({
                    "audio_file": str(audio_file),
                    "transcript_file": str(output_txt),
                    "language": result["language"]
                })
            except Exception as e:
                logger.error(f"Failed to process {audio_file}: {str(e)}")
                continue
        
        logger.success(f"Processed {len(transcript_info)} audio files successfully")
        
        # Print language distribution
        lang_counts = {}
        for info in transcript_info:
            lang = info["language"]
            lang_counts[lang] = lang_counts.get(lang, 0) + 1
        
        logger.info("Language distribution:")
        for lang, count in lang_counts.items():
            logger.info(f"  {LANGUAGE_MAP.get(lang, lang)}: {count} file(s)")
        
        return transcript_info


def main():
    """CLI entry point for multilingual speech-to-text conversion."""
    import sys
    
    logger.info("Starting multilingual speech-to-text conversion")
    
    if len(sys.argv) > 1:
        # Process specific file
        audio_path = sys.argv[1]
        converter = MultilingualSpeechToTextConverter(model_size="base")
        output_path = Path(settings.data_folder) / f"{Path(audio_path).stem}.txt"
        result = converter.process_audio_file(audio_path, str(output_path))
        logger.info(f"Language: {result['language']}")
    else:
        # Process entire folder
        converter = MultilingualSpeechToTextConverter(model_size="base")
        converter.process_audio_folder()
    
    logger.info("Multilingual speech-to-text conversion completed")


if __name__ == "__main__":
    main()
