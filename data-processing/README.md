# Data Processing Scripts

Tools for extracting, cleaning, and validating CISM practice exam data.

## Overview

This folder contains all scripts used for:
- PDF extraction and question parsing
- Answer and explanation population
- Data cleaning and formatting fixes
- Quality verification and validation

## Scripts

### Extraction
- `extract_questions_v2.py` - Advanced PDF extractor with pattern matching
- `extract_questions.py` - Basic PDF extraction script
- `EXTRACTION_GUIDE.md` - Detailed extraction documentation

### Data Population
- `fill_answers.py` - Populate answers and explanations from choice text
- `cleanup_json.py` - Fix formatting issues (spaced words, quotes, OCR artifacts)
- `fix_smart_quotes.py` - Fix Unicode smart quotes
- `fix_all_apostrophes.py` - Fix possessive apostrophe spacing
- `fix_spaced_words.py` - Fix random spaces in the middle of words

### Validation & Verification
- `verify_quality.py` - Comprehensive data quality check
- `verify_json.py` - Quick JSON structure verification
- `scan_issues.py` - Scan for specific formatting issues
- `search_quotes.py` - Search for remaining quote issues

## Usage

All scripts reference the JSON file from the parent directory (`../cism_questions.json`).

### Run any script:
```bash
python script_name.py
```

### Example workflow:
```bash
# Extract questions from PDF
python extract_questions_v2.py

# Clean up formatting
python cleanup_json.py

# Verify data quality
python verify_quality.py
```

## Data File Location

The shared data file `cism_questions.json` is stored in the parent directory so it can be accessed by both:
- Data processing scripts (for cleaning and validation)
- Web application (for serving to users)

## JSON Structure

```json
{
  "number": 1,
  "question": "Question text here",
  "choices": {
    "A": "Choice A text",
    "B": "Choice B text",
    "C": "Choice C text",
    "D": "Choice D text"
  },
  "answer": "C",
  "explanation": "Detailed explanation"
}
```
