

from typing import List, Dict


class ConversationMemoryService:
    """
    Lightweight session-based conversational memory.

    Stores recent:
    - user questions
    - assistant answers

    Injected into RAG prompts to support follow-up questions.
    """

    def __init__(self, max_turns: int = 5):
        """
        max_turns:
            Number of recent Q&A pairs to keep.
            5 ≈ last 10 messages (safe for context window)
        """
        self.max_turns = max_turns
        self.history: List[Dict[str, str]] = []


    # Add conversation turn

    def add_turn(self, question: str, answer: str) -> None:
        self.history.append(
            {
                "question": question.strip(),
                "answer": answer.strip(),
            }
        )

        # sliding window memory
        if len(self.history) > self.max_turns:
            self.history = self.history[-self.max_turns :]


    # Build memory context for prompt injection
   
    def get_context(self) -> str:
        """
        Returns compact formatted conversation memory.
        """

        if not self.history:
            return ""

        blocks = []

        for turn in self.history:
            blocks.append(
                f"User: {turn['question']}\n"
                f"Assistant: {turn['answer']}"
            )

        return "\n\n".join(blocks)

  
    # Reset memory
   
    def clear(self) -> None:
        self.history.clear()
