import urllib.request, json, sys
payload = {
    "topic": "CBSE Class 8 science: The Invisible Living World: Beyond Our Naked Eye",
    "num_questions": 2,
    "difficulty": None
}
req = urllib.request.Request('http://127.0.0.1:8000/api/mcq/cbse', data=json.dumps(payload).encode('utf-8'), headers={'Content-Type':'application/json'})
try:
    with urllib.request.urlopen(req, timeout=20) as r:
        print('STATUS', r.status)
        print(r.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print('HTTPERROR', e.code, e.reason)
    try:
        body = e.read().decode('utf-8')
        print('BODY:', body)
    except Exception:
        pass
except Exception as e:
    print('ERROR', e)
    import traceback; traceback.print_exc()
