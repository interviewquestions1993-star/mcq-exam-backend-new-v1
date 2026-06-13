import json
import urllib.request

print('CHECK_START')
try:
    r = urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=5)
    print('HEALTH', r.status, r.read().decode())
except Exception as e:
    print('HEALTH_ERROR', repr(e))

try:
    payload = json.dumps({'topic': 'Math', 'num_questions': 1}).encode('utf-8')
    req = urllib.request.Request(
        'http://127.0.0.1:8000/api/mcq/generate',
        data=payload,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    r = urllib.request.urlopen(req, timeout=10)
    print('MCQ', r.status, r.read().decode())
except Exception as e:
    print('MCQ_ERROR', repr(e))
