import os
import sys
import uvicorn


def ensure_project_root_on_path():
    # Ensure the repository root (parent of this package) is on sys.path
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if root not in sys.path:
        sys.path.insert(0, root)
    return root


if __name__ == '__main__':
    root = ensure_project_root_on_path()
    print('STARTING UVICORN; project root added to sys.path:', root)
    # Allow overriding lifespan behavior via env var. Default to 'on' so FastAPI startup events run
    lifespan = os.getenv('UVICORN_LIFESPAN', 'on')
    port = int(os.getenv('BACKEND_PORT', '8000'))
    uvicorn.run('backendv1.main:app', host='127.0.0.1', port=port, log_level='debug', lifespan=lifespan)
