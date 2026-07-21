"""
index.py

Indexes every supported document inside the knowledge/
directory into the Chroma knowledge database.
"""

from pathlib import Path
import shutil

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
)

from config import (
    KNOWLEDGE_DIR,
    KNOWLEDGE_DB,
    EMBEDDING_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    SUPPORTED_EXTENSIONS,
)


# -------------------------------------------------------
# Load a single file
# -------------------------------------------------------

def load_file(path: Path):
    """
    Returns a list of LangChain Documents.
    """

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

    relative = path.relative_to(KNOWLEDGE_DIR)

    for doc in docs:
        doc.metadata["source"] = str(relative)
        doc.metadata["filename"] = path.name
        doc.metadata["extension"] = ext

    return docs


# -------------------------------------------------------
# Scan knowledge folder
# -------------------------------------------------------

def collect_documents():

    docs = []

    skipped = []

    for path in KNOWLEDGE_DIR.rglob("*"):

        if not path.is_file():
            continue

        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            skipped.append(path)
            continue

        try:
            docs.extend(load_file(path))

        except Exception as e:
            print(f"[ERROR] {path}")
            print(f"        {e}")

    return docs, skipped


# -------------------------------------------------------
# Main
# -------------------------------------------------------

def main():

    print("Scanning knowledge directory...")

    docs, skipped = collect_documents()

    print(f"Loaded {len(docs)} document sections.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    chunks = splitter.split_documents(docs)

    print(f"Created {len(chunks)} chunks.")

    if KNOWLEDGE_DB.exists():
        shutil.rmtree(KNOWLEDGE_DB)

    KNOWLEDGE_DB.mkdir(parents=True, exist_ok=True)

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    print("Building vector database...")

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(KNOWLEDGE_DB),
    )

    print()
    print("Knowledge base built successfully.")
    print()

    print(f"Documents : {len(docs)}")
    print(f"Chunks    : {len(chunks)}")
    print(f"Skipped   : {len(skipped)}")

    if skipped:

        print()
        print("Skipped files:")

        for file in skipped:
            print(" -", file.relative_to(KNOWLEDGE_DIR))


if __name__ == "__main__":
    main()
