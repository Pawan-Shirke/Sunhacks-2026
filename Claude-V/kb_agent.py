"""
Knowledge Base Agent — ChromaDB vector store for company policies.
Falls back to simple keyword search if ChromaDB or embeddings are unavailable.
"""
import os
from data.sample_data import SAMPLE_POLICIES

# ─── Try to use ChromaDB + OpenAI embeddings ─────────────────────────────────
_chroma_available = False
_vector_store = None

def _init_chroma():
    global _chroma_available, _vector_store
    try:
        import chromadb
        from chromadb.config import Settings

        client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory="db/chroma_data",
            anonymized_telemetry=False
        ))
        collection = client.get_or_create_collection("policies")

        # Index sample policies if empty
        if collection.count() == 0:
            for pol in SAMPLE_POLICIES:
                collection.add(
                    documents=[pol["text"]],
                    metadatas=[{"id": pol["id"], "title": pol["title"]}],
                    ids=[pol["id"]]
                )

        _vector_store = collection
        _chroma_available = True
        print("[KBAgent] ChromaDB initialized successfully.")
    except Exception as e:
        print(f"[KBAgent] ChromaDB not available ({e}), using keyword fallback.")
        _chroma_available = False


_init_chroma()


def index_policy(policy_id: str, text: str, title: str = ""):
    """Add or update a policy document in the knowledge base."""
    if _chroma_available and _vector_store:
        try:
            _vector_store.upsert(
                documents=[text],
                metadatas=[{"id": policy_id, "title": title}],
                ids=[policy_id]
            )
            return True
        except Exception as e:
            print(f"[KBAgent] Error indexing: {e}")
    return False


def query_policies(query_text: str, k: int = 5):
    """
    Retrieve top-k policy documents most relevant to query_text.
    Returns list of dicts with 'id', 'title', 'text', 'score'.
    """
    if _chroma_available and _vector_store:
        try:
            results = _vector_store.query(
                query_texts=[query_text],
                n_results=min(k, _vector_store.count())
            )
            hits = []
            for i, doc_id in enumerate(results["ids"][0]):
                hits.append({
                    "id": doc_id,
                    "title": results["metadatas"][0][i].get("title", doc_id),
                    "text": results["documents"][0][i],
                    "score": results["distances"][0][i] if results.get("distances") else 0.0
                })
            return hits
        except Exception as e:
            print(f"[KBAgent] ChromaDB query error: {e}")

    # ── Keyword fallback ──────────────────────────────────────────────────────
    return _keyword_search(query_text, k)


def _keyword_search(query_text: str, k: int = 5):
    """Simple keyword overlap search as fallback."""
    query_words = set(query_text.lower().split())
    scored = []
    for pol in SAMPLE_POLICIES:
        pol_words = set(pol["text"].lower().split())
        overlap = len(query_words & pol_words)
        scored.append((overlap, pol))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [
        {"id": p["id"], "title": p["title"], "text": p["text"], "score": float(s)}
        for s, p in scored[:k]
    ]
