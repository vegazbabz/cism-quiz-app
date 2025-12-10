"""
Advanced CISM PDF Question Extractor
Extracts all questions, answers, and explanations from CISM practice exam PDF
"""
import PyPDF2
import json
import re
from pathlib import Path
from typing import List, Dict, Tuple


class AdvancedCISMExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.questions = []
        self.text_lines = []
        
    def extract_text_from_pdf(self) -> str:
        """Extract all text from the PDF"""
        text = ""
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                print(f"📄 Total pages: {len(pdf_reader.pages)}")
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                    
                    if (page_num + 1) % 10 == 0:
                        print(f"   Processed {page_num + 1} pages...")
            
            return text
        except Exception as e:
            print(f"❌ Error reading PDF: {e}")
            return None
    
    def parse_questions(self, text: str) -> None:
        """Parse questions with flexible patterns"""
        lines = text.split('\n')
        self.text_lines = [line.strip() for line in lines if line.strip()]
        
        i = 0
        question_count = 0
        
        while i < len(self.text_lines):
            line = self.text_lines[i]
            
            # Look for question number pattern (1., 2., etc.)
            if re.match(r'^\d+\.$', line) or re.match(r'^\d+\.\s', line):
                question_num_match = re.match(r'^(\d+)\.\s*(.*)', line)
                
                if question_num_match:
                    question_num = int(question_num_match.group(1))
                    question_text = question_num_match.group(2).strip()
                    
                    # Collect question text (may span multiple lines)
                    j = i + 1
                    while j < len(self.text_lines):
                        next_line = self.text_lines[j]
                        
                        # Check if this is an answer choice
                        if re.match(r'^[A-D]\.\s', next_line):
                            break
                        
                        # Check if this is next question
                        if re.match(r'^\d+\.$', next_line) or re.match(r'^\d+\.\s', next_line):
                            break
                        
                        if next_line and not re.match(r'^(Answer|Explanation|Copyright|Page \d+)', next_line):
                            question_text += " " + next_line
                        
                        j += 1
                    
                    # Now extract choices
                    choices = {}
                    correct_answer = None
                    explanation = ""
                    
                    while j < len(self.text_lines):
                        curr_line = self.text_lines[j]
                        
                        # Extract choice
                        choice_match = re.match(r'^([A-D])\.\s*(.*)', curr_line)
                        if choice_match:
                            letter = choice_match.group(1)
                            choice_text = choice_match.group(2).strip()
                            
                            # Collect multi-line choices
                            k = j + 1
                            while k < len(self.text_lines):
                                peek = self.text_lines[k]
                                if re.match(r'^[A-D]\.\s', peek) or re.match(r'^Answer:', peek) or re.match(r'^Explanation:', peek) or re.match(r'^\d+\.\s', peek):
                                    break
                                if peek and not re.match(r'^(Copyright)', peek):
                                    choice_text += " " + peek
                                k += 1
                            
                            choices[letter] = choice_text.strip()
                            j = k - 1
                        
                        # Extract answer
                        elif curr_line.startswith('Answer:'):
                            answer_match = re.search(r'Answer:\s*([A-D])', curr_line)
                            if answer_match:
                                correct_answer = answer_match.group(1)
                        
                        # Extract explanation
                        elif curr_line.startswith('Explanation:'):
                            explanation = curr_line.replace('Explanation:', '').strip()
                            k = j + 1
                            while k < len(self.text_lines):
                                peek = self.text_lines[k]
                                if re.match(r'^\d+\.\s', peek) or re.match(r'^Answer:', peek):
                                    break
                                if peek and not re.match(r'^(Copyright|Page \d+)', peek):
                                    explanation += " " + peek
                                k += 1
                            j = k - 1
                        
                        # Stop at next question
                        if re.match(r'^\d+\.\s', curr_line) and curr_line != line:
                            break
                        
                        j += 1
                    
                    # Only add if we have both question and choices
                    if question_text.strip() and len(choices) > 0:
                        self.questions.append({
                            'number': question_num,
                            'question': question_text.strip(),
                            'choices': choices,
                            'answer': correct_answer,
                            'explanation': explanation.strip()
                        })
                        question_count += 1
                    
                    i = j
                else:
                    i += 1
            else:
                i += 1
            
            if question_count % 50 == 0 and question_count > 0:
                print(f"   Extracted {question_count} questions...")
    
    def save_to_json(self, output_path: str) -> bool:
        """Save extracted questions to JSON file"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.questions, f, indent=2, ensure_ascii=False)
            print(f"\n✓ Successfully saved {len(self.questions)} questions to {output_path}")
            return True
        except Exception as e:
            print(f"❌ Error saving JSON: {e}")
            return False
    
    def extract_and_save(self, output_path: str) -> bool:
        """Main method to extract and save questions"""
        print("\n" + "=" * 80)
        print("ADVANCED CISM QUESTION EXTRACTOR")
        print("=" * 80)
        
        print("\n📖 Extracting text from PDF...")
        text = self.extract_text_from_pdf()
        
        if not text:
            print("❌ Failed to extract text from PDF")
            return False
        
        print(f"✓ Extracted {len(text)} characters from PDF")
        
        print("\n🔍 Parsing questions...")
        self.parse_questions(text)
        
        print(f"✓ Found {len(self.questions)} questions")
        
        if len(self.questions) == 0:
            print("⚠️  No questions found. The PDF format may be different.")
            print("Try manually reviewing the PDF structure.")
            return False
        
        print("\n💾 Saving to JSON...")
        success = self.save_to_json(output_path)
        
        if success:
            print("\n" + "=" * 80)
            print(f"✓ Extraction complete! {len(self.questions)} questions ready for quiz")
            print("=" * 80)
        
        return success


def main():
    print("\n" + "=" * 80)
    print("CISM PDF Question Extractor")
    print("=" * 80)
    
    pdf_path = input("\n📁 Enter the path to the CISM PDF file: ").strip().strip('"')
    
    if not Path(pdf_path).exists():
        print(f"\n❌ Error: File not found at {pdf_path}")
        return
    
    output_path = str(Path(__file__).parent.parent / "cism_questions.json")
    
    extractor = AdvancedCISMExtractor(pdf_path)
    success = extractor.extract_and_save(output_path)
    
    if success:
        print("\n✅ You can now use the web quiz application!")
        print("   Start it with: python app.py")
    else:
        print("\n⚠️  Extraction had issues. You may need to manually edit the questions file.")


if __name__ == "__main__":
    main()

