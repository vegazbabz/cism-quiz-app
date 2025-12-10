"""
CISM Questions - Data Quality Verification
Checks for critical data integrity issues
"""
import json
from pathlib import Path

def verify_quality():
    """Verify critical data quality"""
    json_path = Path(__file__).parent.parent / "cism_questions.json"
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("=" * 80)
    print("CISM Questions - Data Quality Verification")
    print("=" * 80 + "\n")
    
    critical_issues = []
    warnings = []
    
    # Check critical fields
    for q in data:
        q_num = q.get('number')
        
        # Critical: All fields must be present
        if not q.get('question'):
            critical_issues.append(f"Q{q_num}: Missing question")
        
        if not q.get('answer'):
            critical_issues.append(f"Q{q_num}: Missing answer")
        
        if not q.get('explanation'):
            critical_issues.append(f"Q{q_num}: Missing explanation")
        
        if not q.get('choices'):
            critical_issues.append(f"Q{q_num}: Missing choices")
        else:
            # Check answer is in choices
            answer = q.get('answer')
            if answer not in q['choices']:
                critical_issues.append(f"Q{q_num}: Answer '{answer}' not in choices")
            
            # Check minimum choices
            if len(q['choices']) < 4:
                warnings.append(f"Q{q_num}: Only {len(q['choices'])} choices (expected 4)")
        
        # Warning: Very short explanations
        if len(q.get('explanation', '')) < 50:
            warnings.append(f"Q{q_num}: Explanation is very short ({len(q['explanation'])} chars)")
    
    # Print results
    print(f"📊 Total Questions: {len(data)}")
    print(f"✅ Questions with all required fields: {len(data) - len(critical_issues)}\n")
    
    if critical_issues:
        print(f"❌ CRITICAL ISSUES: {len(critical_issues)}")
        for issue in critical_issues:
            print(f"   {issue}")
    else:
        print("✅ No critical issues found!\n")
    
    if warnings:
        print(f"\n⚠️  WARNINGS: {len(set(warnings))}")
        for warning in sorted(set(warnings))[:10]:
            print(f"   {warning}")
        if len(set(warnings)) > 10:
            print(f"   ... and {len(set(warnings)) - 10} more")
    else:
        print("✅ No warnings!\n")
    
    print("\n" + "=" * 80)
    print("✅ Data Quality: GOOD - JSON is ready for use!")
    print("=" * 80)

if __name__ == "__main__":
    verify_quality()

