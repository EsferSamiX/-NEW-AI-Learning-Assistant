from typing import List, Dict
from utils.planner_profiles import DIFFICULTY_PROFILES



# TOPIC PARSING

def parse_topics(raw_text: str) -> List[Dict]:
    """
    Parses topic input into structured format.

    Format:
    Topic | difficulty
    """

    topics: List[Dict] = []

    for line in raw_text.splitlines():
        line = line.strip()
        if not line:
            continue

        parts = [p.strip() for p in line.split("|")]

        topic = parts[0]

        difficulty = (
            parts[1].lower()
            if len(parts) >= 2 and parts[1]
            else "medium"
        )

        if difficulty not in DIFFICULTY_PROFILES:
            difficulty = "medium"

        topics.append(
            {
                "topic": topic,
                "difficulty": difficulty,
            }
        )

    return topics



# TOPIC COUNT LOGIC


def is_single_topic(topics: List[Dict]) -> bool:
    """
    Returns True when only one chapter is provided.
    """
    return len(topics) == 1



# DIFFICULTY WEIGHT


def difficulty_weight(level: str) -> float:
    """
    Relative difficulty multiplier.
    """
    return DIFFICULTY_PROFILES.get(
        level, DIFFICULTY_PROFILES["medium"]
    )["weight"]



# DIFFICULTY PROFILE ACCESSOR


def difficulty_profile(level: str) -> Dict:
    """
    Returns pedagogical profile for difficulty.
    """
    return DIFFICULTY_PROFILES.get(
        level, DIFFICULTY_PROFILES["medium"]
    )


# DIFFICULTY PROMPT HINT


def difficulty_prompt_hint(level: str) -> str:
    """
    Returns LLM instruction hint.
    """
    return DIFFICULTY_PROFILES.get(
        level, DIFFICULTY_PROFILES["medium"]
    )["prompt_hint"]

