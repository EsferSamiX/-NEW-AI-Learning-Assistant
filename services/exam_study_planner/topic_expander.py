from services.core.groq_client import get_groq_response
from services.exam_study_planner.planner_utils import (
    difficulty_prompt_hint,
)

from utils.prompt_templates import TOPIC_EXPANSION_PROMPT


def expand_topic_into_subtopics(
    topic: str,
    difficulty: str = "medium",
) -> list[str]:
    """
    Expands a single chapter into curriculum-appropriate subtopics.

    Difficulty controls:
    - easy   → basic school-level breakdown
    - medium → standard curriculum
    - hard   → deeper analytical coverage
    """

    difficulty_hint = difficulty_prompt_hint(difficulty)

    prompt = TOPIC_EXPANSION_PROMPT.format(
        topic=topic,
        difficulty_upper=difficulty.upper(),
        difficulty_hint=difficulty_hint,
    )

    response = get_groq_response(
        prompt=prompt,
        temperature=0.25 if difficulty == "hard" else 0.2,
        max_tokens=400,
    )

    lines = response.splitlines()
    subtopics: list[str] = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if line[0].isdigit():
            cleaned = (
                line.split(".", 1)[1]
                if "." in line
                else line.split(")", 1)[1]
            ).strip()

            if cleaned:
                subtopics.append(cleaned)

    
    # FALLBACK PROTECTION (NON-LLM SAFETY)
    

    if len(subtopics) < 4:

        if difficulty == "easy":
            subtopics = [
                f"Introduction to {topic}",
                "Basic definitions",
                "Main ideas overview",
                "Simple examples",
                "Important terms",
                "Revision summary",
            ]

        elif difficulty == "hard":
            subtopics = [
                f"Conceptual foundations of {topic}",
                "Detailed internal mechanisms",
                "Mathematical or logical structure",
                "Process flow analysis",
                "Limitations and assumptions",
                "Advanced examples",
                "Common misconceptions",
                "Exam-oriented problem solving",
            ]

        else:
            subtopics = [
                f"Introduction to {topic}",
                "Key concepts",
                "Important components",
                "Functions and roles",
                "Working mechanism",
                "Examples and diagrams",
                "Summary and revision",
            ]

    return subtopics
