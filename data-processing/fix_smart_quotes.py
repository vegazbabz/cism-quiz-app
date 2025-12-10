"""
CISM Questions - Find and Fix All Smart Quote Possessives
Identifies and fixes all variations of smart quotes with space before 's'
"""
import json
import re
from pathlib import Path

def fix_smart_quote_possessives(text):
    """
    Fix all variations of smart quotes with space before 's'
    Including: ' s, ' s, ' s, etc.
    """
    if not isinstance(text, str):
        return text
    
    # Replace all variations of smart/curly quotes followed by space and 's'
    # Using Unicode escape sequences to avoid syntax issues
    text = re.sub(r'\u2019\s+s\b', "'s", text)  # Right single quote + space + s
    text = re.sub(r'\u2018\s+s\b', "'s", text)  # Left single quote + space + s
    text = re.sub(r'\u201d\s+s\b', "'s", text)  # Right double quote + space + s
    text = re.sub(r'\u201c\s+s\b', "'s", text)  # Left double quote + space + s
    text = re.sub(r"'\s+s\b", "'s", text)       # Regular apostrophe + space + s
    
    return text

def process_json():
    """Process the JSON file and fix all smart quote possessives"""
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
    
    print("\n🔍 Scanning and fixing smart quote possessives...")
    
    for i, question in enumerate(questions):
        # Fix question text
        old_q = question.get('question', '')
        new_q = fix_smart_quote_possessives(old_q)
        if old_q != new_q:
            question['question'] = new_q
            total_changes += 1
        
        # Fix explanation
        old_exp = question.get('explanation', '')
        new_exp = fix_smart_quote_possessives(old_exp)
        if old_exp != new_exp:
            question['explanation'] = new_exp
            total_changes += 1
        
        # Fix choices
        choices = question.get('choices', {})
        for letter, choice_text in choices.items():
            old_choice = choice_text
            new_choice = fix_smart_quote_possessives(choice_text)
            if old_choice != new_choice:
                choices[letter] = new_choice
                total_changes += 1
        
        if (i + 1) % 50 == 0:
            print(f"   Processed {i + 1}/{len(questions)} questions...")
    
    print(f"\n✓ Found and fixed {total_changes} smart quote possessive issues")
    
    # Save updated JSON
    print("\n💾 Saving cleaned questions...")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    
    print("✓ Successfully saved to cism_questions.json")
    
    # Verify some samples
    print(f"\n📋 Sample verification (checking for remaining ' s patterns):")
    remaining_issues = 0
    for i, q in enumerate(questions[:10]):
        for key in ['question', 'explanation']:
            text = q.get(key, '')
            if re.search(r'.\s+s\b', text) and "'" in text:
                # Manual check for actual remaining issues
                matches = re.findall(r"'\s+s\b", text)
                if matches:
                    remaining_issues += len(matches)
                    print(f"   Q{q['number']} {key}: Found {len(matches)} issue(s)")
    
    if remaining_issues == 0:
        print("   ✓ No remaining issues found in sample!")

if __name__ == "__main__":
    print("=" * 80)
    print("CISM Questions - Smart Quote Possessive Fixer")
    print("=" * 80 + "\n")
    process_json()
    print("\n" + "=" * 80)

