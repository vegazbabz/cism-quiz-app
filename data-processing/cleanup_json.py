"""
CISM Questions - JSON Cleanup Script
Fixes common formatting issues like curly quotes, spaced words, etc.
"""
import json
import re
from pathlib import Path

def cleanup_text(text):
    """Clean up common formatting issues in text"""
    if not isinstance(text, str):
        return text
    
    # Fix curly quotes and smart quotes
    text = text.replace('\u2019', "'")  # Right single quote (U+2019)
    text = text.replace('\u2018', "'")  # Left single quote (U+2018)
    text = text.replace('\u201d', '"')  # Right double quote (U+201D)
    text = text.replace('\u201c', '"')  # Left double quote (U+201C)
    text = text.replace('–', '-')  # En dash
    text = text.replace('—', '-')  # Em dash
    text = text.replace(''', "'")  # Right single quote (fallback)
    text = text.replace(''', "'")  # Left single quote (fallback)
    text = text.replace('"', '"')  # Left double quote (fallback)
    text = text.replace('"', '"')  # Right double quote (fallback)
    
    # Fix spaced words - these commonly appear as:
    # "or ganization" -> "organization"
    # "of ficer" -> "officer"
    # "dif ferent" -> "different"
    # "dif ficult" -> "difficult"
    # "ef fectiveness" -> "effectiveness"
    # "ef fective" -> "effective"
    # "ef fort" -> "effort"
    # "insuf ficient" -> "insufficient"
    
    spaced_patterns = [
        ("or ganization's", "organization's"),  # Fix possessive with space
        ('or ganization', 'organization'),
        ('of ficer', 'officer'),
        ('dif ferent', 'different'),
        ('dif ficult', 'difficult'),
        ('ef fectiveness', 'effectiveness'),
        ('ef fective', 'effective'),
        ('ef fort', 'effort'),
        ('insuf ficient', 'insufficient'),
        ('har dened', 'hardened'),
        ('ar guably', 'arguably'),
        ('for gone', 'forgone'),
        ('jar gon', 'jargon'),
        ('staf f', 'staff'),
        ('tar get', 'target'),
        ('r esponsibility', 'responsibility'),
        ('\u2019 s', "'s"),  # Fix space before 's with smart quote
        ('\u2018 s', "'s"),  # Fix other variant
        ("' s", "'s"),  # Fix space before 's
    ]
    
    for spaced, fixed in spaced_patterns:
        text = text.replace(spaced, fixed)
    
    # Fix common OCR/extraction artifacts
    text = text.replace('[e]nsures', 'ensures')
    text = text.replace('SMAR T', 'SMART')
    
    return text

def process_json():
    """Process the JSON file and clean up formatting issues"""
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
    changes_by_type = {
        'question': 0,
        'explanation': 0,
        'choice': 0
    }
    
    print("\n🔍 Scanning and cleaning formatting issues...")
    
    for i, question in enumerate(questions):
        # Clean question text
        old_q = question.get('question', '')
        new_q = cleanup_text(old_q)
        if old_q != new_q:
            question['question'] = new_q
            changes_by_type['question'] += 1
            total_changes += 1
        
        # Clean explanation
        old_exp = question.get('explanation', '')
        new_exp = cleanup_text(old_exp)
        if old_exp != new_exp:
            question['explanation'] = new_exp
            changes_by_type['explanation'] += 1
            total_changes += 1
        
        # Clean choices
        choices = question.get('choices', {})
        for letter, choice_text in choices.items():
            old_choice = choice_text
            new_choice = cleanup_text(choice_text)
            if old_choice != new_choice:
                choices[letter] = new_choice
                changes_by_type['choice'] += 1
                total_changes += 1
        
        if (i + 1) % 50 == 0:
            print(f"   Processed {i + 1}/{len(questions)} questions...")
    
    print(f"\n✓ Found and fixed {total_changes} issues:")
    for issue_type, count in changes_by_type.items():
        if count > 0:
            print(f"   - {issue_type}: {count} fixes")
    
    # Save updated JSON
    print("\n💾 Saving cleaned questions...")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    
    print("✓ Successfully saved to cism_questions.json")
    
    # Show a sample
    print(f"\n📋 Sample fixes (Question 1):")
    q = questions[0]
    print(f"   Question: {q['question'][:100]}...")
    print(f"   Explanation: {q['explanation'][:150]}...")

if __name__ == "__main__":
    print("=" * 80)
    print("CISM Questions - JSON Cleanup")
    print("=" * 80 + "\n")
    process_json()
    print("\n" + "=" * 80)

