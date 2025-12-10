"""
CISM Questions - Fix ALL apostrophe + space + s patterns
Including regular apostrophes followed by space and 's'
"""
import json
import re
from pathlib import Path

def fix_all_possessive_spacing(text):
    """
    Fix ALL variations of apostrophe/quote + space + 's'
    This includes both smart quotes and regular apostrophes
    """
    if not isinstance(text, str):
        return text
    
    # Replace ANY apostrophe-like character followed by space and 's'
    # This catches: ' s, ' s, ' s, 's, etc.
    
    # Pattern to match: any quote-like character (including regular apostrophe) + spaces + 's'
    text = re.sub(r"['\u2019\u2018\u201d\u201c]\s+s\b", "'s", text)
    
    return text

def process_json():
    """Process the JSON file and fix all apostrophe spacing issues"""
    json_path = Path(__file__).parent.parent / "cism_questions.json"
    
    if not json_path.exists():
        print(f"❌ File {json_path} not found!")
        return
    
    print("📖 Loading questions from cism_questions.json...")
    with open(json_path, 'r', encoding='utf-8') as f:
        questions = json.load(f)
    
    print(f"✓ Loaded {len(questions)} questions")
    
    # Track changes
    total_changes = 0
    changes_detail = []
    
    print("\n🔍 Scanning and fixing all apostrophe + space + s patterns...")
    
    for i, question in enumerate(questions):
        # Fix question text
        old_q = question.get('question', '')
        new_q = fix_all_possessive_spacing(old_q)
        if old_q != new_q:
            question['question'] = new_q
            total_changes += 1
            changes_detail.append(f"Q{question['number']} question")
        
        # Fix explanation
        old_exp = question.get('explanation', '')
        new_exp = fix_all_possessive_spacing(old_exp)
        if old_exp != new_exp:
            question['explanation'] = new_exp
            total_changes += 1
            changes_detail.append(f"Q{question['number']} explanation")
        
        # Fix choices
        choices = question.get('choices', {})
        for letter, choice_text in choices.items():
            old_choice = choice_text
            new_choice = fix_all_possessive_spacing(choice_text)
            if old_choice != new_choice:
                choices[letter] = new_choice
                total_changes += 1
                changes_detail.append(f"Q{question['number']} choice {letter}")
        
        if (i + 1) % 50 == 0:
            print(f"   Processed {i + 1}/{len(questions)} questions...")
    
    print(f"\n✓ Found and fixed {total_changes} apostrophe spacing issues")
    
    if changes_detail and total_changes <= 20:
        print("\n📋 Fixed items:")
        for change in changes_detail:
            print(f"   - {change}")
    
    # Save updated JSON
    print("\n💾 Saving cleaned questions...")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    
    print("✓ Successfully saved to cism_questions.json")
    
    # Verify
    print(f"\n✅ Verification:")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    remaining = 0
    for q in data:
        text = json.dumps(q)
        if re.search(r"['\u2019\u2018\u201d\u201c]\s+s\b", text):
            remaining += 1
    
    print(f"   Remaining issues: {remaining}")

if __name__ == "__main__":
    print("=" * 80)
    print("CISM Questions - Apostrophe Spacing Fixer")
    print("=" * 80 + "\n")
    process_json()
    print("\n" + "=" * 80)

