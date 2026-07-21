"""
config.py

Global configuration for the Local AI Assistant.
"""

from pathlib import Path

# ============================================================
# Project Directories
# ============================================================

PROJECT_ROOT = Path(__file__).parent.resolve()

KNOWLEDGE_DIR = PROJECT_ROOT / "knowledge"
DRAFTS_DIR = PROJECT_ROOT / "drafts"
CHAT_DIR = PROJECT_ROOT / "chats"

DATABASE_DIR = PROJECT_ROOT / "database"
KNOWLEDGE_DB = DATABASE_DIR / "knowledge"
MEMORY_DB = DATABASE_DIR / "memory"

# ============================================================
# Ollama
# ============================================================

OLLAMA_MODEL = "qwen3:8b"

OLLAMA_HOST = "http://localhost:11434"

# ============================================================
# Embedding Model
# ============================================================

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

# ============================================================
# Retrieval (Knowledge Base)
# ============================================================

TOP_K = 4

CHUNK_SIZE = 800
CHUNK_OVERLAP = 100

# Maximum number of retrieved documents
MAX_CONTEXT_DOCUMENTS = 4

# ============================================================
# Conversation Memory
# ============================================================

# Number of messages kept directly in the prompt
SHORT_TERM_MEMORY = 8

# Number of semantic memories retrieved
SEMANTIC_MEMORY_K = 3

# Minimum similarity score required before a memory is recalled.
# Lower values recall more memories.
SEMANTIC_MEMORY_THRESHOLD = 0.45

# Store assistant replies in semantic memory?
STORE_ASSISTANT_MESSAGES = True

STORE_CONVERSATIONS = True

# ============================================================
# Prompt Limits
# ============================================================

# Prevent accidentally sending huge drafts
MAX_DRAFT_CHARACTERS = 200_000

# Prevent huge knowledge contexts
MAX_CONTEXT_CHARACTERS = 15_000

# ============================================================
# Streaming
# ============================================================

STREAM_OUTPUT = True

# ============================================================
# Chat Saving
# ============================================================

AUTO_SAVE_CHAT = True

CHAT_EXTENSION = ".md"

# ============================================================
# Draft Support
# ============================================================

SUPPORTED_EXTENSIONS = {
    ".txt",
    ".md",
    ".pdf",
    ".docx",
    ".py",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".csv",
    ".html",
    ".css",
    ".js",
    ".ts",
    ".java",
    ".c",
    ".cpp",
    ".h",
    ".hpp",
    ".rs",
    ".go",
    ".php",
    ".xml",
}

# ============================================================
# Prompt
# ============================================================

SYSTEM_PROMPT = """
You are BeeAI, a completely offline local AI assistant.

Primary objectives:

- Answer questions accurately.
- Use the knowledge base whenever possible.
- Never invent facts.
- If information is unavailable, clearly state that.
- Review and improve drafts while preserving the author's intent.
- Explain your reasoning when appropriate.
- Prefer concise, direct answers unless asked otherwise.

When editing:

- Improve grammar.
- Improve clarity.
- Preserve tone.
- Preserve technical accuracy.
- Do not remove important information.
- Point out contradictions with the knowledge base.

When answering:

- Prefer retrieved knowledge over assumptions.
- Mention which knowledge sources influenced the answer.
"""

# ============================================================
# CLI
# ============================================================

PROMPT = "> "

WELCOME = """
BeeAI Local Assistant

Commands:

/help
/draft <file>
/paste
/clear
/remember
/forget
/new
/save
/load
/sources
/history
/exit
"""
