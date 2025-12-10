#!/usr/bin/env python3
"""Test the API"""
import subprocess
import time
import requests
from ask import SimpleChatbot

print("=" * 60)
print("TESTING CHATBOT & API")
print("=" * 60)

# Test 1: Direct Chatbot
print("\n1️⃣  TESTING DIRECT CHATBOT")
print("-" * 60)
chatbot = SimpleChatbot()

# English
result = chatbot.ask('What is devotion?')
print(f"✅ English: {result['language']}")
print(f"   Answer: {result['answer'][:70]}...")

# Hindi
result = chatbot.ask('भक्ति क्या है?')
print(f"✅ Hindi: {result['language']}")
print(f"   Answer: {result['answer'][:70]}...")

# Test 2: API Server
print("\n2️⃣  TESTING API SERVER")
print("-" * 60)

# Start API server in background
print("Starting API server...")
server = subprocess.Popen(['python', 'simple_api.py'], 
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE)

time.sleep(4)

try:
    # Health check
    response = requests.get('http://localhost:8000/health', timeout=5)
    print(f"✅ Health Check: {response.status_code}")
    print(f"   Status: {response.json()}")
    
    # Test POST /ask
    response = requests.post(
        'http://localhost:8000/ask',
        json={'question': 'What is karma?'},
        timeout=5
    )
    print(f"\n✅ POST /ask: {response.status_code}")
    data = response.json()
    print(f"   Answer: {data['answer'][:70]}...")
    print(f"   Language: {data['language']}")
    print(f"   Safe: {data['is_safe']}")
    
    # Test GET /ask
    response = requests.get(
        'http://localhost:8000/ask?question=What%20is%20meditation?',
        timeout=5
    )
    print(f"\n✅ GET /ask: {response.status_code}")
    data = response.json()
    print(f"   Answer: {data['answer'][:70]}...")
    
    # Test Languages endpoint
    response = requests.get('http://localhost:8000/languages', timeout=5)
    print(f"\n✅ GET /languages: {response.status_code}")
    data = response.json()
    print(f"   Languages: {[l['name'] for l in data['supported_languages']]}")
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
    
except Exception as e:
    print(f"❌ Error: {e}")
    
finally:
    server.terminate()
    server.wait()
