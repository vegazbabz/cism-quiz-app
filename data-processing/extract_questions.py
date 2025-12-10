"""
CISM Quiz Question Extractor
Extracts questions, answers, and explanations from CISM PDF
"""
import PyPDF2
import json
import re
from pathlib import Path


class CISMQuestionExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.questions = []
        
    def extract_text_from_pdf(self):
        """Extract all text from the PDF"""
        text = ""
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return None
    
    def parse_questions(self, text):
        """Parse questions from extracted text"""
        # Pattern to match question numbers (e.g., "1.", "2.", etc.)
        question_pattern = r'\n(\d+)\.\s+(.*?)(?=\n\d+\.\s+|\Z)'
        
        # Pattern to match answer choices
        choice_pattern = r'([A-D])\.\s+(.*?)(?=[A-D]\.|$)'
        
        # Find all questions
        questions = re.finditer(question_pattern, text, re.DOTALL)
        
        for match in questions:
            question_num = match.group(1)
            question_block = match.group(2)
            
            # Split into question text and rest
            lines = question_block.split('\n')
            
            # Extract question text (everything before choices)
            question_text = []
            choices = {}
            answer = None
            explanation = ""
            
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                
                # Check if this is a choice line
                if re.match(r'^[A-D]\.\s+', line):
                    # Start collecting choices
                    choice_match = re.match(r'^([A-D])\.\s+(.*)', line)
                    if choice_match:
                        choice_letter = choice_match.group(1)
                        choice_text = choice_match.group(2)
                        choices[choice_letter] = choice_text
                elif line and not choices:
                    question_text.append(line)
                
                i += 1
            
            if question_text and choices:
                self.questions.append({
                    'number': int(question_num),
                    'question': ' '.join(question_text),
                    'choices': choices,
                    'answer': None,  # To be filled manually or from answer key
                    'explanation': None  # To be filled manually or from answer key
                })
    
    def save_to_json(self, output_path):
        """Save extracted questions to JSON file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.questions, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(self.questions)} questions to {output_path}")
    
    def extract_and_save(self, output_path):
        """Main method to extract and save questions"""
        print("Extracting text from PDF...")
        text = self.extract_text_from_pdf()
        
        if text:
            print("Parsing questions...")
            self.parse_questions(text)
            print("Saving to JSON...")
            self.save_to_json(output_path)
            return True
        return False


def main():
    # Path to the PDF file
    pdf_path = input("Enter the path to the CISM PDF file: ").strip('"')
    
    if not Path(pdf_path).exists():
        print(f"Error: File not found at {pdf_path}")
        return
    
    output_path = str(Path(__file__).parent.parent / "cism_questions.json")
    
    extractor = CISMQuestionExtractor(pdf_path)
    success = extractor.extract_and_save(output_path)
    
    if success:
        print(f"\n✓ Successfully extracted questions to {output_path}")
        print("Note: You may need to manually review and add answers/explanations.")
    else:
        print("\n✗ Failed to extract questions")


if __name__ == "__main__":
    main()

