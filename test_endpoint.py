import urllib.request, json, time

def req(path, data=None):
    url = 'http://127.0.0.1:8000' + path
    headers = {'Content-Type': 'application/json'} if data else {}
    try:
        req = urllib.request.Request(url, data=data, headers=headers)
        with urllib.request.urlopen(req, timeout=20) as r:
            print(path, 'STATUS', r.status)
            print(r.read().decode('utf-8')[:4000])
    except Exception as e:
        print('ERROR', path, e)
        import traceback; traceback.print_exc()

if __name__ == '__main__':
    time.sleep(1)
    req('/health')
    req('/api/mcq/cbse', json.dumps({'topic': 'Science', 'num_questions': 1}).encode('utf-8'))
