"""
CISM Web-based Quiz Application
Flask app for interactive browser-based quizzing
"""
from flask import Flask, render_template, jsonify, request
import json
from pathlib import Path
from datetime import datetime
import random
import os

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Get the directory where the app is running
BASE_DIR = Path(__file__).parent.parent
QUESTIONS_FILE = BASE_DIR / "cism_questions.json"
CHAPTERS_FILE = BASE_DIR / "chapter_overviews.json"
questions = []
chapters = []

# Track file modification times for smart caching
_questions_mtime = None
_chapters_mtime = None

def load_questions():
    """Load questions from JSON file if modified or not loaded"""
    global questions, _questions_mtime
    try:
        if QUESTIONS_FILE.exists():
            current_mtime = os.path.getmtime(QUESTIONS_FILE)
            # Only reload if file was modified or hasn't been loaded yet
            if _questions_mtime is None or current_mtime != _questions_mtime:
                with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
                    questions = json.load(f)
                _questions_mtime = current_mtime
                print(f"✓ Loaded {len(questions)} questions from {QUESTIONS_FILE}")
    except FileNotFoundError:
        print(f"Warning: {QUESTIONS_FILE} not found!")
        questions = []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {QUESTIONS_FILE}")
        questions = []

# Load questions on startup
load_questions()

def load_chapters():
    """Load chapter overviews if available and not already cached"""
    global chapters, _chapters_mtime
    try:
        if CHAPTERS_FILE.exists():
            current_mtime = os.path.getmtime(CHAPTERS_FILE)
            # Only reload if file was modified or hasn't been loaded yet
            if _chapters_mtime is None or current_mtime != _chapters_mtime:
                with open(CHAPTERS_FILE, 'r', encoding='utf-8') as f:
                    chapters = json.load(f)
                _chapters_mtime = current_mtime
                print(f"✓ Loaded {len(chapters)} chapters from {CHAPTERS_FILE}")
        else:
            chapters = []
    except Exception as exc:
        print(f"Warning loading chapters: {exc}")
        chapters = []

# Load chapters on startup
load_chapters()

@app.route('/')
def index():
    """Serve the main quiz page"""
    return render_template('quiz.html')

@app.route('/api/chapters')
def get_chapters():
    """API endpoint to get chapter overviews"""
    # Load/reload chapters if file has been modified
    load_chapters()
    
    response = jsonify({
        'chapters': chapters,
        'total': len(chapters)
    })
    # Prevent stale caching of chapter content
    response.headers['Cache-Control'] = 'no-store'
    return response

@app.route('/api/questions')
def get_questions():
    """API endpoint to get all questions"""
    # Load/reload questions if file has been modified
    load_questions()
    
    response = jsonify({
        'questions': questions,
        'total': len(questions)
    })
    # Prevent stale caching of questions
    response.headers['Cache-Control'] = 'no-store'
    return response

@app.route('/api/questions/shuffled')
def get_shuffled_questions():
    """API endpoint to get shuffled questions"""
    # Load/reload questions if file has been modified
    load_questions()
    
    shuffled = questions.copy()
    random.shuffle(shuffled)
    response = jsonify({
        'questions': shuffled,
        'total': len(shuffled)
    })
    # Prevent stale caching of questions
    response.headers['Cache-Control'] = 'no-store'
    return response

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

@app.route('/api/statistics')
def get_statistics():
    """Get quiz statistics from results file"""
    results_file = BASE_DIR / "quiz_results.txt"
    
    if not results_file.exists():
        return jsonify({'results': [], 'total': 0})
    
    results = []
    try:
        with open(results_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Parse results - each result is between separator lines
        entries = content.split('=' * 80)
        for entry in entries:
            entry = entry.strip()
            if not entry:
                continue
                
            lines = entry.split('\n')
            result = {}
            for line in lines:
                if line.startswith('Quiz Date:'):
                    result['date'] = line.replace('Quiz Date:', '').strip()
                elif line.startswith('Score:'):
                    # Parse "Score: 25/50 (50.0%)"
                    score_part = line.replace('Score:', '').strip()
                    if '(' in score_part:
                        score_str, pct_str = score_part.split('(')
                        result['score_display'] = score_str.strip()
                        result['percentage'] = pct_str.replace(')', '').strip()
                        # Extract numeric values
                        if '/' in score_str:
                            score, total = score_str.split('/')
                            result['score'] = int(score.strip())
                            result['total'] = int(total.strip())
            
            if result.get('date'):
                results.append(result)
        
        # Reverse to show most recent first
        results.reverse()
        
    except Exception as e:
        print(f"Error reading statistics: {e}")
        return jsonify({'results': [], 'total': 0, 'error': str(e)})
    
    return jsonify({'results': results, 'total': len(results)})

@app.route('/api/progress', methods=['GET', 'POST'])
def manage_progress():
    """Get or save quiz progress"""
    PROGRESS_FILE = BASE_DIR / "quiz_progress.json"
    
    if request.method == 'GET':
        # Return saved progress
        try:
            if PROGRESS_FILE.exists():
                with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
                    progress = json.load(f)
                return jsonify({'progress': progress, 'found': True})
        except Exception as e:
            print(f"Error reading progress: {e}")
        return jsonify({'progress': None, 'found': False})
    
    elif request.method == 'POST':
        # Save progress
        try:
            data = request.json
            with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            print(f"✓ Saved quiz progress")
            return jsonify({'success': True, 'message': 'Progress saved'})
        except Exception as e:
            print(f"Error saving progress: {e}")
            return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/progress/clear', methods=['DELETE'])
def clear_progress():
    """Clear saved progress"""
    PROGRESS_FILE = BASE_DIR / "quiz_progress.json"
    try:
        if PROGRESS_FILE.exists():
            PROGRESS_FILE.unlink()
        print(f"✓ Cleared quiz progress")
        return jsonify({'success': True, 'message': 'Progress cleared'})
    except Exception as e:
        print(f"Error clearing progress: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "=" * 80)
    print("CISM Quiz - Web Application")
    print("=" * 80)
    print("\n🌐 Starting web server...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server\n")
    print("=" * 80 + "\n")
    app.run(debug=True, use_reloader=False)
