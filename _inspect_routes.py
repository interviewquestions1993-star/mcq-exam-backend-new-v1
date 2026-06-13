import json
import urllib.request

url = 'http://127.0.0.1:8000/openapi.json'
try:
    r = urllib.request.urlopen(url, timeout=5)
    print('STATUS', r.status)
    data = json.loads(r.read().decode())
    print('PATHS')
    for path in data.get('paths', {}).keys():
        print(path)
except Exception as e:
    print('ERROR', repr(e))
