# CISM Quiz Application - Setup Guide

## Quick Start with PDF Extraction

### Step 1: Extract Questions from PDF

Run the advanced extractor:

```powershell
cd c:\Git\CISM-quiz-app
C:/Users/nma/AppData/Local/Programs/Python/Python314/python.exe extract_questions_v2.py
```

When prompted, enter the full path to your PDF:
```
C:\Users\nma\Downloads\CISM 2022\cism-certified-information-security-manager-practice-exams-second-edition-9781264693740.pdf
```

The extractor will:
- ✓ Read all pages from the PDF
- ✓ Extract all 300 questions
- ✓ Parse answers and explanations
- ✓ Save to `cism_questions.json`

### Step 2: Start the Web Application

```powershell
C:/Users/nma/AppData/Local/Programs/Python/Python314/python.exe C:\Git\CISM-quiz-app\app.py
```

Then open your browser to: **http://localhost:5000**

## What's New

### ✅ Improved PDF Extractor (`extract_questions_v2.py`)
- Better parsing of question structure
- Handles multi-line questions and choices
- Extracts all 300 questions from the CISM exam
- Better error handling and progress reporting

### ✅ Fixed Scrolling
- All questions now load completely
- No pagination needed
- Smooth scrolling through all 300 questions

### ✅ Button Explanations
- Welcome page now explains all three modes
- Clear descriptions of when to use each mode

## Quiz Modes Explained

### ▶️ Start Quiz
- Questions appear in their original order
- You select an answer and see feedback immediately
- Your score is calculated when you complete or end the quiz
- Perfect for simulating the actual exam

### 🔀 Shuffle Questions  
- Same as Start Quiz but questions are randomized
- Prevents memorization by order
- Great for varied practice sessions
- Tests true understanding

### 📖 Practice Mode
- All questions visible with answers shown immediately
- Detailed explanations visible right away
- Perfect for learning and studying
- No scoring - focus on understanding

## Troubleshooting

### Questions not loading?
Make sure `cism_questions.json` exists in the `c:\Git\CISM-quiz-app` directory.

### Extraction failed?
Try the advanced extractor: `extract_questions_v2.py`

### Still having issues?
Check the terminal output for error messages.

## File Structure
```
c:\Git\CISM-quiz-app\
├── app.py                      # Flask web server
├── extract_questions.py        # Original extractor
├── extract_questions_v2.py     # Advanced extractor
├── cism_quiz.py               # Command-line version
├── cism_questions.json        # All 300 questions (auto-generated)
├── requirements.txt           # Python dependencies
└── templates/
    └── quiz.html              # Web interface
```

Good luck with your CISM exam! 📚
