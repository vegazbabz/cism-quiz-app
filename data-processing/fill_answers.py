"""
CISM Questions Answer & Explanation Filler
Parses the choices in the existing JSON and extracts answers and explanations
"""
import json
import re
from pathlib import Path

def extract_answer_and_explanation(choices):
    """
    Extract answer letter and explanation from choices.
    The correct answer is the one with the longest text containing explanation.
    Pattern: Answer letter contains answer letter + explanation text
    """
    answer = None
    explanation = ""
    
    # Find which choice contains the explanation (usually the longest or has "incorrect" in other choices)
    choice_lengths = {k: len(v) for k, v in choices.items()}
    
    # The choice with explanation usually contains "incorrect" keywords or is significantly longer
    for letter, text in choices.items():
        if text and isinstance(text, str):
            # Look for keywords that indicate this is the explanation choice
            if any(keyword in text.lower() for keyword in ['is incorrect', 'are incorrect', 'is the best', 'stands for', 'defines']):
                answer = letter
                explanation = text
                break
    
    # If no answer found yet, find the longest choice (often contains explanation)
    if not answer:
        longest_choice = max(choice_lengths.items(), key=lambda x: x[1])
        answer = longest_choice[0]
        explanation = choices.get(answer, "")
    
    return answer, explanation

def process_json():
    """Process the existing cism_questions.json and fill in answers and explanations"""
    json_path = Path(__file__).parent.parent / "cism_questions.json"
    
    if not json_path.exists():
        print(f"❌ File {json_path} not found!")
        return
    
    print("📖 Loading questions from cism_questions.json...")
    with open(json_path, 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    print(f"✓ Loaded {len(questions)} questions")
    print("\n🔍 Extracting answers and explanations...")
    
    updated_count = 0
    for i, question in enumerate(questions):
        choices = question.get('choices', {})
        if choices:
            answer, explanation = extract_answer_and_explanation(choices)
            if answer:
                question['answer'] = answer
                question['explanation'] = explanation
                updated_count += 1
        
        if (i + 1) % 50 == 0:
            print(f"   Processed {i + 1}/{len(questions)} questions...")
    
    print(f"\n✓ Updated {updated_count} questions")
    
    # Save updated JSON
    print("\n💾 Saving updated questions...")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    
    print("✓ Successfully saved to cism_questions.json")
    
    # Verify
    print("\n✅ Verification:")
    answered = sum(1 for q in questions if q.get('answer'))
    print(f"   Questions with answers: {answered}/{len(questions)}")
    
    # Show a sample
    print(f"\n📋 Sample (Question 1):")
    q = questions[0]
    print(f"   Number: {q['number']}")
    print(f"   Question: {q['question'][:100]}...")
    print(f"   Answer: {q['answer']}")
    print(f"   Explanation: {q['explanation'][:150]}...")

if __name__ == "__main__":
    print("=" * 80)
    print("CISM Questions - Answer & Explanation Filler")
    print("=" * 80 + "\n")
    process_json()
    print("\n" + "=" * 80)

