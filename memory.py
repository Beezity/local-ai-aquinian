"""
memory.py

BeeAI Conversation Memory

Provides:

- Rolling conversation memory
- Semantic long-term memory
- Conversation exchange storage
- Memory retrieval
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from datetime import datetime
import uuid

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

from config import (
    EMBEDDING_MODEL,
    MEMORY_DB,
    SHORT_TERM_MEMORY,
    SEMANTIC_MEMORY_K,
    STORE_CONVERSATIONS,
)


# ============================================================
# Message
# ============================================================


@dataclass
class Message:

    role: str
    content: str


# ============================================================
# Memory
# ============================================================


class Memory:

    def __init__(self):

        self.history = deque(
            maxlen=SHORT_TERM_MEMORY
        )

        embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL
        )

        self.db = Chroma(
            persist_directory=str(MEMORY_DB),
            embedding_function=embeddings,
        )

    # =========================================================
    # Short-Term Memory
    # =========================================================

    def add_user(self, text: str):

        self.history.append(
            Message(
                "User",
                text,
            )
        )

    def add_assistant(self, text: str):

        self.history.append(
            Message(
                "Assistant",
                text,
            )
        )

    def short_term(self) -> str:

        if not self.history:
            return "None"

        lines = []

        for message in self.history:

            lines.append(
                f"{message.role}: {message.content}"
            )

        return "\n".join(lines)

    # =========================================================
    # Semantic Memory
    # =========================================================

    def should_store_exchange(
        self,
        question: str,
        answer: str,
    ) -> bool:

        question = question.strip().lower()

        ignored = {

            "hi",
            "hello",
            "hey",
            "thanks",
            "thank you",
            "ok",
            "okay",
            "yes",
            "no",
            "continue",
            "continue.",
            "lol",
            "lmao",
            "nice",
            "cool",

        }

        if question in ignored:
            return False

        if len(question) < 20:
            return False

        if len(answer.strip()) < 40:
            return False

        return True

    def add_exchange(
        self,
        question: str,
        answer: str,
    ):

        if not STORE_CONVERSATIONS:
            return

        if not self.should_store_exchange(
            question,
            answer,
        ):
            return

        text = f"""
User
====

{question}

Assistant
=========

{answer}
"""

        document = Document(

            page_content=text.strip(),

            metadata={

                "type": "conversation",

                "timestamp":
                    datetime.utcnow().isoformat(),

                "id":
                    str(uuid.uuid4()),

            },

        )

        self.db.add_documents(
            [document]
        )

    # =========================================================
    # Retrieval
    # =========================================================

    def search(
        self,
        query: str,
    ):

        return self.db.similarity_search(
            query,
            k=SEMANTIC_MEMORY_K,
        )

    def recall(
        self,
        query: str,
    ) -> str:

        docs = self.search(query)

        if not docs:
            return "None"

        memories = []

        for i, doc in enumerate(
            docs,
            start=1,
        ):

            memories.append(
                f"""Memory {i}
--------------------
{doc.page_content}
"""
            )

        return "\n".join(memories)

    # =========================================================
    # Utilities
    # =========================================================

    def remember(self):

        return self.short_term()

    def clear_short(self):

        self.history.clear()

    def clear_all(self):

        self.history.clear()

        ids = self.db.get()["ids"]

        if ids:

            self.db.delete(ids)

    def stats(self):

        ids = self.db.get()["ids"]

        return {

            "short_messages":
                len(self.history),

            "semantic_entries":
                len(ids),

        }

    def count(self):

        return len(
            self.db.get()["ids"]
        )
