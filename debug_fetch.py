import sys, os
import urllib.request, json

# Ensure workspace root is on sys.path so `import backendv1` works when run from project root
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from backendv1 import main
url = main.RAW_CBSE_MCQS_URL
print('URL:', url)
for hdr in (None, {'User-Agent':'python-urllib/3.14'}):
    try:
        if hdr:
            req = urllib.request.Request(url, headers=hdr)
            print('\nRequest with headers:', hdr)
            r = urllib.request.urlopen(req, timeout=15)
        else:
            print('\nRequest without headers')
            r = urllib.request.urlopen(url, timeout=15)
        raw = r.read()
        text = raw.decode('utf-8')
        print('STATUS', getattr(r,'status',None), 'LEN', len(raw))
        print('REPR first 200:', repr(text[:200]))
        print('JSON parse ok:', isinstance(json.loads(text), list))
    except Exception as e:
        print('ERROR', e)
        import traceback; traceback.print_exc()
