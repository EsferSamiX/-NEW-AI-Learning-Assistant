from datetime import date
from typing import List, Dict

from services.exam_study_planner.planner_utils import (
    parse_topics,
    is_single_topic,
)

from services.exam_study_planner.schedule_builder import build_schedule
from services.exam_study_planner.topic_expander import (
    expand_topic_into_subtopics,
)


DEFAULT_PRIORITY = "high"


def generate_study_plan(
    exam_date: date,
    daily_hours: int,
    topics_text: str,
) -> List[Dict]:
    """
    High-level intelligent exam study planner.

    Behavior:
    - Multiple chapters → use directly
    - Single chapter → automatically expanded into subtopics
    - Difficulty affects:
        • subtopic depth
        • time allocation
        • schedule density
    """


    # PARSE TOPICS
    
    topics = parse_topics(topics_text)

    if not topics:
        raise ValueError("No topics provided.")


    # AI TOPIC EXPANSION (DIFFICULTY-AWARE)

    if is_single_topic(topics):

        base_topic = topics[0]

        difficulty = base_topic.get("difficulty", "medium")

        subtopics = expand_topic_into_subtopics(
            topic=base_topic["topic"],
            difficulty=difficulty,  
        )

        topics = [
            {
                "topic": f"{base_topic['topic']} — {sub}",
                "difficulty": difficulty,
                "priority": DEFAULT_PRIORITY,
            }
            for sub in subtopics
        ]


    # NORMALIZE FIELDS
   
    for t in topics:
        t.setdefault("difficulty", "medium")
        t.setdefault("priority", DEFAULT_PRIORITY)

 
    # BUILD FINAL STUDY PLAN
    
    plan = build_schedule(
        topics=topics,
        exam_date=exam_date,
        daily_hours=daily_hours,
    )

    return plan
