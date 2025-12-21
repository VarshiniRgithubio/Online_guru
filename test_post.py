import requests, json, sys

try:
    r = requests.post('http://127.0.0.1:8000/ask', json={'question':'What is devotion?'}, timeout=30)
    print('STATUS', r.status_code)
    print(json.dumps(r.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print('ERROR', e)
    sys.exit(1)
