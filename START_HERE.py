#!/usr/bin/env python3
"""
Complete guide showing all 3 ways to use the chatbot
"""

print("""
╔════════════════════════════════════════════════════════════════════╗
║         SAI BABA GUIDANCE CHATBOT - COMPLETE USAGE GUIDE           ║
╚════════════════════════════════════════════════════════════════════╝

🎉 Your chatbot is ready! Choose any method below to ask questions:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 METHOD 1: COMMAND LINE (Fastest - No Setup Needed!)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ask ANY question instantly from PowerShell:

    python ask.py "What is devotion?"

That's it! Get answer immediately.

Examples:

    python ask.py "What is faith?"
    python ask.py "What is the purpose of life?"
    python ask.py "What is service to others?"
    python ask.py "भक्ति क्या है?"           # Hindi - works too!
    python ask.py "జీవిత లక్ష్యం ఏమిటి?"     # Telugu - works too!

✅ BEST FOR: Quick questions, scripts, automation
⏱️  TIME TO USE: ~1 second

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 METHOD 2: INTERACTIVE CHAT (Like ChatGPT)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Keep asking questions conversationally:

    python ask.py

Then type your questions one by one:

    👉 Ask a question: What is devotion?
    ✨ Answer: Devotion is the path of love...
    
    👉 Ask a question: What is faith?
    ✨ Answer: Faith is trust in God...
    
    👉 Ask a question: quit
    ✨ Thank you...

✅ BEST FOR: Exploring topics, conversations
⏱️  TIME TO USE: ~2 seconds

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌐 METHOD 3: WEB BROWSER (Most User-Friendly)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Interactive documentation with beautiful UI:

Step 1: Start the API server (in PowerShell)

    python simple_api.py

You'll see:
    ✨ Starting server...
    📡 API running on: http://localhost:8000
    📖 Interactive docs: http://localhost:8000/docs

Step 2: Open your web browser

    http://localhost:8000/docs

Step 3: Ask questions using the interface

    - Click on "POST /ask" endpoint
    - Click "Try it out"
    - Enter your question:
      {
        "question": "What is devotion?",
        "language": "en"
      }
    - Click "Execute"
    - See the answer!

✅ BEST FOR: User-friendly interface, no coding needed
⏱️  TIME TO USE: ~5 seconds

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 COMPARISON TABLE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Method          | Setup     | Speed    | Ease      | Best For
──────────────────────────────────────────────────────────────────
CLI             | ✅ None   | ⚡ 1 sec | ⭐⭐⭐  | Quick Qs
Interactive     | ✅ None   | ⚡ 2 sec | ⭐⭐⭐  | Chats
Web Browser     | Server    | ⚡ 5 sec | ⭐⭐⭐  | UI
PowerShell      | Server    | ⚡ 3 sec | ⭐⭐   | Scripts
Python          | Server    | ⚡ 3 sec | ⭐⭐   | Apps
JavaScript      | Server    | ⚡ 3 sec | ⭐⭐⭐  | Web

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❓ FREQUENTLY ASKED QUESTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Q: Do I need to start a server first?
A: Only for Methods 3 & beyond. Methods 1 & 2 work immediately!

Q: Can I ask in different languages?
A: YES! The system auto-detects language. Try:
   python ask.py "भक्ति क्या है?" (Hindi)
   python ask.py "భక్తి అంటే ఏమిటి?" (Telugu)
   python ask.py "ಭಕ್ತಿ ಎಂದರೆ ಏನು?" (Kannada)

Q: What if I want better answers?
A: Add more teachings to data/ folder and run:
   python ingest.py

Q: Can I use this with my app?
A: YES! Use any of these methods for integration:
   - CLI: python ask.py "question"
   - API: http://localhost:8000/ask (JSON)
   - Python: import ask.py and call SimpleChatbot

Q: Is it free?
A: This version uses free sample teachings.
   For OpenAI/Google responses, add API keys to .env

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 QUICK START RIGHT NOW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Choose ONE:

1️⃣ INSTANT (No setup):
   python ask.py "What is devotion?"

2️⃣ INTERACTIVE (No setup):
   python ask.py

3️⃣ WEB UI (Requires server):
   Terminal 1: python simple_api.py
   Browser: http://localhost:8000/docs

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ TRY THESE QUESTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

python ask.py "What is devotion?"
python ask.py "What is faith?"
python ask.py "What is karma?"
python ask.py "What is meditation?"
python ask.py "What is truth?"
python ask.py "What is love?"
python ask.py "What is peace?"
python ask.py "What is the purpose of life?"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ EVERYTHING IS READY - START NOW!

For detailed documentation, see: HOW_TO_ASK.md
For API details, see: API_EXAMPLES.md
For system info, see: DEPLOY.md

Any questions? The chatbot is ready to help! 🙏

""")
