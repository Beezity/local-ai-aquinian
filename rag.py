"""
rag.py

Retrieval-Augmented Generation (RAG)

Handles:

- Loading the knowledge database
- Similarity search
- Formatting retrieved context
- Returning source information
"""

from pathlib import Path
from dataclasses import dataclass

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

from config import (
    KNOWLEDGE_DB,
    EMBEDDING_MODEL,
    TOP_K,
    MAX_CONTEXT_CHARACTERS,
)


# ============================================================
# Result
# ============================================================

@dataclass
class RetrievalResult:

    documents: list[Document]

    context: str

    sources: list[str]


# ============================================================
# RAG
# ============================================================

class KnowledgeBase:

    def __init__(self):

        embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL
        )

        self.db = Chroma(
            persist_directory=str(KNOWLEDGE_DB),
            embedding_function=embeddings,
        )

    # --------------------------------------------------------

    def search(
        self,
        question: str,
        k: int = TOP_K,
    ) -> RetrievalResult:

        docs = self.db.similarity_search(
            question,
            k=k,
        )

        return self._build_result(docs)

    # --------------------------------------------------------

    def search_with_scores(
        self,
        question: str,
        k: int = TOP_K,
    ):

        return self.db.similarity_search_with_score(
            question,
            k=k,
        )

    # --------------------------------------------------------

    def _build_result(
        self,
        docs: list[Document],
    ) -> RetrievalResult:

        context_parts = []

        total = 0

        sources = []

        seen = set()

        for doc in docs:

            text = doc.page_content.strip()

            if not text:
                continue

            if total >= MAX_CONTEXT_CHARACTERS:
                break

            remaining = (
                MAX_CONTEXT_CHARACTERS
                - total
            )

            if len(text) > remaining:
                text = text[:remaining]

            context_parts.append(text)

            total += len(text)

            src = Path(
                doc.metadata.get(
                    "source",
                    "Unknown"
                )
            ).name

            if src not in seen:

                seen.add(src)
                sources.append(src)

        context = "\n\n".join(
            context_parts
        )

        return RetrievalResult(
            documents=docs,
            context=context,
            sources=sources,
        )

    # --------------------------------------------------------

    def count(self):

        return len(
            self.db.get()["ids"]
        )

    # --------------------------------------------------------

    def stats(self):

        ids = self.db.get()["ids"]

        return {
            "chunks": len(ids)
        }
