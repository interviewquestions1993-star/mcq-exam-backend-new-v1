from pathlib import Path
import sys

from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_community.vectorstores.utils import filter_complex_metadata

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
for path in (str(HERE), str(ROOT)):
    if path not in sys.path:
        sys.path.insert(0, path)

try:
    from backendv1.config import OLLAMA_BASE_URL
except ImportError:
    from config import OLLAMA_BASE_URL

# ========================= CONFIG =========================
BASE_DIR = Path(__file__).resolve().parent
PDF_FOLDER = BASE_DIR / "ncert_pdfs"          # Put your NCERT PDFs here
PERSIST_DIR = BASE_DIR / "chroma_db"          # Local Chroma vector store folder
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150
COLLECTION_NAME = "ncert_grade8"
# =======================================================

def get_embeddings():
    base_url = OLLAMA_BASE_URL.rstrip("/")
    if base_url.endswith("/v1"):
        base_url = base_url[: -len("/v1")]

    return OllamaEmbeddings(
        model="nomic-embed-text",
        base_url=base_url,
        validate_model_on_init=False,
    )


def ingest_pdfs():
    print(f"📂 Scanning folder: {PDF_FOLDER}")

    if not PDF_FOLDER.exists():
        PDF_FOLDER.mkdir(parents=True, exist_ok=True)
        print(f"Created folder {PDF_FOLDER}. Put your PDFs there and run again.")
        return

    documents = []
    pdf_files = list(PDF_FOLDER.rglob("*.pdf")) + list(PDF_FOLDER.rglob("*.PDF"))

    print(f"Scanning PDF folder: {PDF_FOLDER}")
    print(f"Found {len(pdf_files)} PDF files")

    for pdf_path in pdf_files:
        print(f"Processing: {pdf_path.name}")
        try:
            loader = UnstructuredPDFLoader(str(pdf_path), mode="elements")
            docs = loader.load()
            documents.extend(docs)
        except Exception as e:
            print(f"❌ Error with {pdf_path.name}: {e}")

    if not documents:
        print("No documents found!")
        return

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    splits = text_splitter.split_documents(documents)

    # Filter complex metadata to avoid Chroma validation errors
    splits = filter_complex_metadata(splits)

    print(f"Creating vector store with {len(splits)} chunks...")

    Chroma.from_documents(
        documents=splits,
        embedding=get_embeddings(),
        persist_directory=PERSIST_DIR,
        collection_name=COLLECTION_NAME,
    )

    print("✅ Successfully indexed all PDFs! You can now query the model.")


if __name__ == "__main__":
    ingest_pdfs()
