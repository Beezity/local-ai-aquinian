"""
draft.py

Handles loading draft documents.
"""

from dataclasses import dataclass
from pathlib import Path

from langchain_community.document_loaders import (
    Docx2txtLoader,
    PyPDFLoader,
    TextLoader,
)

from config import (
    DRAFTS_DIR,
    MAX_DRAFT_CHARACTERS,
    SUPPORTED_EXTENSIONS,
)


# ============================================================
# Draft Object
# ============================================================


@dataclass
class Draft:

    name: str
    path: Path | None
    text: str
    extension: str


# ============================================================
# Internal
# ============================================================


def _read_file(path: Path) -> str:

    ext = path.suffix.lower()

    if ext == ".pdf":
        loader = PyPDFLoader(str(path))

    elif ext == ".docx":
        loader = Docx2txtLoader(str(path))

    else:
        loader = TextLoader(
            str(path),
            encoding="utf-8",
        )

    docs = loader.load()

    return "\n\n".join(
        doc.page_content
        for doc in docs
    )


# ============================================================
# Public API
# ============================================================


def load(path: str | Path) -> Draft:

    path = Path(path)

    if not path.is_absolute():
        path = DRAFTS_DIR / path

    path = path.resolve()

    if not path.exists():
        raise FileNotFoundError(path)

    ext = path.suffix.lower()

    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported draft type: {ext}"
        )

    text = _read_file(path)

    if len(text) > MAX_DRAFT_CHARACTERS:

        raise ValueError(
            f"Draft exceeds "
            f"{MAX_DRAFT_CHARACTERS:,} characters."
        )

    return Draft(
        name=path.name,
        path=path,
        text=text,
        extension=ext,
    )


def from_text(text: str) -> Draft:

    text = text.strip()

    if not text:
        raise ValueError(
            "Draft is empty."
        )

    if len(text) > MAX_DRAFT_CHARACTERS:

        raise ValueError(
            f"Draft exceeds "
            f"{MAX_DRAFT_CHARACTERS:,} characters."
        )

    return Draft(
        name="Pasted Draft",
        path=None,
        text=text,
        extension=".txt",
    )


def paste() -> Draft:

    print()
    print("Paste your draft.")
    print("Finish with END on its own line.")
    print()

    lines = []

    while True:

        line = input()

        if line.strip() == "END":
            break

        lines.append(line)

    return from_text(
        "\n".join(lines)
    )


def summary(draft: Draft) -> str:

    words = len(draft.text.split())

    chars = len(draft.text)

    return (
        f"{draft.name} "
        f"({words:,} words, "
        f"{chars:,} characters)"
    )
