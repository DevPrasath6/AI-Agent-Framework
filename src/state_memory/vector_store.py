"""
Enhanced vector store with multiple backend support and advanced features.

Supports in-memory storage for development and external vector databases
for production (FAISS, Pinecone, Weaviate, etc.).
"""
from __future__ import annotations

import asyncio
import json
import logging
import math
import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

# Optional vector DB dependencies
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    np = None
    NUMPY_AVAILABLE = False

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    faiss = None
    FAISS_AVAILABLE = False


@dataclass
class VectorDocument:
    """Document with vector embedding and metadata."""
    id: str
    content: str
    vector: List[float]
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    namespace: str = "default"


@dataclass
class VectorSearchResult:
    """Result from vector similarity search."""
    document: VectorDocument
    score: float
    rank: int


class VectorStore(ABC):
    """Abstract base class for vector storage backends."""

    @abstractmethod
    async def upsert(self, document: VectorDocument) -> bool:
        """Insert or update a document."""
        pass

    @abstractmethod
    async def query(
        self,
        query_vector: List[float],
        top_k: int = 5,
        namespace: str = "default",
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[VectorSearchResult]:
        """Query for similar vectors."""
        pass

    @abstractmethod
    async def delete(self, document_id: str, namespace: str = "default") -> bool:
        """Delete a document."""
        pass

    @abstractmethod
    async def get_stats(self) -> Dict[str, Any]:
        """Get storage statistics."""
        pass


class InMemoryVectorStore(VectorStore):
    """In-memory vector store for development and testing."""

    def __init__(self):
        self._documents: Dict[str, VectorDocument] = {}
        self.logger = logging.getLogger(f"{__name__}.InMemory")

    async def upsert(self, document: VectorDocument) -> bool:
        """Insert or update a document."""
        key = f"{document.namespace}:{document.id}"
        self._documents[key] = document
        self.logger.debug(f"Upserted document {document.id} in namespace {document.namespace}")
        return True

    async def query(
        self,
        query_vector: List[float],
        top_k: int = 5,
        namespace: str = "default",
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[VectorSearchResult]:
        """Query for similar vectors using cosine similarity."""
        results = []

        for key, doc in self._documents.items():
            if not key.startswith(f"{namespace}:"):
                continue

            # Apply metadata filters
            if filter_metadata:
                if not all(
                    doc.metadata.get(k) == v
                    for k, v in filter_metadata.items()
                ):
                    continue

            score = self._cosine_similarity(query_vector, doc.vector)
            results.append(VectorSearchResult(document=doc, score=score, rank=0))

        # Sort by score and assign ranks
        results.sort(key=lambda x: x.score, reverse=True)
        for i, result in enumerate(results[:top_k]):
            result.rank = i + 1

        return results[:top_k]

    async def delete(self, document_id: str, namespace: str = "default") -> bool:
        """Delete a document."""
        key = f"{namespace}:{document_id}"
        if key in self._documents:
            del self._documents[key]
            return True
        return False

    async def get_stats(self) -> Dict[str, Any]:
        """Get storage statistics."""
        namespaces = {}
        for key in self._documents.keys():
            namespace = key.split(":", 1)[0]
            namespaces[namespace] = namespaces.get(namespace, 0) + 1

        return {
            "total_documents": len(self._documents),
            "namespaces": namespaces,
            "backend": "in_memory"
        }

    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Compute cosine similarity between two vectors."""
        if not a or not b or len(a) != len(b):
            return 0.0
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(y * y for y in b))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)


class FAISSVectorStore(VectorStore):
    """FAISS-based vector store for high-performance similarity search."""

    def __init__(self, dimension: int = 1536):
        if not FAISS_AVAILABLE:
            raise ImportError("FAISS not available - install with: pip install faiss-cpu")

        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)  # Inner product (cosine similarity)
        self._id_map: Dict[int, str] = {}  # FAISS index -> document ID
        self._documents: Dict[str, VectorDocument] = {}
        self._next_id = 0
        self.logger = logging.getLogger(f"{__name__}.FAISS")

    async def upsert(self, document: VectorDocument) -> bool:
        """Insert or update a document."""
        try:
            if len(document.vector) != self.dimension:
                raise ValueError(f"Vector dimension {len(document.vector)} != {self.dimension}")

            # Normalize vector for cosine similarity
            vector = np.array(document.vector, dtype=np.float32)
            vector = vector / np.linalg.norm(vector)

            key = f"{document.namespace}:{document.id}"

            # Remove existing entry if present
            if key in self._documents:
                await self.delete(document.id, document.namespace)

            # Add to FAISS index
            self.index.add(vector.reshape(1, -1))

            # Update mappings
            self._id_map[self._next_id] = key
            self._documents[key] = document
            self._next_id += 1

            self.logger.debug(f"Upserted document {document.id} in FAISS")
            return True

        except Exception as e:
            self.logger.error(f"Failed to upsert document: {e}")
            return False

    async def query(
        self,
        query_vector: List[float],
        top_k: int = 5,
        namespace: str = "default",
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[VectorSearchResult]:
        """Query using FAISS index."""
        try:
            if len(query_vector) != self.dimension:
                raise ValueError(f"Query vector dimension {len(query_vector)} != {self.dimension}")

            # Normalize query vector
            query = np.array(query_vector, dtype=np.float32)
            query = query / np.linalg.norm(query)

            # Search FAISS index
            scores, indices = self.index.search(query.reshape(1, -1), min(top_k * 2, self.index.ntotal))

            results = []
            for score, idx in zip(scores[0], indices[0]):
                if idx == -1:  # No more results
                    break

                doc_key = self._id_map.get(idx)
                if not doc_key:
                    continue

                # Check namespace
                if not doc_key.startswith(f"{namespace}:"):
                    continue

                doc = self._documents.get(doc_key)
                if not doc:
                    continue

                # Apply metadata filters
                if filter_metadata:
                    if not all(
                        doc.metadata.get(k) == v
                        for k, v in filter_metadata.items()
                    ):
                        continue

                results.append(VectorSearchResult(
                    document=doc,
                    score=float(score),
                    rank=len(results) + 1
                ))

                if len(results) >= top_k:
                    break

            return results

        except Exception as e:
            self.logger.error(f"FAISS query failed: {e}")
            return []

    async def delete(self, document_id: str, namespace: str = "default") -> bool:
        """Delete a document (FAISS doesn't support deletion, so we mark as deleted)."""
        key = f"{namespace}:{document_id}"
        if key in self._documents:
            del self._documents[key]
            # Note: FAISS doesn't support efficient deletion, so index grows
            # In production, you'd rebuild the index periodically
            return True
        return False

    async def get_stats(self) -> Dict[str, Any]:
        """Get storage statistics."""
        namespaces = {}
        for key in self._documents.keys():
            namespace = key.split(":", 1)[0]
            namespaces[namespace] = namespaces.get(namespace, 0) + 1

        return {
            "total_documents": len(self._documents),
            "index_size": self.index.ntotal,
            "dimension": self.dimension,
            "namespaces": namespaces,
            "backend": "faiss"
        }


class VectorMemoryManager:
    """High-level manager for vector memory operations."""

    def __init__(self, store: VectorStore):
        self.store = store
        self.logger = logging.getLogger(f"{__name__}.Manager")

    async def add_text(
        self,
        text: str,
        embedding: List[float],
        metadata: Optional[Dict[str, Any]] = None,
        document_id: Optional[str] = None,
        namespace: str = "default"
    ) -> str:
        """Add text with embedding to vector memory."""
        doc_id = document_id or str(uuid.uuid4())

        document = VectorDocument(
            id=doc_id,
            content=text,
            vector=embedding,
            metadata=metadata or {},
            namespace=namespace
        )

        success = await self.store.upsert(document)
        if success:
            self.logger.debug(f"Added text document {doc_id}")
            return doc_id
        else:
            raise RuntimeError(f"Failed to add document {doc_id}")

    async def search_similar(
        self,
        query_text: str,
        query_embedding: List[float],
        top_k: int = 5,
        namespace: str = "default",
        min_score: float = 0.0,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[VectorSearchResult]:
        """Search for similar documents."""
        results = await self.store.query(
            query_vector=query_embedding,
            top_k=top_k,
            namespace=namespace,
            filter_metadata=filter_metadata
        )

        # Filter by minimum score
        filtered_results = [r for r in results if r.score >= min_score]

        self.logger.debug(f"Found {len(filtered_results)} similar documents for query")
        return filtered_results

    async def get_conversation_context(
        self,
        query_embedding: List[float],
        conversation_id: str,
        max_tokens: int = 2000,
        namespace: str = "conversations"
    ) -> str:
        """Retrieve relevant conversation context."""
        results = await self.search_similar(
            query_text="",
            query_embedding=query_embedding,
            top_k=10,
            namespace=namespace,
            filter_metadata={"conversation_id": conversation_id}
        )

        context_parts = []
        token_count = 0

        for result in results:
            content = result.document.content
            # Rough token estimation (4 chars per token)
            estimated_tokens = len(content) // 4

            if token_count + estimated_tokens > max_tokens:
                break

            context_parts.append(content)
            token_count += estimated_tokens

        return "\n\n".join(context_parts)

    async def add_conversation_turn(
        self,
        conversation_id: str,
        role: str,
        content: str,
        embedding: List[float],
        metadata: Optional[Dict[str, Any]] = None,
        namespace: str = "conversations"
    ) -> str:
        """Add a conversation turn to memory."""
        turn_metadata = {
            "conversation_id": conversation_id,
            "role": role,
            "timestamp": datetime.now().isoformat(),
            **(metadata or {})
        }

        return await self.add_text(
            text=content,
            embedding=embedding,
            metadata=turn_metadata,
            namespace=namespace
        )

    async def get_knowledge_base_context(
        self,
        query_embedding: List[float],
        domain: Optional[str] = None,
        max_results: int = 5,
        namespace: str = "knowledge_base"
    ) -> List[str]:
        """Retrieve relevant knowledge base articles."""
        filter_metadata = {"domain": domain} if domain else None

        results = await self.search_similar(
            query_text="",
            query_embedding=query_embedding,
            top_k=max_results,
            namespace=namespace,
            filter_metadata=filter_metadata
        )

        return [result.document.content for result in results]


# Global vector store instance
_vector_store: Optional[VectorStore] = None
_vector_manager: Optional[VectorMemoryManager] = None


def get_vector_store() -> VectorStore:
    """Get the global vector store instance."""
    global _vector_store

    if _vector_store is None:
        # Try to use FAISS if available, otherwise fall back to in-memory
        if FAISS_AVAILABLE and NUMPY_AVAILABLE:
            try:
                _vector_store = FAISSVectorStore()
                logger.info("Initialized FAISS vector store")
            except Exception as e:
                logger.warning(f"Failed to initialize FAISS: {e}, falling back to in-memory")
                _vector_store = InMemoryVectorStore()
        else:
            _vector_store = InMemoryVectorStore()
            logger.info("Initialized in-memory vector store")

    return _vector_store


def get_vector_memory_manager() -> VectorMemoryManager:
    """Get the global vector memory manager."""
    global _vector_manager

    if _vector_manager is None:
        _vector_manager = VectorMemoryManager(get_vector_store())

    return _vector_manager


# Legacy compatibility functions
def upsert(vector_id: str, vector: List[float], metadata: Dict[str, Any] = None) -> None:
    """Legacy function for backward compatibility."""
    asyncio.create_task(_legacy_upsert(vector_id, vector, metadata))


async def _legacy_upsert(vector_id: str, vector: List[float], metadata: Dict[str, Any] = None):
    """Async implementation of legacy upsert."""
    document = VectorDocument(
        id=vector_id,
        content=metadata.get("content", "") if metadata else "",
        vector=vector,
        metadata=metadata or {}
    )
    store = get_vector_store()
    await store.upsert(document)


def query(query_vec: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
    """Legacy function for backward compatibility."""
    # Run async query in sync context
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        results = loop.run_until_complete(_legacy_query(query_vec, top_k))
        return [
            {
                "id": r.document.id,
                "score": r.score,
                "metadata": r.document.metadata
            }
            for r in results
        ]
    finally:
        loop.close()


async def _legacy_query(query_vec: List[float], top_k: int = 5) -> List[VectorSearchResult]:
    """Async implementation of legacy query."""
    store = get_vector_store()
    return await store.query(query_vec, top_k)


def clear_store() -> None:
    """Clear the vector store (testing helper)."""
    global _vector_store, _vector_manager
    _vector_store = None
    _vector_manager = None
