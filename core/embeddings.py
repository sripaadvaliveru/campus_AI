"""
embeddings.py — FAISS vector store management using HuggingFace sentence-transformers.
Builds, saves, and loads the campus knowledge vector index.
"""

import logging
import os
import pickle
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

VECTOR_STORE_PATH = Path(os.getenv("VECTOR_STORE_PATH", "./vector_store"))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")


class CampusVectorStore:
    """Manages the FAISS vector store for campus knowledge retrieval."""

    def __init__(self):
        self.index = None
        self.documents: List[Dict[str, Any]] = []
        self.embeddings_model = None
        self._model_loaded = False

    def _load_model(self):
        """Lazy-load the embedding model."""
        if not self._model_loaded:
            try:
                from sentence_transformers import SentenceTransformer
                logger.info(f"Loading embedding model: {EMBEDDING_MODEL}")
                self.embeddings_model = SentenceTransformer(EMBEDDING_MODEL)
                self._model_loaded = True
                logger.info("Embedding model loaded successfully.")
            except Exception as e:
                logger.error(f"Failed to load embedding model: {e}")
                raise

    def _embed_texts(self, texts: List[str]) -> "np.ndarray":
        """Embed a list of texts using the sentence transformer."""
        self._load_model()
        import numpy as np
        embeddings = self.embeddings_model.encode(
            texts,
            show_progress_bar=True,
            batch_size=32,
            normalize_embeddings=True
        )
        return np.array(embeddings, dtype="float32")

    def build_index(self, documents: List[Dict[str, Any]]) -> None:
        """Build FAISS index from a list of documents."""
        if not documents:
            logger.warning("No documents provided for indexing.")
            return

        import faiss
        import numpy as np

        logger.info(f"Building FAISS index from {len(documents)} documents...")

        texts = [doc["text"] for doc in documents]
        self.documents = documents

        embeddings = self._embed_texts(texts)
        dimension = embeddings.shape[1]

        # Use IVF index for large datasets, flat for small
        if len(documents) > 1000:
            nlist = min(100, len(documents) // 10)
            quantizer = faiss.IndexFlatIP(dimension)
            self.index = faiss.IndexIVFFlat(quantizer, dimension, nlist, faiss.METRIC_INNER_PRODUCT)
            self.index.train(embeddings)
        else:
            self.index = faiss.IndexFlatIP(dimension)

        self.index.add(embeddings)
        logger.info(f"FAISS index built with {self.index.ntotal} vectors (dimension={dimension})")

    def save(self) -> None:
        """Save the FAISS index and documents to disk."""
        VECTOR_STORE_PATH.mkdir(parents=True, exist_ok=True)

        import faiss
        faiss.write_index(self.index, str(VECTOR_STORE_PATH / "campus.index"))

        with open(VECTOR_STORE_PATH / "documents.pkl", "wb") as f:
            pickle.dump(self.documents, f)

        logger.info(f"Vector store saved to {VECTOR_STORE_PATH}")

    def load(self) -> bool:
        """Load the FAISS index and documents from disk. Returns True if successful."""
        index_path = VECTOR_STORE_PATH / "campus.index"
        docs_path = VECTOR_STORE_PATH / "documents.pkl"

        if not index_path.exists() or not docs_path.exists():
            logger.info("No existing vector store found.")
            return False

        try:
            import faiss
            self.index = faiss.read_index(str(index_path))

            with open(docs_path, "rb") as f:
                self.documents = pickle.load(f)

            self._load_model()
            logger.info(f"Vector store loaded: {self.index.ntotal} vectors, {len(self.documents)} documents")
            return True
        except Exception as e:
            logger.error(f"Failed to load vector store: {e}")
            return False

    def search(self, query: str, top_k: int = 5) -> List[Tuple[float, Dict[str, Any]]]:
        """Search the vector store for relevant documents. Returns (score, doc) tuples."""
        if self.index is None or not self.documents:
            logger.warning("Vector store not initialized.")
            return []

        import numpy as np
        query_embedding = self._embed_texts([query])

        scores, indices = self.index.search(query_embedding, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.documents) and idx >= 0:
                results.append((float(score), self.documents[idx]))

        return results

    def get_relevant_context(self, query: str, top_k: int = 4, min_score: float = 0.2) -> str:
        """Return formatted context string from top matching documents."""
        results = self.search(query, top_k=top_k)
        if not results:
            return "No relevant information found."

        context_parts = []
        for score, doc in results:
            if score >= min_score:
                source = doc.get("metadata", {}).get("source", "campus data")
                context_parts.append(f"[Source: {source}]\n{doc['text']}")

        if not context_parts:
            return "No sufficiently relevant information found."

        return "\n\n---\n\n".join(context_parts)

    @property
    def is_ready(self) -> bool:
        """Check if the vector store is loaded and ready."""
        return self.index is not None and len(self.documents) > 0


# Global singleton instance
_vector_store: Optional[CampusVectorStore] = None


def get_vector_store() -> CampusVectorStore:
    """Get or initialize the global vector store instance."""
    global _vector_store
    if _vector_store is None:
        _vector_store = CampusVectorStore()
        if not _vector_store.load():
            logger.warning("Vector store not found. Run initialize.py to build it first.")
    return _vector_store


def build_and_save_vector_store(documents: List[Dict[str, Any]]) -> CampusVectorStore:
    """Build a new vector store from documents and save it."""
    global _vector_store
    vs = CampusVectorStore()
    vs.build_index(documents)
    vs.save()
    _vector_store = vs
    return vs
