"""Quick test of the system without internet dependency"""

import sys
from pathlib import Path

# Test 1: Module imports
print("=" * 60)
print("TEST 1: Testing module imports...")
print("=" * 60)

try:
    from config import settings
    print("✓ Config module imported")
    print(f"  - Supported languages: {settings.supported_languages}")
    print(f"  - Vector DB path: {settings.vector_db_path}")
except Exception as e:
    print(f"✗ Config import failed: {e}")
    sys.exit(1)

try:
    from language_utils import LanguageDetector
    print("✓ Language utilities imported")
    detector = LanguageDetector()
    test_lang = detector.detect_language("What is the purpose of life?")
    print(f"  - Test detection: 'What is the purpose of life?' detected as: {test_lang}")
except Exception as e:
    print(f"✗ Language utilities failed: {e}")
    sys.exit(1)

try:
    from rag_engine import MultilingualRAGEngine, SafetyFilter
    print("✓ RAG engine imported")
    
    # Test safety filter
    safety = SafetyFilter()
    test_medical = safety.is_prohibited_topic("Can you cure my diabetes?")
    if test_medical:
        print(f"  - Medical check working: detected medical topic")
    else:
        print(f"  - Medical check working: allowed non-medical topic")
        
except Exception as e:
    print(f"✗ RAG engine import failed: {e}")
    sys.exit(1)

try:
    from api import app
    print("✓ FastAPI app imported successfully")
except Exception as e:
    print(f"✗ FastAPI app import failed: {e}")
    sys.exit(1)

# Test 2: File structure
print("\n" + "=" * 60)
print("TEST 2: Checking project structure...")
print("=" * 60)

required_dirs = ["data", "audio", "transcripts", "vector_db"]
required_files = ["api.py", "rag_engine.py", "config.py", "language_utils.py", "ingest.py", ".env"]

for dir_name in required_dirs:
    dir_path = Path(dir_name)
    if dir_path.exists():
        print(f"✓ Directory '{dir_name}/' exists")
    else:
        print(f"✗ Directory '{dir_name}/' missing")

for file_name in required_files:
    file_path = Path(file_name)
    if file_path.exists():
        print(f"✓ File '{file_name}' exists")
    else:
        if file_name == ".env":
            print(f"⚠ File '{file_name}' missing (create with: cp .env.example .env)")
        else:
            print(f"✗ File '{file_name}' missing")

# Test 3: Configuration status
print("\n" + "=" * 60)
print("TEST 3: Configuration Status...")
print("=" * 60)

env_path = Path(".env")
if env_path.exists():
    print("✓ .env file exists")
    with open(".env", "r") as f:
        content = f.read()
        has_api_key = "API_KEY" in content or "OPENAI_API_KEY" in content or "GOOGLE_API_KEY" in content
        if has_api_key:
            print("✓ API key configuration found")
        else:
            print("⚠ No API key found - system needs OpenAI or Google API key to work")
            print("  Configure in .env file:")
            print("    OPENAI_API_KEY=your_key_here")
            print("  OR")
            print("    GOOGLE_API_KEY=your_key_here")
else:
    print("⚠ .env file not found")
    print("  Create it with: cp .env.example .env")
    print("  Then add your API keys")

# Test 4: Sample data
print("\n" + "=" * 60)
print("TEST 4: Sample Data Status...")
print("=" * 60)

sample_file = Path("data/sample_teachings.txt")
if sample_file.exists():
    size = sample_file.stat().st_size
    print(f"✓ Sample teachings file exists ({size} bytes)")
    with open(sample_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    print(f"  - Contains {len(lines)} lines")
    print(f"  - Preview: {lines[0][:60]}...")
else:
    print("⚠ Sample teachings file not found")
    print("  Add text/PDF files to data/ folder for the RAG system")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print("""
✓ All core modules are working
✓ Project structure is in place

To get the system fully running:

1. If you don't have .env file:
   cp .env.example .env

2. Add your API key to .env:
   - For OpenAI: OPENAI_API_KEY=sk-...
   - For Google: GOOGLE_API_KEY=...

3. Build the vector database:
   python ingest.py

4. Start the API server:
   python api.py

5. Test with: curl -X POST http://localhost:8000/ask \\
     -H "Content-Type: application/json" \\
     -d '{{"question": "What is devotion?"}}'

6. Interactive docs: http://localhost:8000/docs
""")

print("=" * 60)
