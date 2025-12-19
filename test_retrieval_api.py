from fastapi.testclient import TestClient
from retrieval_api import app

client = TestClient(app)

print('Calling GET /health')
res = client.get('/health')
print(res.status_code)
print(res.json())

print('\nCalling POST /ask')
res = client.post('/ask', json={'question':'What does Sai Baba teach about devotion?','language':'en'})
print(res.status_code)
print(res.json())
