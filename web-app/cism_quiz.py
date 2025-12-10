"""
CISM Interactive Quiz Application
Presents multiple choice questions with explanations
"""
import json
import random
import os
from pathlib import Path
from datetime import datetime


class CISMQuiz:
    def __init__(self, questions_file):
        self.questions_file = questions_file
        self.questions = []
        self.current_question = 0
        self.score = 0
        self.incorrect_questions = []
        self.load_questions()
        
    def load_questions(self):
        """Load questions from JSON file"""
        try:
            with open(self.questions_file, 'r', encoding='utf-8') as f:
                self.questions = json.load(f)
            print(f"✓ Loaded {len(self.questions)} questions")
        except FileNotFoundError:
            print(f"Error: Questions file '{self.questions_file}' not found!")
            print("Please run extract_questions.py first or create a questions file.")
            self.questions = []
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in '{self.questions_file}'")
            self.questions = []
    
    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_question(self, question):
        """Display a single question with choices"""
        self.clear_screen()
        print("=" * 80)
        print(f"Question {question['number']} of {len(self.questions)}")
        print("=" * 80)
        print(f"\n{question['question']}\n")
        
        for letter in sorted(question['choices'].keys()):
            print(f"  {letter}. {question['choices'][letter]}")
        print()
    
    def get_user_answer(self):
        """Get and validate user input"""
        while True:
            answer = input("Your answer (A/B/C/D, or 'Q' to quit): ").strip().upper()
            if answer in ['A', 'B', 'C', 'D', 'Q']:
                return answer
            print("Invalid input. Please enter A, B, C, D, or Q to quit.")
    
    def show_explanation(self, question, user_answer, is_correct):
        """Show whether answer was correct and display explanation"""
        print("\n" + "-" * 80)
        if is_correct:
            print("✓ CORRECT! Well done!")
            print(f"Your answer: {user_answer}")
        else:
            print("✗ INCORRECT")
            print(f"Your answer: {user_answer}")
            print(f"Correct answer: {question['answer']}")
        
        # Always show the explanation
        if question.get('explanation'):
            print(f"\n📖 Explanation:")
            print(f"   {question['explanation']}")
        else:
            print(f"\n📖 Correct answer: {question['answer']}. {question['choices'][question['answer']]}")
        
        print("-" * 80)
        print(f"Current Score: {self.score}/{self.current_question}")
        print("-" * 80)
        input("\nPress Enter for next question...")
    
    def run_quiz(self, shuffle=False, num_questions=None):
        """Run the quiz"""
        if not self.questions:
            return
        
        # Prepare questions
        questions_to_use = self.questions.copy()
        if shuffle:
            random.shuffle(questions_to_use)
        if num_questions:
            questions_to_use = questions_to_use[:num_questions]
        
        self.score = 0
        self.incorrect_questions = []
        
        print("\n" + "=" * 80)
        print("CISM PRACTICE QUIZ")
        print("=" * 80)
        print(f"Total questions: {len(questions_to_use)}")
        print("After selecting your answer, you'll see the correct answer immediately!")
        print("=" * 80)
        input("\nPress Enter to start...")
        
        for idx, question in enumerate(questions_to_use):
            self.current_question = idx + 1
            
            # Display question
            self.display_question(question)
            
            # Get user answer
            user_answer = self.get_user_answer()
            
            if user_answer == 'Q':
                print("\nQuiz terminated by user.")
                break
            
            # Check answer immediately
            correct_answer = question.get('answer', '').upper()
            is_correct = (user_answer == correct_answer) if correct_answer else False
            
            if is_correct:
                self.score += 1
            else:
                self.incorrect_questions.append({
                    'number': question['number'],
                    'question': question['question'],
                    'user_answer': user_answer,
                    'correct_answer': correct_answer
                })
            
            # Show answer and explanation immediately
            self.show_explanation(question, user_answer, is_correct)
        
        # Show final results
        self.show_results(len(questions_to_use))
    
    def show_results(self, total_questions):
        """Display final quiz results"""
        self.clear_screen()
        print("\n" + "=" * 80)
        print("QUIZ RESULTS")
        print("=" * 80)
        
        percentage = (self.score / total_questions * 100) if total_questions > 0 else 0
        
        print(f"\nScore: {self.score}/{total_questions} ({percentage:.1f}%)")
        
        # Performance rating
        if percentage >= 90:
            rating = "Excellent! 🌟"
        elif percentage >= 80:
            rating = "Very Good! 👍"
        elif percentage >= 70:
            rating = "Good"
        elif percentage >= 60:
            rating = "Fair"
        else:
            rating = "Needs Improvement"
        
        print(f"Rating: {rating}")
        
        # Show incorrect questions
        if self.incorrect_questions:
            print(f"\n{len(self.incorrect_questions)} question(s) incorrect:")
            print("-" * 80)
            for item in self.incorrect_questions:
                print(f"\nQ{item['number']}: {item['question'][:60]}...")
                print(f"Your answer: {item['user_answer']} | Correct answer: {item['correct_answer']}")
        else:
            print("\n🎉 Perfect score! All questions answered correctly!")
        
        print("\n" + "=" * 80)
        
        # Save results
        self.save_results(total_questions, percentage)
    
    def save_results(self, total_questions, percentage):
        """Save quiz results to file"""
        results_file = "quiz_results.txt"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(results_file, 'a', encoding='utf-8') as f:
            f.write(f"\n{'=' * 80}\n")
            f.write(f"Quiz Date: {timestamp}\n")
            f.write(f"Score: {self.score}/{total_questions} ({percentage:.1f}%)\n")
            if self.incorrect_questions:
                f.write(f"Incorrect questions: {', '.join([str(q['number']) for q in self.incorrect_questions])}\n")
            f.write(f"{'=' * 80}\n")
    
    def practice_mode(self):
        """Practice mode - review questions without scoring"""
        if not self.questions:
            return
        
        print("\n" + "=" * 80)
        print("PRACTICE MODE")
        print("=" * 80)
        print("Review questions and answers at your own pace")
        print("=" * 80)
        input("\nPress Enter to start...")
        
        for question in self.questions:
            self.display_question(question)
            input("\nPress Enter to see the answer...")
            
            print(f"\n✓ Correct Answer: {question.get('answer', 'Not available')}")
            if question.get('explanation'):
                print(f"\nExplanation: {question['explanation']}")
            
            print("\n" + "-" * 80)
            continue_practice = input("\nContinue? (Y/N): ").strip().upper()
            if continue_practice == 'N':
                break


def display_menu():
    """Display main menu"""
    print("\n" + "=" * 80)
    print("CISM QUIZ APPLICATION")
    print("=" * 80)
    print("\n1. Take Full Quiz")
    print("2. Take Custom Quiz (specify number of questions)")
    print("3. Practice Mode (review with answers)")
    print("4. Shuffle Questions")
    print("5. View Statistics")
    print("6. Exit")
    print("\n" + "=" * 80)


def main():
    # Default questions file
    questions_file = "cism_questions.json"
    
    # Check if questions file exists
    if not Path(questions_file).exists():
        print(f"\nWarning: '{questions_file}' not found!")
        custom_path = input("Enter path to questions JSON file (or press Enter to exit): ").strip('"')
        if custom_path:
            questions_file = custom_path
        else:
            print("Exiting...")
            return
    
    quiz = CISMQuiz(questions_file)
    
    if not quiz.questions:
        print("\nNo questions loaded. Exiting...")
        return
    
    while True:
        display_menu()
        choice = input("Select an option (1-6): ").strip()
        
        if choice == '1':
            quiz.run_quiz()
        elif choice == '2':
            try:
                num = int(input("How many questions? "))
                quiz.run_quiz(num_questions=num)
            except ValueError:
                print("Invalid number!")
        elif choice == '3':
            quiz.practice_mode()
        elif choice == '4':
            quiz.run_quiz(shuffle=True)
        elif choice == '5':
            if Path("quiz_results.txt").exists():
                with open("quiz_results.txt", 'r', encoding='utf-8') as f:
                    print(f.read())
            else:
                print("\nNo quiz results found yet.")
            input("\nPress Enter to continue...")
        elif choice == '6':
            print("\nThank you for using CISM Quiz! Good luck with your exam! 📚")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
