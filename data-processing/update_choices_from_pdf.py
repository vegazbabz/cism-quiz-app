"""
Update choices in cism_questions.json by re-extracting choices from the source PDF.
- Keeps existing question, answer, and explanation intact.
- Replaces only the `choices` for matching question numbers.
"""
import json
from pathlib import Path
from extract_questions_v2 import AdvancedCISMExtractor

PDF_PATH = Path(r"C:\Users\nma\Downloads\CISM 2022\cism-certified-information-security-manager-practice-exams-second-edition-9781264693740.pdf")
JSON_PATH = Path(__file__).parent.parent / "cism_questions.json"


def main():
    if not PDF_PATH.exists():
        print(f"❌ PDF not found: {PDF_PATH}")
        return
    if not JSON_PATH.exists():
        print(f"❌ JSON not found: {JSON_PATH}")
        return

    extractor = AdvancedCISMExtractor(str(PDF_PATH))
    print("📖 Extracting text from PDF (choices only)...")
    text = extractor.extract_text_from_pdf()
    if not text:
        print("❌ Could not extract text from PDF")
        return

    print("🔍 Parsing questions to obtain choices...")
    extractor.parse_questions(text)
    pdf_choices = {q['number']: q['choices'] for q in extractor.questions}
    print(f"✓ Parsed choices for {len(pdf_choices)} questions from PDF")

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    replaced = 0
    missing = 0
    for q in data:
        num = q.get("number")
        if num in pdf_choices:
            q['choices'] = pdf_choices[num]
            replaced += 1
        else:
            missing += 1

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✓ Choices updated for {replaced} questions")
    if missing:
        print(f"⚠️  {missing} questions in JSON had no matching choices in PDF")


if __name__ == "__main__":
    main()
