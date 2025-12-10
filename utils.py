"""
Utility functions and helpers for the Sai Baba Guidance Chatbot.
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime


def validate_file_path(file_path: str, must_exist: bool = False) -> bool:
    """
    Validate a file path.
    
    Args:
        file_path: Path to validate
        must_exist: If True, file must exist
    
    Returns:
        True if valid, False otherwise
    """
    try:
        path = Path(file_path)
        if must_exist:
            return path.exists() and path.is_file()
        return True
    except Exception:
        return False


def validate_directory(dir_path: str, create: bool = False) -> bool:
    """
    Validate a directory path.
    
    Args:
        dir_path: Directory path to validate
        create: If True, create directory if it doesn't exist
    
    Returns:
        True if valid/created, False otherwise
    """
    try:
        path = Path(dir_path)
        if not path.exists():
            if create:
                path.mkdir(parents=True, exist_ok=True)
                return True
            return False
        return path.is_dir()
    except Exception:
        return False


def get_file_extension(file_path: str) -> str:
    """
    Get file extension from path.
    
    Args:
        file_path: Path to file
    
    Returns:
        File extension (lowercase, without dot)
    """
    return Path(file_path).suffix.lower().lstrip('.')


def list_files_by_extension(directory: str, extensions: List[str]) -> List[str]:
    """
    List all files in directory with specific extensions.
    
    Args:
        directory: Directory to search
        extensions: List of extensions (without dots)
    
    Returns:
        List of file paths
    """
    dir_path = Path(directory)
    if not dir_path.exists():
        return []
    
    files = []
    for ext in extensions:
        files.extend(dir_path.glob(f"**/*.{ext}"))
    
    return [str(f) for f in files]


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters.
    
    Args:
        filename: Original filename
    
    Returns:
        Sanitized filename
    """
    # Remove invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace spaces with underscores
    sanitized = sanitized.replace(' ', '_')
    # Remove multiple underscores
    sanitized = re.sub(r'_+', '_', sanitized)
    return sanitized.strip('_')


def format_timestamp(dt: datetime = None) -> str:
    """
    Format timestamp for logging.
    
    Args:
        dt: Datetime object (uses current time if None)
    
    Returns:
        Formatted timestamp string
    """
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
    
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def extract_metadata_from_document(doc_path: str) -> Dict[str, Any]:
    """
    Extract metadata from document path.
    
    Args:
        doc_path: Path to document
    
    Returns:
        Dictionary with metadata
    """
    path = Path(doc_path)
    metadata = {
        "filename": path.name,
        "extension": path.suffix.lower(),
        "size_bytes": path.stat().st_size if path.exists() else 0,
        "modified_time": datetime.fromtimestamp(path.stat().st_mtime).isoformat() if path.exists() else None
    }
    return metadata


def count_words(text: str) -> int:
    """
    Count words in text.
    
    Args:
        text: Text to count words in
    
    Returns:
        Word count
    """
    return len(text.split())


def estimate_tokens(text: str, chars_per_token: int = 4) -> int:
    """
    Estimate token count for text.
    
    Args:
        text: Text to estimate
        chars_per_token: Average characters per token
    
    Returns:
        Estimated token count
    """
    return len(text) // chars_per_token


class PerformanceTimer:
    """Context manager for timing operations."""
    
    def __init__(self, operation_name: str = "Operation"):
        self.operation_name = operation_name
        self.start_time = None
        self.end_time = None
    
    def __enter__(self):
        self.start_time = datetime.now()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = datetime.now()
        duration = (self.end_time - self.start_time).total_seconds()
        print(f"{self.operation_name} completed in {duration:.2f} seconds")
        return False
    
    @property
    def duration(self) -> float:
        """Get duration in seconds."""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0
