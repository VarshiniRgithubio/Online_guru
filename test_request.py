import time
import requests

# Wait a bit for the server to start
time.sleep(3)

url = "http://127.0.0.1:8000/ask"
payload = {"question": "What is devotion according to Sai Baba?"}

try:
    r = requests.post(url, json=payload, timeout=30)
    print(r.status_code)
    print(r.text)
except Exception as e:
    print('ERROR', e)
