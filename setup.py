#!/usr/bin/env python
"""
Setup script for the Sai Baba Guidance Chatbot.
Run this script to initialize the project and verify installation.
"""

import sys
import subprocess
from pathlib import Path
from loguru import logger


def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        logger.error(f"Python 3.9+ required. You have Python {version.major}.{version.minor}")
        return False
    logger.success(f"Python version: {version.major}.{version.minor}.{version.micro}")
    return True


def create_directories():
    """Create necessary project directories."""
    directories = [
        "data",
        "audio",
        "transcripts",
        "vector_db"
    ]
    
    logger.info("Creating project directories...")
    for directory in directories:
        path = Path(directory)
        path.mkdir(exist_ok=True)
        logger.info(f"  ✓ {directory}/")
    
    logger.success("Directories created")


def check_env_file():
    """Check if .env file exists."""
    env_path = Path(".env")
    example_path = Path(".env.example")
    
    if not env_path.exists():
        if example_path.exists():
            logger.warning(".env file not found")
            logger.info("Please create .env file from .env.example:")
            logger.info("  1. Copy .env.example to .env")
            logger.info("  2. Add your API keys")
            return False
        else:
            logger.error(".env.example not found")
            return False
    
    logger.success(".env file exists")
    return True


def verify_installation():
    """Verify that all required packages are installed."""
    logger.info("Verifying package installation...")
    
    required_packages = [
        "fastapi",
        "uvicorn",
        "langchain",
        "faiss-cpu",
        "sentence-transformers",
        "pypdf",
        "whisper",
        "torch",
        "loguru",
        "python-dotenv"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            logger.info(f"  ✓ {package}")
        except ImportError:
            logger.warning(f"  ✗ {package} not installed")
            missing_packages.append(package)
    
    if missing_packages:
        logger.warning(f"Missing packages: {', '.join(missing_packages)}")
        logger.info("Run: pip install -r requirements.txt")
        return False
    
    logger.success("All packages installed")
    return True


def display_next_steps():
    """Display next steps for the user."""
    print("\n" + "="*60)
    print("SETUP COMPLETE - Next Steps:")
    print("="*60)
    print()
    print("1. Configure your API keys:")
    print("   - Edit .env file")
    print("   - Add OPENAI_API_KEY or GOOGLE_API_KEY")
    print()
    print("2. Add your data:")
    print("   - Place PDF/TXT files in the 'data/' folder")
    print("   - (Optional) Place audio files in 'audio/' folder")
    print()
    print("3. Process audio (if you have audio files):")
    print("   python speech_to_text.py")
    print()
    print("4. Build the vector database:")
    print("   python ingest.py")
    print()
    print("5. Start the API server:")
    print("   python api.py")
    print()
    print("6. Access the API documentation:")
    print("   http://localhost:8000/docs")
    print()
    print("="*60)


def main():
    """Main setup function."""
    logger.info("Starting Sai Baba Guidance Chatbot Setup")
    print()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    print()
    
    # Create directories
    create_directories()
    print()
    
    # Check .env file
    env_exists = check_env_file()
    print()
    
    # Verify installation
    packages_ok = verify_installation()
    print()
    
    # Display next steps
    if packages_ok and env_exists:
        logger.success("Setup verification complete!")
        display_next_steps()
    else:
        logger.warning("Setup incomplete. Please address the issues above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
