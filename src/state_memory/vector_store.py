# Vector store wrapper placeholder (in-memory)
"""Simple in-memory vector store used for local testing and demos.

This implementation is intentionally lightweight and not suitable for
production. Use a real vector DB (FAISS, Milvus, Pinecone, etc.) for
scale or persistence.
"""

from typing import Any, Dict, List, Tuple
import math

_VECTOR_DB: Dict[str, Tuple[List[float], Dict[str, Any]]] = {}


def upsert(
    vector_id: str, vector: List[float], metadata: Dict[str, Any] = None
) -> None:
    """Insert or update a vector in the in-memory store.

    Args:
            vector_id: Unique identifier for the vector
            vector: List of floats representing the vector
            metadata: Optional metadata dictionary
    """
    _VECTOR_DB[vector_id] = (vector, metadata or {})


def _cosine_similarity(a: List[float], b: List[float]) -> float:
    """Compute cosine similarity between two vectors."""
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def query(query_vec: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
    """Query the in-memory vector store and return top_k nearest items.

    Returns a list of dicts: {"id", "score", "metadata"}
    """
    results = []
    for vid, (vec, meta) in _VECTOR_DB.items():
        score = _cosine_similarity(query_vec, vec)
        results.append({"id": vid, "score": score, "metadata": meta})

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]


def clear_store() -> None:
    """Clear the in-memory vector store (testing helper)."""
    _VECTOR_DB.clear()
