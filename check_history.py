import os
import sys
sys.path.insert(0, os.getcwd())

import main as m
print('FIREBASE_ENABLED=', m.FIREBASE_ENABLED)
print('FIRESTORE_HISTORY_COLLECTION=', m.FIRESTORE_HISTORY_COLLECTION)
print('FIREBASE_COLLECTION=', m.FIREBASE_COLLECTION)
print('save_ai_response=', m.save_ai_response is not None)
print('get_firestore_client=', m.get_firestore_client is not None)
client = m.get_firestore_client()
print('client=', client)
if client is not None:
    coll = client.collection(m.FIRESTORE_HISTORY_COLLECTION or m.FIREBASE_COLLECTION)
    try:
        docs = list(coll.limit(1).stream())
        print('docs_count=', len(docs))
        for d in docs:
            print('doc', d.id, d.to_dict())
    except Exception as exc:
        print('query failed:', type(exc).__name__, exc)
