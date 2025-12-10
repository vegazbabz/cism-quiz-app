# CISM Web Application

A Flask-based web application for interactive CISM practice exam quizzing.

## Features

- 🌐 Browser-based quiz interface with modern, responsive design
- ❓ Multiple choice questions (A, B, C, D) with 300+ questions
- 📝 Instant answer feedback with detailed explanations
- 📊 Real-time scoring and performance tracking
- 🎯 Multiple quiz modes:
  - **Start Quiz**: All questions in original order with chapter overviews
  - **Shuffle Questions**: Randomized order, no chapters shown
  - **Practice Mode**: All answers visible immediately for study (no scoring)
  - **Custom Length**: Select even number of questions (10, 20, 30...) for shorter randomized quizzes
- 📚 Chapter organization with collapsible overviews
- 🎨 Color-coded feedback (green for correct, red for incorrect)
- ⏱️ Built-in timer with hide/show toggle
- 🔘 Collapsible questions for easier navigation
- 🚀 Quick navigation buttons (scroll to top / go to chapter)
- 💾 **Persistent Quiz Progress**: Auto-saves after each answer, resume where you left off even after browser refresh or server restart
- 💾 Persistent results tracking
- 📊 View Statistics: Track your progress with detailed quiz history and performance metrics

## Setup

### Prerequisites
- Python 3.7 or higher

### Installation & Running

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the application:**
   
   Navigate to the web-app folder, e.g.:
   ```bash
   cd "c:\Git\CISM-quiz-app\web-app"
   ```
   
   Run via Python (use full path if `python` command is not in PATH):
   ```bash
   python app.py
   ```
   
   Or if Python is not in PATH:
   ```bash
   "C:/Users/username/AppData/Local/Programs/Python/Python314/python.exe" app.py
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
- `GET /api/questions` - Get all questions (with smart caching)
- `GET /api/chapters` - Get chapter overviews (with smart caching)
- `POST /api/check-answer` - Submit and check an answer
  - Returns: correct answer, full explanation, and explanations for all choices
- `POST /api/save-result` - Save quiz results to file
- `GET /api/statistics` - Retrieve past quiz results and statistics
- `GET /api/progress` - Get saved quiz progress
- `POST /api/progress` - Save quiz progress (auto-saved after each answer)
- `DELETE /api/progress/clear` - Clear saved progress

## Key Features

- **Comprehensive Feedback:** Displays explanations for all answer choices when a user selects an incorrect answer
- **Correct Answer Details:** Returns the correct answer and detailed explanation
- **Persistent Progress Tracking:** Auto-saves quiz progress after each answer, survives server restarts and browser refreshes
- **Smart Caching:** Live file reloading - edit JSON files while server is running, changes reflect immediately
- **Statistics & Analytics:** Track quiz history and performance metrics
- **Multiple Quiz Modes:** Standard, Shuffle, Practice, and Custom Length options
- **Chapter Navigation:** Jump to any chapter with persistent sidebar navigation
- **Real-time Scoring:** Live score updates with color-coded question feedback
