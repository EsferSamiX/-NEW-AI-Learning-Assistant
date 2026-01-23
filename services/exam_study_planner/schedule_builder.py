from datetime import timedelta, date
from typing import List, Dict

from services.exam_study_planner.planner_utils import difficulty_weight


FOCUS_BLOCK = 30  # minutes
MAX_BLOCKS_PER_TOPIC_PER_DAY = 2



# HUMAN-LIKE EXAM STUDY SCHEDULER


def build_schedule(
    topics: List[Dict],
    exam_date: date,
    daily_hours: int,
) -> List[Dict]:

    today = date.today()

    if exam_date <= today:
        raise ValueError("Exam date must be in the future.")

    
    # TIME BUDGET
  
    minutes_per_day = daily_hours * 60
    total_days = (exam_date - today).days
    total_minutes = minutes_per_day * total_days

    if total_minutes <= 0:
        raise ValueError("Insufficient study time.")

    
    # BUILD TOPIC STATES
   
    topic_pool = []
    total_weight = 0.0

    for t in topics:
        w = difficulty_weight(t.get("difficulty", "medium"))
        total_weight += w

        topic_pool.append(
            {
                "topic": t["topic"],
                "difficulty": t.get("difficulty", "medium"),
                "weight": w,
                "remaining": 0,
                "exposure_days": 0,
                "last_seen": -10,
            }
        )

    
    # DISTRIBUTE TOTAL TIME FAIRLY
   
    for t in topic_pool:
        share = t["weight"] / total_weight
        t["remaining"] = max(
            FOCUS_BLOCK * 2,
            int(share * total_minutes),
        )

  
    # SCHEDULING ENGINE
    
    schedule = []
    current_day = today
    day_index = 0

    while current_day < exam_date:

        minutes_left = minutes_per_day
        sessions = []

        
        #  STUDY — INTERLEAVED ROTATION
        
        for topic in topic_pool:

            if minutes_left < FOCUS_BLOCK:
                break

            if topic["remaining"] <= 0:
                continue

            # avoid repeating same topic too much
            if (
                day_index - topic["last_seen"] < 1
                and topic["exposure_days"] >= 1
            ):
                continue

            blocks_today = min(
                MAX_BLOCKS_PER_TOPIC_PER_DAY,
                topic["remaining"] // FOCUS_BLOCK,
            )

            for _ in range(blocks_today):
                if minutes_left < FOCUS_BLOCK:
                    break

                sessions.append(
                    {
                        "type": "study",
                        "topic": topic["topic"],
                        "minutes": FOCUS_BLOCK,
                    }
                )

                topic["remaining"] -= FOCUS_BLOCK
                minutes_left -= FOCUS_BLOCK
                topic["last_seen"] = day_index
                topic["exposure_days"] += 1

      
        #  REVISION — YESTERDAY TOPICS
        
        revision_candidates = [
            t for t in topic_pool
            if t["exposure_days"] >= 1
        ]

        if minutes_left >= FOCUS_BLOCK and revision_candidates:
            topic = revision_candidates[day_index % len(revision_candidates)]

            sessions.append(
                {
                    "type": "revision",
                    "topic": topic["topic"],
                    "minutes": FOCUS_BLOCK,
                }
            )
            minutes_left -= FOCUS_BLOCK

        
        #  PRACTICE
     
        if minutes_left >= FOCUS_BLOCK:
            sessions.append(
                {
                    "type": "practice",
                    "topic": "Practice questions",
                    "minutes": minutes_left,
                }
            )

        schedule.append(
            {
                "date": current_day,
                "sessions": sessions,
            }
        )

        current_day += timedelta(days=1)
        day_index += 1

    
    # FINAL MOCK 
   
    final_mock_day = exam_date - timedelta(days=2)

    if final_mock_day > today:
        schedule.append(
            {
                "date": final_mock_day,
                "sessions": [
                    {
                        "type": "mock_test",
                        "topic": "Full syllabus mock test",
                        "minutes": minutes_per_day,
                    }
                ],
            }
        )

   
    # FINAL REVISION DAY
  
    schedule.append(
        {
            "date": exam_date - timedelta(days=1),
            "sessions": [
                {
                    "type": "final_revision",
                    "topic": "Light revision + rest",
                    "minutes": max(FOCUS_BLOCK, minutes_per_day // 2),
                }
            ],
        }
    )

    schedule.sort(key=lambda x: x["date"])

    return schedule
