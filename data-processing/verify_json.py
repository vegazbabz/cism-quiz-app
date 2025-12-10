import json

with open(str(Path(__file__).parent.parent / "cism_questions.json"), 'r', encoding='utf-8') as f:
    data = json.load(f)
    
print(f"Total questions: {len(data)}")
print("\nFirst 5 questions:")
for i, q in enumerate(data[:5]):
    answer = q.get('answer', 'None')
    exp_len = len(q.get('explanation', ''))
    print(f"Q{q['number']}: answer={answer}, explanation_length={exp_len}")

# Count how many have answers
answered = sum(1 for q in data if q.get('answer'))
print(f"\nQuestions with answers: {answered}/{len(data)}")

