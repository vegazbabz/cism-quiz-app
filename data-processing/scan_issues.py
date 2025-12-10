"""
CISM Questions - Comprehensive Issue Scanner
Finds remaining formatting, spacing, and content issues
"""
import json
import re
from pathlib import Path
from collections import defaultdict

def scan_json():
    """Scan the JSON file for common issues"""
    json_path = Path(__file__).parent.parent / "cism_questions.json"
    
    if not json_path.exists():
        print(f"❌ File {json_path} not found!")
        return
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("=" * 80)
    print("CISM Questions - Comprehensive Issue Scanner")
    print("=" * 80 + "\n")
    
    issues = defaultdict(list)
    
    for i, q in enumerate(data):
        q_num = q.get('number')
        
        # Check for double spaces
        for key in ['question', 'explanation']:
            text = q.get(key, '')
            if '  ' in text:  # Double space
                issues['double_spaces'].append(f"Q{q_num} {key}")
        
        # Check for choices with double spaces
        choices = q.get('choices', {})
        for letter, choice_text in choices.items():
            if '  ' in choice_text:
                issues['double_spaces'].append(f"Q{q_num} choice {letter}")
        
        # Check for incomplete explanations
        if not q.get('explanation'):
            issues['missing_explanation'].append(f"Q{q_num}")
        
        # Check for missing answer
        if not q.get('answer'):
            issues['missing_answer'].append(f"Q{q_num}")
        
        # Check for mismatched answer (answer not in choices)
        answer = q.get('answer')
        if answer and answer not in choices:
            issues['invalid_answer'].append(f"Q{q_num} (answer: {answer})")
        
        # Check for Unicode issues (control characters, etc.)
        full_text = json.dumps(q)
        if re.search(r'[\x00-\x08\x0B-\x0C\x0E-\x1F]', full_text):
            issues['control_characters'].append(f"Q{q_num}")
        
        # Check for common OCR artifacts
        artifacts = [
            (r'\d\. [A-Z]', 'numbered_choice_pattern'),  # "1. A" instead of "A"
            (r'\bO [A-Z]', 'letter_o_pattern'),  # "O A" instead of "A"
            (r'\s+\.\s+', 'spacing_period'),  # " . " spacing
            (r'\s+,\s+', 'spacing_comma'),  # " , " spacing
        ]
        
        for pattern, issue_type in artifacts:
            if re.search(pattern, q.get('question', '') + ' ' + q.get('explanation', '')):
                if issue_type not in issues or f"Q{q_num}" not in issues[issue_type]:
                    issues[issue_type].append(f"Q{q_num}")
        
        # Check for weird spacing around possessives (catch any remaining)
        text = json.dumps(q)
        if re.search(r"[a-z]\s{2,}[a-z]", text):  # Multiple spaces between words
            issues['multiple_spaces'].append(f"Q{q_num}")
    
    # Print results
    if not any(issues.values()):
        print("✅ No issues found! JSON is clean.")
        return
    
    for issue_type, question_list in sorted(issues.items()):
        print(f"\n⚠️  {issue_type.upper()}: {len(question_list)} issue(s)")
        for item in sorted(set(question_list))[:10]:  # Show first 10
            print(f"   - {item}")
        if len(question_list) > 10:
            print(f"   ... and {len(question_list) - 10} more")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    scan_json()

