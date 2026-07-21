"""
prompt.py

Prompt construction for BeeAI.

This module converts structured data into the final prompt
sent to the language model.
"""

from dataclasses import dataclass
from typing import Optional

from config import SYSTEM_PROMPT
from draft import Draft


# ============================================================
# Prompt Input
# ============================================================

@dataclass
class PromptInput:

    question: str

    knowledge: str = ""

    memory: str = ""

    conversation: str = ""

    draft: Optional[Draft] = None

    sources: list[str] | None = None


# ============================================================
# Prompt Builder
# ============================================================

class PromptBuilder:

    def __init__(self):

        self.system = SYSTEM_PROMPT.strip()

    # --------------------------------------------------------

    def build(
        self,
        data: PromptInput,
    ) -> str:

        sections = []

        sections.append(self.system)

        # ----------------------------------------------------
        # Conversation
        # ----------------------------------------------------

        if data.conversation:

            sections.append(
                self._section(
                    "Conversation History",
                    data.conversation,
                )
            )

        # ----------------------------------------------------
        # Semantic Memory
        # ----------------------------------------------------

        if data.memory:

            sections.append(
                self._section(
                    "Relevant Memories",
                    data.memory,
                )
            )

        # ----------------------------------------------------
        # Knowledge
        # ----------------------------------------------------

        if data.knowledge:

            sections.append(
                self._section(
                    "Knowledge Base",
                    data.knowledge,
                )
            )

        # ----------------------------------------------------
        # Draft
        # ----------------------------------------------------

        if data.draft:

            sections.append(
                self._section(
                    f"Draft ({data.draft.name})",
                    data.draft.text,
                )
            )

        # ----------------------------------------------------
        # Sources
        # ----------------------------------------------------

        if data.sources:

            sections.append(
                self._section(
                    "Knowledge Sources",
                    "\n".join(
                        f"- {src}"
                        for src in data.sources
                    ),
                )
            )

        # ----------------------------------------------------
        # User Question
        # ----------------------------------------------------

        sections.append(
            self._section(
                "Current Request",
                data.question,
            )
        )

        return "\n\n".join(sections)

    # --------------------------------------------------------

    @staticmethod
    def _section(
        title: str,
        body: str,
    ) -> str:

        return (
            f"## {title}\n\n"
            f"{body.strip()}"
        )
