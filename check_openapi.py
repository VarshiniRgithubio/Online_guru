from api import app
import json
spec = app.openapi()
post = spec.get('paths', {}).get('/ask', {}).get('post', {})
responses = post.get('responses', {})
print(json.dumps(responses.get('200', responses), indent=2))
