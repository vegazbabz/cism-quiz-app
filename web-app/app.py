"""
CISM Web-based Quiz Application
Flask app for interactive browser-based quizzing
"""
from flask import Flask, render_template, jsonify, request
import json
from pathlib import Path
from datetime import datetime
import random

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Get the directory where the app is running
BASE_DIR = Path(__file__).parent.parent
QUESTIONS_FILE = BASE_DIR / "cism_questions.json"
questions = []

def load_questions():
    """Load questions from JSON file"""
    global questions
    try:
        with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
            questions = json.load(f)
        print(f"✓ Loaded {len(questions)} questions from {QUESTIONS_FILE}")
    except FileNotFoundError:
        print(f"Warning: {QUESTIONS_FILE} not found!")
        questions = []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {QUESTIONS_FILE}")
        questions = []

# Load questions on startup
load_questions()

@app.route('/')
def index():
    """Serve the main quiz page"""
    return render_template('quiz.html')

@app.route('/api/questions')
def get_questions():
    """API endpoint to get all questions"""
    return jsonify({
        'questions': questions,
        'total': len(questions)
    })

@app.route('/api/questions/shuffled')
def get_shuffled_questions():
    """API endpoint to get shuffled questions"""
    shuffled = questions.copy()
    random.shuffle(shuffled)
    return jsonify({
        'questions': shuffled,
        'total': len(shuffled)
    })

@app.route('/api/check-answer', methods=['POST'])
def check_answer():
    """API endpoint to check if answer is correct"""
    data = request.get_json()
    question_id = data.get('question_id')
    user_answer = data.get('answer', '').upper()
    
    # Find the question
    question = next((q for q in questions if q['number'] == question_id), None)
    
    if not question:
        return jsonify({'error': 'Question not found'}), 404
    
    # Handle None answer values
    correct_answer = question.get('answer') or ''
    if correct_answer:
        correct_answer = correct_answer.upper()
    
    is_correct = (user_answer == correct_answer) if correct_answer else False
    
    # Build explanations for all choices (if present)
    choice_explanations = {}
    choices = question.get('choices', {})
    explanation = question.get('explanation', '') or 'No explanation available.'
    # If explanation contains breakdowns for each choice, parse them (future-proof)
    # For now, use the main explanation for correct, and the distractor text for wrong answers if present
    for key, value in choices.items():
        # If the value contains explanation for wrong answers, use it
        if key == correct_answer:
            # For correct answer, use main explanation
            choice_explanations[key] = explanation
        else:
            # For distractors, if explanation is embedded in value, extract after a period
            if '. ' in value:
                # Take the part after the first period as explanation
                parts = value.split('. ', 1)
                choice_explanations[key] = parts[1].strip() if len(parts) > 1 else ''
            else:
                choice_explanations[key] = ''

    return jsonify({
        'correct': is_correct,
        'correct_answer': correct_answer,
        'explanation': explanation,
        'choice_text': choices.get(correct_answer, '') if correct_answer else '',
        'choice_explanations': choice_explanations
    })

@app.route('/api/save-result', methods=['POST'])
def save_result():
    """Save quiz result to file"""
    data = request.get_json()
    score = data.get('score', 0)
    total = data.get('total', 0)
    
    results_file = BASE_DIR / "quiz_results.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    percentage = (score / total * 100) if total > 0 else 0
    
    with open(results_file, 'a', encoding='utf-8') as f:
        f.write(f"\n{'=' * 80}\n")
        f.write(f"Quiz Date: {timestamp}\n")
        f.write(f"Score: {score}/{total} ({percentage:.1f}%)\n")
        f.write(f"{'=' * 80}\n")
    
    return jsonify({'success': True})

if __name__ == '__main__':
    print("\n" + "=" * 80)
    print("CISM Quiz - Web Application")
    print("=" * 80)
    print("\n🌐 Starting web server...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server\n")
    print("=" * 80 + "\n")
    app.run(debug=True, use_reloader=False)
