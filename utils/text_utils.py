
import re

def normalize_text(text: str) -> str:
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def minutes_to_readable(minutes: int) -> str:
    if minutes < 60:
        return f"{minutes} min"

    hours = minutes // 60
    mins = minutes % 60

    if mins == 0:
        return f"{hours} hours"

    return f"{hours} hour {mins} min"
