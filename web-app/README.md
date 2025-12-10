# CISM Web Application

A Flask-based web application for interactive CISM practice exam quizzing.

## Features

- 🌐 Browser-based quiz interface
- ❓ Multiple choice questions (A, B, C, D)
- 📝 Answer explanations for all choices
- 📊 Performance tracking
- ⚡ Real-time feedback
- 🎯 Detailed choice explanations on wrong answers

## Setup

### Prerequisites
- Python 3.7 or higher

### Installation & Running

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the application:**
   
   Navigate to the web-app folder:
   ```bash
   cd "c:\Git\CISM-quiz-app\web-app"
   ```
   
   Run via Python (use full path if `python` command is not in PATH):
   ```bash
   python app.py
   ```
   
   Or if Python is not in PATH:
   ```bash
   "C:/Users/nma/AppData/Local/Programs/Python/Python314/python.exe" app.py
   ```

3. **Open in browser:**
   ```
   http://localhost:5000
   ```

## Project Structure

- `app.py` - Main Flask application and API endpoints
- `cism_quiz.py` - Alternative command-line quiz interface
- `templates/` - HTML templates for the web interface
- `requirements.txt` - Python dependencies

## Data

The application uses `../cism_questions.json` which is stored in the parent directory and shared with data-processing scripts.

## API Endpoints

- `GET /` - Load the quiz interface
- `GET /api/questions` - Get all questions
- `GET /api/question/<number>` - Get a specific question
- `POST /api/check-answer` - Submit and check an answer
  - Returns: correct answer, full explanation, and explanations for all choices

## Key Features

- **Comprehensive Feedback:** Displays explanations for all answer choices when a user selects an incorrect answer
- **Correct Answer Details:** Returns the correct answer and detailed explanation
- **Progress Tracking:** Tracks quiz results and performance metrics
