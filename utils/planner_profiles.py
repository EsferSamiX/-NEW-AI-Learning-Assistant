# ======================================================
# DIFFICULTY PROFILES
# ======================================================

DIFFICULTY_PROFILES = {
    "easy": {
        "weight": 1.0,
        "depth": "basic understanding",
        "revision_cycles": 1,
        "practice_type": "simple questions",
        "focus": [
            "definitions",
            "basic concepts",
            "examples",
        ],
        "notes": "Focus on understanding fundamentals.",
        "prompt_hint": (
            "Use simple language. Avoid formulas. "
            "Focus on intuition, examples, and basic understanding."
        ),
    },

    "medium": {
        "weight": 1.5,
        "depth": "conceptual + applied",
        "revision_cycles": 2,
        "practice_type": "mixed problems",
        "focus": [
            "definitions",
            "mechanism",
            "process flow",
            "applications",
        ],
        "notes": "Balance theory and application.",
        "prompt_hint": (
            "Explain concepts clearly with working principles "
            "and moderate technical depth."
        ),
    },

    "hard": {
        "weight": 2.2,
        "depth": "advanced mastery",
        "revision_cycles": 3,
        "practice_type": "advanced problems",
        "focus": [
            "internal mechanisms",
            "derivations",
            "edge cases",
            "limitations",
            "design reasoning",
        ],
        "notes": (
            "Focus on deep reasoning, analytical understanding, "
            "and exam-level problem solving."
        ),
        "prompt_hint": (
            "Explain in depth using mechanisms, reasoning, "
            "step-by-step processes, limitations, and exam-oriented insight."
        ),
    },
}
