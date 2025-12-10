"""
Search for all apostrophe + space + s patterns
"""
import json
import re

with open(str(Path(__file__).parent.parent / "cism_questions.json"), 'r', encoding='utf-8') as f:
    data = json.load(f)

issues = []
pattern = re.compile(r"['\u2019\u2018]\s+s\b")

for q in data:
    for key in ['question', 'explanation']:
        text = q.get(key, '')
        matches = pattern.findall(text)
        if matches:
            issues.append({
                'question_num': q['number'],
                'field': key,
                'matches': len(matches),
                'text_snippet': text[:80] + '...'
            })

if issues:
    print(f"Found {len(issues)} issues:")
    for issue in issues[:10]:
        print(f"  Q{issue['question_num']} ({issue['field']}): {issue['matches']} match(es)")
        print(f"    {issue['text_snippet']}")
else:
    print("No issues found!")

