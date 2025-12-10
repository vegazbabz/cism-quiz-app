import json
import re
from pathlib import Path

JSON_PATH = Path(__file__).parent.parent / "cism_questions.json"

PATTERNS = [
    "A, B, and",
    "A, B, C",
    "B, C, and",
    "B, C, D",
    "C, D, and",
    "A is incorrect",
    "B is incorrect",
    "C is incorrect",
    "D is incorrect",
]

def trim_choice(text: str) -> str:
    # Try to cut off at the first distractor marker
    for marker in PATTERNS:
        idx = text.find(marker)
        if idx != -1:
            return text[:idx].rstrip(" .;")
    # Fallback to first sentence
    first_period = text.find('.')
    if first_period != -1:
        return text[: first_period + 1].strip()
    return text.strip()

def main():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    fixed = 0
    for q in data:
        ans = q.get("answer")
        if not ans or "choices" not in q:
            continue
        choices = q["choices"]
        if ans not in choices:
            continue
        choice_text = choices[ans]
        expl = q.get("explanation", "")

        # Heuristic: if the correct choice is very long or matches explanation cues
        if not choice_text:
            continue
        needs_fix = False
        if len(choice_text) > 220:
            needs_fix = True
        if choice_text == expl:
            needs_fix = True
        if any(marker in choice_text for marker in PATTERNS):
            needs_fix = True

        if needs_fix:
            new_text = trim_choice(choice_text)
            if new_text and new_text != choice_text:
                choices[ans] = new_text
                fixed += 1

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✓ Fixed {fixed} correct-answer choices")

if __name__ == "__main__":
    main()
