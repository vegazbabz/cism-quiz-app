# CISM Quiz Application

A comprehensive CISM (Certified Information Security Manager) exam preparation platform with both command-line and web-based interfaces.

## Project Structure

```
CISM-quiz-app/
├── web-app/                 # Flask web application
│   ├── app.py               # Main Flask server
│   ├── cism_quiz.py         # CLI quiz interface
│   ├── requirements.txt      # Python dependencies
│   └── templates/           # HTML templates
├── data-processing/         # Data extraction & validation scripts
│   ├── extract_questions_v2.py
│   ├── cleanup_json.py
│   ├── consolidate_chapter_text.py
│   ├── verify_quality.py
│   └── EXTRACTION_GUIDE.md
├── cism_questions.json      # Question database (300 questions)
├── chapter_overviews.json   # Chapter organization & overviews
└── README.md
```

## Features

- 📚 Interactive quiz interfaces (CLI & Web)
- 🔀 Multiple quiz modes (Standard, Shuffle, Practice, Custom Length)
- 💬 Instant feedback with detailed explanations
- 📊 Real-time performance tracking and scoring
- 💾 **Persistent quiz progress** - Auto-saves after each answer, survives server restarts and browser refreshes
- 💾 Save quiz results and track progress
- 📈 View Statistics: Review past quiz results with detailed history and performance metrics
- 🎯 Chapter-based organization with overviews
- ⏱️ Built-in timer for timed practice
- 🌐 Modern, responsive browser-based web interface
- 📝 Command-line interface for quick practice
- 🎨 Visual feedback (color-coded correct/incorrect answers)
- 🔄 Smart caching with live file reloading (edit JSON files while server is running)

## Quick Start

### Web Application (Recommended)
```powershell
cd web-app
pip install -r requirements.txt
python app.py
# Open http://localhost:5000 in your browser
```

### Command-Line Interface
```powershell
cd web-app
pip install -r requirements.txt
python cism_quiz.py
```

## Folders

### `/web-app`
Flask-based web application for browser-based quizzing.
- Features: Real-time feedback, all choice explanations, performance tracking
- See [web-app/README.md](web-app/README.md) for details

### `/data-processing`
Scripts for extracting questions from PDF, cleaning data, and validation.
- Extract from CISM practice exam PDFs
- Fix formatting issues and validate data quality
- See [data-processing/README.md](data-processing/README.md) for details

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. **Clone this repository**

2. **For Web Application:**
   ```powershell
   cd web-app
   pip install -r requirements.txt
   python app.py
   ```

3. **For Command-Line:**
   ```powershell
   cd web-app
   pip install -r requirements.txt
   python cism_quiz.py
   ```

## Data

The application uses `cism_questions.json` (300 CISM practice exam questions) which is shared between:
- **Web Application** (`web-app/app.py`) - Serves questions via API
- **CLI Application** (`web-app/cism_quiz.py`) - Loads for practice sessions
- **Data Processing Scripts** (`data-processing/*`) - For extraction, cleaning, and validation

### JSON Structure
```json
{
  "number": 1,
  "question": "Question text",
  "choices": {
    "A": "Choice A",
    "B": "Choice B",
    "C": "Choice C",
    "D": "Choice D"
  },
  "answer": "C",
  "explanation": "Detailed explanation"
}
```

## Data Processing

To extract and prepare questions from a PDF:

```powershell
cd data-processing
python extract_questions_v2.py
python cleanup_json.py
python verify_quality.py
```

See [data-processing/README.md](data-processing/README.md) for full documentation.

3. **Run the quiz application:**
   ```powershell
   python cism_quiz.py
   ```

## Quiz Modes

### 1. Full Quiz
Take all available questions in order.

### 2. Custom Quiz
Specify how many questions you want to practice (e.g., 25 questions).

### 3. Practice Mode
Review questions with answers shown immediately - perfect for learning and memorization.

### 4. Shuffle Questions
Randomize question order for varied practice sessions.

### 5. View Statistics
Review your past quiz results and track improvement over time. Available in both web and CLI interfaces.

## Question File Format

Questions are stored in JSON format with the following structure:

```json
{
  "number": 1,
  "question": "Question text here?",
  "choices": {
    "A": "First option",
    "B": "Second option",
    "C": "Third option",
    "D": "Fourth option"
  },
  "answer": "B",
  "explanation": "Detailed explanation of why B is correct..."
}
```

## Customization

### Adding Your Own Questions

1. Edit `cism_questions.json` directly, or
2. Create a new JSON file following the format above
3. When running the quiz, specify your custom file path when prompted

### Modifying Extracted Questions

After running `extract_questions.py`, you may need to:
- Verify question text accuracy
- Add correct answers (if not auto-detected)
- Add explanations for each question

## Tips for Exam Preparation

1. **Start with Practice Mode** - Familiarize yourself with questions and explanations
2. **Use Shuffle Mode** - Avoid memorizing question order
3. **Take Custom Quizzes** - Build stamina with timed 25-50 question sessions
4. **Review Statistics** - Identify weak areas and track improvement
5. **Repeat Incorrect Questions** - Focus on areas where you struggle

## Files Overview

- `cism_quiz.py` - Main quiz application
- `extract_questions.py` - PDF question extractor
- `cism_questions.json` - Questions database
- `quiz_results.txt` - Saved quiz results (auto-generated)
- `requirements.txt` - Python dependencies

## Troubleshooting

### PDF Extraction Issues
If extraction doesn't work properly:
- Ensure the PDF is not password-protected
- Check that the PDF has selectable text (not just scanned images)
- You may need to manually create/edit the questions JSON file

### Missing Dependencies
```powershell
pip install --upgrade -r requirements.txt
```

## Study Resources

- Official ISACA CISM Review Manual
- ISACA CISM Practice Questions Database
- Domain-specific study guides

## Exam Domains Covered

1. **Information Security Governance** (17%)
2. **Information Risk Management** (20%)
3. **Information Security Program** (33%)
4. **Incident Management** (30%)

## License

For personal educational use only. Respect copyright laws regarding the source material.

## Contributing

Feel free to add more questions, improve the extraction logic, or enhance the quiz interface.

## Good Luck! 🎓

Remember: The CISM exam requires both knowledge and experience. Use this tool to reinforce concepts, but also gain practical experience in information security management.

---

**Note:** This application is designed to help you practice. Always refer to official ISACA materials for the most accurate and up-to-date exam content.
