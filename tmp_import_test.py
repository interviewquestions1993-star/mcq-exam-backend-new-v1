import sys
sys.path.insert(0, r'd:\AI-Exam-preparer-v1')
import importlib
modules = [
    ('langchain_community.document_loaders', 'UnstructuredPDFLoader'),
    ('langchain_text_splitters', 'RecursiveCharacterTextSplitter'),
    ('langchain_ollama', 'OllamaEmbeddings'),
    ('langchain_chroma', 'Chroma'),
]
for mod, name in modules:
    print('IMPORTING', mod)
    try:
        m = importlib.import_module(mod)
        getattr(m, name)
        print(mod, 'OK')
    except Exception as e:
        print(mod, 'ERROR', e)
