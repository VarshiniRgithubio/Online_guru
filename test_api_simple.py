#!/usr/bin/env python3
"""Test API"""
import requests
import time
import subprocess
import sys

# Start server in background
print("Starting API server...")
server = subprocess.Popen([sys.executable, 'simple_api.py'], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL)

# Wait for server to start
time.sleep(5)

try:
    # Test 1: Health check
    print("\nTest 1: GET /health")
    print("-" * 50)
    r = requests.get('http://localhost:8000/health', timeout=5)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.json()}")
    
    # Test 2: Ask question
    print("\nTest 2: POST /ask (English)")
    print("-" * 50)
    r = requests.post('http://localhost:8000/ask', 
                     json={'question': 'What is devotion?'},
                     timeout=5)
    print(f"Status: {r.status_code}")
    data = r.json()
    print(f"Answer: {data['answer'][:80]}...")
    print(f"Language: {data['language']}")
    
    # Test 3: Hindi question
    print("\nTest 3: POST /ask (Hindi)")
    print("-" * 50)
    r = requests.post('http://localhost:8000/ask', 
                     json={'question': 'भक्ति क्या है?'},
                     timeout=5)
    print(f"Status: {r.status_code}")
    data = r.json()
    print(f"Language Detected: {data['language']}")
    print(f"Answer Preview: {str(data['answer'])[:80]}...")
    
    # Test 4: GET /ask
    print("\nTest 4: GET /ask?question=")
    print("-" * 50)
    r = requests.get('http://localhost:8000/ask?question=What%20is%20karma',
                    timeout=5)
    print(f"Status: {r.status_code}")
    data = r.json()
    print(f"Answer: {data['answer'][:80]}...")
    
    # Test 5: GET /languages
    print("\nTest 5: GET /languages")
    print("-" * 50)
    r = requests.get('http://localhost:8000/languages', timeout=5)
    print(f"Status: {r.status_code}")
    langs = r.json()['supported_languages']
    for lang in langs:
        print(f"  - {lang['code']}: {lang['name']}")
    
    print("\n" + "=" * 50)
    print("SUCCESS: All API tests passed!")
    print("=" * 50)
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    
finally:
    print("\nShutting down server...")
    server.terminate()
    server.wait()
    print("Done!")
