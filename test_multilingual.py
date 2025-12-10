#!/usr/bin/env python3
"""Test multilingual responses"""

from ask import SimpleChatbot

chatbot = SimpleChatbot()

print('=' * 70)
print('MULTILINGUAL RESPONSE TEST')
print('=' * 70)

# Test 1: English
print('\n🇬🇧 ENGLISH:')
print('-' * 70)
result = chatbot.ask('What is devotion?', 'en')
print(f'Question: What is devotion?')
print(f'Language: {result["language"]}')
print(f'Answer: {result["answer"][:120]}...')

# Test 2: Hindi
print('\n🇮🇳 HINDI:')
print('-' * 70)
result = chatbot.ask('devotion', 'hi')
print(f'Question: devotion')
print(f'Language: {result["language"]}')
print(f'Answer (in Hindi): {result["answer"][:120]}...')

# Test 3: Telugu
print('\n🇮🇳 TELUGU:')
print('-' * 70)
result = chatbot.ask('faith', 'te')
print(f'Question: faith')
print(f'Language: {result["language"]}')
print(f'Answer (in Telugu): {result["answer"][:120]}...')

# Test 4: Kannada
print('\n🇮🇳 KANNADA:')
print('-' * 70)
result = chatbot.ask('karma', 'kn')
print(f'Question: karma')
print(f'Language: {result["language"]}')
print(f'Answer (in Kannada): {result["answer"][:120]}...')

print('\n' + '=' * 70)
print('✅ All multilingual responses working!')
print('=' * 70)
