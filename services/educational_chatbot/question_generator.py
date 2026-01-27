from services.core.groq_client import get_groq_response

from utils.prompt_templates import (
    QUESTION_GENERATION_PROMPT,
    QUESTION_DIFFICULTY_INSTRUCTIONS,
)


def generate_questions_from_context(
    context: str,
    num_questions: int = 3,
    difficulty: str = "easy",
):
    """
    Generates domain-agnostic, technically grounded questions
    based strictly on the provided PDF context.

    Supports:
    - science
    - engineering
    - mathematics
    - AI / ML
    - history
    - religion
    - accounting
    - business
    - medical
    - humanities
    """

    difficulty = difficulty.lower().strip()


    # Difficulty resolution
   
    difficulty_instruction = QUESTION_DIFFICULTY_INSTRUCTIONS.get(
        difficulty,
        QUESTION_DIFFICULTY_INSTRUCTIONS["medium"],
    )

    
    # Prompt construction
    
    prompt = QUESTION_GENERATION_PROMPT.format(
        difficulty_instruction=difficulty_instruction,
        context=context,
        num_questions=num_questions,
    )

    
    # LLM call
    
    response = get_groq_response(
        prompt=prompt,
        temperature=0.3,
        max_tokens=500,
    )

   
    # Output parsing
    
    questions = []

    for line in response.splitlines():
        line = line.strip()
        if line and line[0].isdigit():
            questions.append(
                line.split(".", 1)[1].strip()
            )

    return questions

