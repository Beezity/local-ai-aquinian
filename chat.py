"""
chat.py

BeeAI Local Assistant

Main CLI entrypoint.
"""

from pathlib import Path
from datetime import datetime

from langchain_ollama import ChatOllama

from config import (
    OLLAMA_MODEL,
    STREAM_OUTPUT,
    WELCOME,
    PROMPT,
    CHAT_DIR,
)

from rag import KnowledgeBase
from memory import Memory
from prompt import (
    PromptBuilder,
    PromptInput,
)
from draft import (
    load as load_draft,
    paste as paste_draft,
    summary as draft_summary,
)

# ============================================================
# Startup
# ============================================================

print(WELCOME)

CHAT_DIR.mkdir(
    exist_ok=True,
    parents=True,
)

print("Loading knowledge base...")

kb = KnowledgeBase()

print(
    f"Loaded {kb.count()} knowledge chunks."
)

print("Loading memory...")

memory = Memory()

print("Loading model...")

llm = ChatOllama(
    model=OLLAMA_MODEL,
)

builder = PromptBuilder()

print("Ready.\n")

# ============================================================
# Runtime State
# ============================================================

current_draft = None

last_sources = []

conversation = []

chat_title = (
    datetime.now()
    .strftime("%Y-%m-%d_%H-%M-%S")
)

# ============================================================
# Helpers
# ============================================================


def save_chat():

    if not conversation:
        return

    filename = CHAT_DIR / f"{chat_title}.md"

    with open(
        filename,
        "w",
        encoding="utf-8",
    ) as f:

        f.write("# BeeAI Conversation\n\n")

        for role, text in conversation:

            f.write(f"## {role}\n\n")

            f.write(text)

            f.write("\n\n")

    print(f"\nSaved to {filename}")


def show_sources():

    if not last_sources:

        print("No sources.")

        return

    print()

    for src in last_sources:

        print("-", src)

    print()


def help_menu():

    print(
"""
Commands

/help

/draft <file>

/paste

/clear

/remember

/forget

/sources

/save

/new

/exit
"""
    )


# ============================================================
# Command Handler
# ============================================================


def handle_command(command):

    global current_draft
    global chat_title

    if command == "/help":

        help_menu()

        return True

    if command == "/sources":

        show_sources()

        return True

    if command == "/remember":

        print()

        print(memory.remember())

        print()

        return True

    if command == "/forget":

        memory.clear_all()

        print("Memory cleared.")

        return True

    if command == "/clear":

        current_draft = None

        print("Draft unloaded.")

        return True

    if command == "/paste":

        try:

            current_draft = paste_draft()

            print()

            print(
                draft_summary(
                    current_draft
                )
            )

            print()

        except Exception as e:

            print(e)

        return True

    if command.startswith("/draft"):

        filename = command[7:].strip()

        try:

            current_draft = load_draft(
                filename
            )

            print()

            print(
                draft_summary(
                    current_draft
                )
            )

            print()

        except Exception as e:

            print(e)

        return True

    if command == "/save":

        save_chat()

        return True

    if command == "/new":

        save_chat()

        conversation.clear()

        memory.clear_short()

        current_draft = None

        chat_title = (
            datetime.now()
            .strftime(
                "%Y-%m-%d_%H-%M-%S"
            )
        )

        print(
            "Started new chat."
        )

        return True

    if command == "/exit":

        save_chat()

        raise SystemExit

    return False


# ============================================================
# Main loop begins below...
# ============================================================

while True:

    try:

        question = input(PROMPT).strip()

        if not question:
            continue

        if question.startswith("/"):

            if handle_command(question):
                continue

        # Remaining logic:
        #
        # 1. Retrieve knowledge
        # 2. Retrieve semantic memories
        # 3. Build prompt
        # 4. Stream response
        # 5. Save conversation
        # 6. Update semantic memory
        #
        # (implemented in Part 2)

        # ----------------------------------------------------
        # 1. Retrieve Knowledge
        # ----------------------------------------------------

        result = kb.search(question)

        last_sources = result.sources

        # ----------------------------------------------------
        # 2. Retrieve Semantic Memory
        # ----------------------------------------------------

        semantic_memory = memory.recall(question)

        short_memory = memory.remember()

        # ----------------------------------------------------
        # 3. Build Prompt
        # ----------------------------------------------------

        prompt = builder.build(

            PromptInput(

                question=question,

                knowledge=result.context,

                memory=semantic_memory,

                conversation=short_memory,

                draft=current_draft,

                sources=result.sources,

            )

        )

        # ----------------------------------------------------
        # 4. Stream Response
        # ----------------------------------------------------

        print()

        answer = ""

        if STREAM_OUTPUT:

            for chunk in llm.stream(prompt):

                if chunk.content:

                    print(
                        chunk.content,
                        end="",
                        flush=True,
                    )

                    answer += chunk.content

            print()

        else:

            response = llm.invoke(prompt)

            answer = response.content

            print(answer)

        print()

        # ----------------------------------------------------
        # 5. Save Conversation
        # ----------------------------------------------------

        conversation.append(
            ("User", question)
        )

        conversation.append(
            ("Assistant", answer)
        )

        # ----------------------------------------------------
        # 6. Update Memory
        # ----------------------------------------------------

        memory.add_user(question)

        memory.add_assistant(answer)

        memory.add_exchange(
            question,
            answer,
        )

        # ----------------------------------------------------
        # 7. Show Sources
        # ----------------------------------------------------

        if result.sources:

            print("Knowledge Sources")

            for src in result.sources:

                print(f"  • {src}")

            print()

        # ----------------------------------------------------
        # 8. Draft Indicator
        # ----------------------------------------------------

        if current_draft:

            print(
                f"Current Draft: {current_draft.name}"
            )

            print()

        print("-" * 60)
        print()

    except KeyboardInterrupt:

        print()

        save_chat()

        break

    except Exception as e:

        print(e)

