import traceback

try:
    from backendv1.ingest import get_embeddings
    emb = get_embeddings()
    print('OK', type(emb))
except Exception:
    traceback.print_exc()