import json
import random
import os
import logging
import traceback
import urllib.request
import urllib.parse
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from .config import (
    OLLAMA_BASE_URL,
    OLLAMA_API_KEY,
    OLLAMA_MODEL,
    CHROMA_PERSIST_DIR,
    CHROMA_COLLECTION_NAME,
)

# Firebase client (optional)
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from Backend.firebase_client import get_firestore_client, save_ai_response, FIREBASE_ENABLED, FIREBASE_COLLECTION
    from firebase_admin import firestore as _fb_firestore
except Exception as _e:
    logging.warning("Firebase client unavailable: %s", _e)
    get_firestore_client = None
    save_ai_response = None
    FIREBASE_ENABLED = False
    FIREBASE_COLLECTION = 'ai_responses'
    _fb_firestore = None


# Custom exception for chapter not found
class ChapterNotFound(Exception):
    """Raised when a chapter's data file is not found on the remote source."""
    pass


app = FastAPI(title="NCERT Grade 8 Quiz Generator")

# CORS: allow local frontend during development
allowed_origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========================= CONFIG =========================
EMBEDDING_MODEL = "nomic-embed-text"
LLM_MODEL = OLLAMA_MODEL if ":" in OLLAMA_MODEL else f"{OLLAMA_MODEL}:latest"
PERSIST_DIR = CHROMA_PERSIST_DIR
COLLECTION_NAME = CHROMA_COLLECTION_NAME
# =======================================================

# Globals to be initialized lazily on first use
embeddings = None
vectorstore = None
client = None

# Configure basic logging to file for debugging server-side errors
LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "backend.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
)

# NOTE: Removed startup_event to allow fast server startup.
# Initialization happens lazily in ensure_initialized() on first use.


def ensure_initialized():
    """Lazy initialization of embeddings, vectorstore, and client.
    
    This initializes these expensive objects on first use (first endpoint call)
    rather than at server startup to allow the server to start quickly.
    Once initialized, objects are reused for all subsequent requests.
    """
    global embeddings, vectorstore, client
    if embeddings is None or vectorstore is None or client is None:
        logging.info("Lazy initialization: embeddings/vectorstore/client are missing — initializing now")
        try:
            # Import langchain modules here to avoid slow imports at server startup
            from langchain_ollama import OllamaEmbeddings
            from langchain_chroma import Chroma
            
            embeddings = OllamaEmbeddings(
                model=EMBEDDING_MODEL,
                base_url=OLLAMA_BASE_URL,
                validate_model_on_init=False,
            )
            vectorstore = Chroma(
                persist_directory=PERSIST_DIR,
                embedding_function=embeddings,
                collection_name=COLLECTION_NAME,
            )
            client = OpenAI(base_url=f"{OLLAMA_BASE_URL.rstrip('/')}/v1", api_key=OLLAMA_API_KEY)
            logging.info("Lazy initialization complete")
        except Exception:
            tb = traceback.format_exc()
            logging.error("Lazy initialization failed:\n%s", tb)
            with open(os.path.join(LOG_DIR, "last_error.txt"), "w", encoding="utf-8") as fh:
                fh.write(tb)
            raise

    if vectorstore is None:
        message = "Vectorstore initialization returned None"
        logging.error(message)
        raise RuntimeError(message)


class MCQRequest(BaseModel):
    topic: str
    num_questions: int = 5
    difficulty: Optional[str] = None
    source: Optional[str] = None


class CBSEMCQRequest(BaseModel):
    topic: Optional[str] = None
    num_questions: int = 10
    difficulty: Optional[str] = None


RAW_CBSE_MCQS_BASE = "https://raw.githubusercontent.com/learnenglishandgrow93-web/cbse-mcq-bank/refs/heads/main/"
_CBSE_MCQS_CACHE = {}


def fetch_cbse_mcqs(chapter_name: Optional[str] = None):
    """Fetch CBSE MCQs from GitHub raw. If chapter_name is provided, construct
    the raw URL for that chapter file and fetch it. Caches per-URL results.
    Raises ChapterNotFound if chapter-specific URL returns 404.
    """
    global _CBSE_MCQS_CACHE
    # Build target URL
    if chapter_name:
        # Accept either already-encoded or plain chapter names. Normalize by
        # stripping and URL-encoding the chapter filename component.
        name = chapter_name.strip()
        # Do not further split on colons here; the caller provides the normalized chapter name
        if "-" in name and "%20" not in name:
            # if hyphen-separated, prefer last segment
            parts = [p.strip() for p in name.split("-") if p.strip()]
            if parts:
                name = parts[-1]

        encoded = urllib.parse.quote(name, safe='')
        url = RAW_CBSE_MCQS_BASE + encoded
        logging.info(f"Constructed chapter-specific URL: {url}")
        is_chapter_specific = True
    else:
        # Fallback to a default filename previously used
        url = RAW_CBSE_MCQS_BASE + "The%20Invisible%20Living%20World%3A%20Beyond%20Our%20Naked%20Eye"
        logging.info(f"Using default fallback URL: {url}")
        is_chapter_specific = False

    if url in _CBSE_MCQS_CACHE:
        return _CBSE_MCQS_CACHE[url]

    try:
        with urllib.request.urlopen(url, timeout=15) as response:
            content = response.read().decode("utf-8")
            
            # Extract only the valid JSON array (from first [ to last ])
            # This handles files with extra text before or after the JSON
            first_bracket = content.find('[')
            last_bracket = content.rfind(']')
            if first_bracket != -1 and last_bracket != -1 and last_bracket > first_bracket:
                content = content[first_bracket:last_bracket+1]
            
            # Some upstream files contain literal control characters (unescaped newlines,
            # tabs, or carriage returns) inside JSON string values which makes
            # `json.loads` fail. Sanitize the text by escaping control characters
            # that appear while inside a JSON string.
            def _sanitize_json_text(s: str) -> str:
                out_chars = []
                in_str = False
                esc = False
                for ch in s:
                    if ch == '"' and not esc:
                        in_str = not in_str
                        out_chars.append(ch)
                        esc = False
                        continue
                    if ch == '\\' and not esc:
                        esc = True
                        out_chars.append(ch)
                        continue
                    if esc:
                        # previous was a backslash, this char is escaped
                        out_chars.append(ch)
                        esc = False
                        continue
                    if in_str and ch == '\n':
                        out_chars.append('\\n')
                        continue
                    if in_str and ch == '\r':
                        out_chars.append('\\r')
                        continue
                    if in_str and ch == '\t':
                        out_chars.append('\\t')
                        continue
                    out_chars.append(ch)
                return ''.join(out_chars)

            sanitized = _sanitize_json_text(content)
            data = json.loads(sanitized)
    except urllib.error.HTTPError as exc:
        # If chapter-specific URL returns 404, raise ChapterNotFound
        if is_chapter_specific and exc.code == 404:
            raise ChapterNotFound(f"Chapter data not yet available: {chapter_name}") from exc
        raise RuntimeError(f"Failed to load CBSE MCQs from remote source ({url}): {exc}") from exc
    except Exception as exc:
        raise RuntimeError(f"Failed to load CBSE MCQs from remote source ({url}): {exc}") from exc

    if not isinstance(data, list):
        raise ValueError("CBSE MCQ source must be a JSON array")

    _CBSE_MCQS_CACHE[url] = data
    return data


def convert_cbse_item(item: dict):
    return {
        "id": item.get("id"),
        "question": item.get("question", ""),
        "options": item.get("options", []),
        "correct_answer": item.get("answer") or item.get("correct_answer") or "",
        "explanation": item.get("explanation", ""),
        "difficulty": str(item.get("difficulty", "")).capitalize() or "Medium",
    }


def extract_json(text: str):
    import re
    import json as json_module
    
    text = (text or "").strip()
    if not text:
        raise ValueError("LLM response body was empty; no JSON could be extracted")

    # Remove markdown code fences
    code_fence_pattern = r'```(?:json|python|javascript|yaml)?\s*\n?(.*?)\n?```'
    match = re.search(code_fence_pattern, text, re.DOTALL)
    if match:
        text = match.group(1).strip()
    
    text = text.strip()
    if text.startswith('```'):
        text = text[3:]
    if text.endswith('```'):
        text = text[:-3]
    
    text = re.sub(r'^(json|python|javascript|yaml)\s*', '', text, flags=re.IGNORECASE).strip()
    
    # Find the first JSON structure
    start_positions = [pos for pos in (text.find('{'), text.find('[')) if pos != -1]
    if not start_positions:
        raise ValueError(f"Unable to locate JSON in LLM response: {text!r}")

    json_text = text[min(start_positions):]
    
    # Try standard JSON parsing first
    try:
        return json_module.loads(json_text)
    except json_module.JSONDecodeError:
        pass
    
    # Fix common LLM error: unquoted MCQ options like: B) text instead of "B) text"
    # This regex handles: , B) text, C) text patterns
    # We look for: comma + optional whitespace + letter + ) and add quotes around the option
    
    # Pattern explanation:
    # ,(\s+)([A-Z]\))(\s+) means: comma, spaces, letter), spaces
    # Replace with: ,"$2$3$quoted_option"
    
    def add_quotes_to_unquoted_options(s):
        """Add quotes around unquoted MCQ options in arrays."""
        # Find all positions where we have ", B)" pattern (comma, space, letter, paren)
        # and the content after isn't already quoted
        result = []
        lines = s.split('\n')
        for line in lines:
            # Look for "options": [ ... ] lines
            if '"options"' in line:
                # Find the array content
                match = re.search(r'"options"\s*:\s*\[(.*)\]', line)
                if match:
                    opts_content = match.group(1)
                    # Split by comma, but preserve quoted strings
                    # This is a simplification - just wrap unquoted items
                    opts_content = re.sub(
                        r',(\s*)([A-Z]\))',  # comma, optional space, letter, paren
                        r', "\2',             # replace with comma, space, quote, letter, paren
                        opts_content
                    )
                    # Now we need to close the quotes - find where each option ends
                    # Option ends before next comma (outside quotes) or at ]
                    opts_content = re.sub(
                        r'("\w\)[^"]*?)(?=,|$)',  # quoted option content, lookahead for comma or end
                        r'\1"',                    # close the quote
                        opts_content
                    )
                    line = f'"options": [{opts_content}]'
                result.append(line)
            else:
                result.append(line)
        return '\n'.join(result)
    
    json_text = add_quotes_to_unquoted_options(json_text)
    
    try:
        return json_module.loads(json_text)
    except json_module.JSONDecodeError as exc:
        raise ValueError(
            f"Could not parse JSON from LLM response. Tried standard JSON, manual fix attempts. Raw: {text[:300]!r}. Error: {exc}"
        ) from exc


def get_retriever(query: str):
    ensure_initialized()
    if vectorstore is None:
        raise RuntimeError("Vectorstore is not initialized")

    if not hasattr(vectorstore, "as_retriever"):
        raise RuntimeError("Chroma vectorstore has no as_retriever() method")

    retriever = vectorstore.as_retriever(search_kwargs={"k": 12})
    if retriever is None:
        raise RuntimeError("as_retriever() returned None")

    if hasattr(retriever, "get_relevant_documents"):
        docs = retriever.get_relevant_documents(query)
    elif hasattr(retriever, "retrieve"):
        docs = retriever.retrieve(query)
    elif hasattr(retriever, "invoke"):
        docs = retriever.invoke(query)
    else:
        raise RuntimeError("Retriever does not support get_relevant_documents, retrieve, or invoke")

    return docs


@app.post("/api/mcq/generate")
def generate_mcqs(request: MCQRequest):
    try:
        query = f"NCERT Grade 8 {request.topic}" if request.topic else "NCERT Grade 8"
        docs = get_retriever(query)
        if not docs:
            logging.warning("Retriever returned no documents for query: %s", query)
            context = (
                "No reference documents were found in the vector store. "
                "Generate the MCQs using NCERT Grade 8 knowledge only."
            )
        else:
            context = "\n\n".join([doc.page_content for doc in docs])

        system_prompt = f"""You are an expert CBSE NCERT Grade 8 teacher with 15+ years of experience.
Your task is to generate exactly {request.num_questions} fresh, high-quality MCQs for the topic '{request.topic}'.
Use ONLY the provided context and NCERT-aligned concepts.

Return a valid JSON object with the following structure:
{{
  "topic": "{request.topic}",
  "num_questions": {request.num_questions},
  "questions": [
    {{
      "id": 1,
      "question": "...",
      "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
      "correct_answer": "A",
      "explanation": "...",
      "difficulty": "Easy|Medium|Hard"
    }}
  ],
  "status": "success"
}}
Only return valid JSON. Do not include any extra text outside the JSON object."""

        if request.difficulty:
            system_prompt += f"\nUse the requested difficulty level: {request.difficulty}."
        if request.source:
            system_prompt += f"\nUse information from this source if relevant: {request.source}."

        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context:\n\n{context}\n\nGenerate the JSON payload now."}
            ],
            temperature=0.82,
            max_tokens=3500,
            top_p=0.92
        )

        choice = response.choices[0]
        content = None

        # OpenAI wrapper may expose the assistant text in different fields
        if hasattr(choice, 'message') and getattr(choice, 'message', None) is not None:
            content = getattr(choice.message, 'content', None)
        if not content and hasattr(choice, 'text'):
            content = getattr(choice, 'text', None)
        if not content and hasattr(choice, 'content'):
            content = getattr(choice, 'content', None)

        logging.info('LLM raw choice content: %r', content)
        if not content:
            raw = None
            try:
                raw = choice.to_dict() if hasattr(choice, 'to_dict') else repr(choice)
            except Exception:
                raw = repr(choice)
            raise RuntimeError(f"LLM response content was empty. choice={raw}")

        data = extract_json(content)

        return data

    except HTTPException:
        raise
    except Exception as e:
        tb = traceback.format_exc()
        logging.error("Exception in /api/mcq/generate:\n%s", tb)
        with open(os.path.join(LOG_DIR, "last_error.txt"), "w", encoding="utf-8") as fh:
            fh.write(tb)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/mcq/cbse")
def get_cbse_mcqs(request: CBSEMCQRequest):
    import re

    raw_query = (request.topic or "").strip()
    query = raw_query.lower()
    difficulty = (request.difficulty or "").strip().lower()

    # Attempt to fetch chapter-specific MCQs based on the topic
    entries = None
    chapter_not_found = False
    if raw_query:
        chapter_name = None
        if ":" in raw_query:
            # Keep everything after the first colon; chapter titles may contain colons
            chapter_name = raw_query.split(":", 1)[1].strip()
        elif "-" in raw_query:
            parts = [p.strip() for p in raw_query.split("-") if p.strip()]
            if parts:
                chapter_name = parts[-1]
        else:
            # If the topic looks like a chapter title (multiple words), use it
            if len(raw_query.split()) > 2:
                chapter_name = raw_query

        if chapter_name:
            try:
                entries = fetch_cbse_mcqs(chapter_name=chapter_name)
            except ChapterNotFound as exc:
                # Chapter data not yet available
                logging.warning("Chapter not found: %s", exc)
                chapter_not_found = True
            except Exception as exc:
                logging.warning("Failed to fetch CBSE MCQs for chapter '%s': %s", chapter_name, exc)

    # If chapter was not found, return a message to the user
    if chapter_not_found:
        return {
            "topic": request.topic or "CBSE",
            "num_questions": 0,
            "questions": [],
            "status": "chapter_not_available",
            "message": f"Chapter '{chapter_name}' is not yet available. Please check back soon!",
        }

    # Fallback to default source if chapter-specific fetch failed or was not attempted
    if entries is None:
        try:
            entries = fetch_cbse_mcqs()
        except Exception as exc:
            logging.error("CBSE MCQ fetch failed: %s", exc)
            raise HTTPException(status_code=500, detail=str(exc))

    # Build a set of candidate query variants to improve matching for verbose
    # topics like "CBSE Class 8 science: The Invisible Living World: Beyond Our Naked Eye"
    queries = set()
    queries.add(query)

    # If the topic contains colons (:) or hyphens, add the last segment as a focused query
    if ":" in raw_query:
        for seg in raw_query.split(":"):
            s = seg.strip().lower()
            if s:
                queries.add(s)
    if "-" in raw_query:
        for seg in raw_query.split("-"):
            s = seg.strip().lower()
            if s:
                queries.add(s)

    # Strip common prefixes like 'cbse' and 'class <num>' to get the core topic
    q_clean = re.sub(r"\bcbse\b", "", query)
    q_clean = re.sub(r"\bclass\s*\d+\b", "", q_clean)
    q_clean = re.sub(r"[^a-z0-9\s]", " ", q_clean)
    q_clean = re.sub(r"\s+", " ", q_clean).strip()
    if q_clean:
        queries.add(q_clean)

    # Also add single-word tokens from the cleaned query as loose matches (avoid very short tokens)
    for token in q_clean.split():
        if len(token) > 3:
            queries.add(token)

    filtered = []
    for item in entries:
        subject = str(item.get("subject", "")).lower()
        chapter = str(item.get("chapter", "")).lower()
        question_text = str(item.get("question", "")).lower()
        item_difficulty = str(item.get("difficulty", "")).lower()

        # Check if any candidate query variant appears in any of the searchable fields
        matched = False
        for q in queries:
            if not q:
                continue
            if q in subject or q in chapter or q in question_text:
                matched = True
                break

        if query and not matched:
            # no candidate matched this item
            continue
        if difficulty and difficulty != item_difficulty:
            continue
        filtered.append(item)

    # If still nothing found but a topic was provided, try a relaxed filter: check whether
    # all non-trivial words from the cleaned query appear somewhere in the item fields.
    if not filtered and raw_query:
        tokens = [t for t in q_clean.split() if len(t) > 3]
        if tokens:
            for item in entries:
                subject = str(item.get("subject", "")).lower()
                chapter = str(item.get("chapter", "")).lower()
                question_text = str(item.get("question", "")).lower()
                hay = " ".join([subject, chapter, question_text])
                if all(tok in hay for tok in tokens):
                    filtered.append(item)

    if not filtered and request.topic:
        raise HTTPException(status_code=404, detail="No matching CBSE MCQs were found for this topic.")

    # If no items matched and no topic was provided, use the full entries pool
    if not filtered:
        pool = entries.copy()
    else:
        pool = filtered

    # Randomize selection so each call returns a different subset
    count = max(1, min(request.num_questions, 50))
    random.shuffle(pool)
    selected = pool[:count]
    questions = [convert_cbse_item(item) for item in selected]

    return {
        "topic": request.topic or "CBSE",
        "num_questions": len(questions),
        "questions": questions,
        "status": "success",
    }


@app.post("/api/mcq/history")
def save_mcq_history(record: dict):
    # Persist quiz attempt to Firebase if configured, otherwise return success
    try:
        if FIREBASE_ENABLED and save_ai_response is not None:
            save_ai_response(FIREBASE_COLLECTION, record)
            return {"status": "success", "message": "History saved to Firebase.", "record": record}
        else:
            # Not configured: respond success but indicate local-only
            logging.info("Firebase not enabled — history not persisted remotely")
            return {"status": "success", "message": "History received (not persisted - Firebase disabled).", "record": record}
    except Exception as exc:
        logging.error("Failed to save history: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/api/mcq/history")
def list_mcq_history(limit: int = 50):
    # Return persisted quiz attempts (most recent first)
    if not FIREBASE_ENABLED or get_firestore_client is None:
        return []
    client = get_firestore_client()
    if client is None:
        return []
    try:
        coll = client.collection(FIREBASE_COLLECTION)
        if _fb_firestore:
            docs = coll.order_by('created_at', direction=_fb_firestore.Query.DESCENDING).limit(limit).stream()
        else:
            docs = coll.order_by('created_at', direction='DESCENDING').limit(limit).stream()
        items = []
        for d in docs:
            data = d.to_dict()
            data['id'] = d.id
            items.append(data)
        return items
    except Exception as exc:
        logging.error("Failed to list persisted mcqs: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/health")
def health():
    return {"status": "healthy", "message": "Ollama backend is ready"}


if __name__ == "__main__":
    print(f"🚀 Starting NCERT Quiz Generator with model: {LLM_MODEL}")
    uvicorn.run(app, host="0.0.0.0", port=8000)
