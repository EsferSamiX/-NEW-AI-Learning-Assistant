from typing import List, Dict

from services.core.groq_client import get_groq_response

from utils.prompt_templates import (
    SINGLE_QUESTION_EVALUATION_PROMPT,
    FINAL_EXAM_EVALUATION_PROMPT,
)



# SINGLE QUESTION EVALUATION (10 MARKS)


def evaluate_single_answer(
    question: str,
    student_answer: str,
    reference_context: str,
) -> Dict:
    """
    Evaluates one answer out of 10 marks.
    """

    prompt = SINGLE_QUESTION_EVALUATION_PROMPT.format(
        question=question,
        student_answer=student_answer,
        reference_context=reference_context,
    )

    response = get_groq_response(
        prompt=prompt,
        temperature=0.15,
        max_tokens=300,
    )

    return {
        "question": question,
        "evaluation": response,
    }



# MULTI-QUESTION EXAM EVALUATION


def evaluate_exam_answers(
    questions: List[str],
    student_answers: List[str],
    reference_context: str,
) -> str:
    """
    Evaluates multiple questions as a full exam.

    ✔ Each question = 10 marks
    ✔ Total = N × 10
    ✔ No fake questions allowed
    """

    if len(questions) != len(student_answers):
        raise ValueError("Questions and answers length mismatch.")

    max_score = len(questions) * 10

    detailed_blocks = []

    for idx, (question, answer) in enumerate(
        zip(questions, student_answers), start=1
    ):
        result = evaluate_single_answer(
            question=question,
            student_answer=answer,
            reference_context=reference_context,
        )

        detailed_blocks.append(
            f"""
==============================
Question {idx}
==============================
{result['evaluation']}
"""
        )

    combined_evaluations = "\n".join(detailed_blocks)

    final_prompt = FINAL_EXAM_EVALUATION_PROMPT.format(
        num_questions=len(questions),
        max_score=max_score,
        combined_evaluations=combined_evaluations,
    )

    final_response = get_groq_response(
        prompt=final_prompt,
        temperature=0.2,
        max_tokens=900,
    )

    return final_response

