# Data Processing Scripts

Tools for extracting, cleaning, and validating CISM practice exam data.

## Overview

This folder contains scripts used for:
- PDF extraction and question parsing
- Data cleaning and formatting fixes
- Quality verification and validation
- Chapter organization

## Essential Scripts

### Extraction
- **`extract_questions_v2.py`** - Extract questions from CISM PDF with pattern matching and OCR fixes

### Cleanup & Organization
- **`cleanup_json.py`** - Fix formatting issues (spaced words, quotes, OCR artifacts)
- **`consolidate_chapter_text.py`** - Consolidate and organize chapter overview text

### Validation & Verification
- **`verify_quality.py`** - Comprehensive data quality check (structure, content, completeness)

### Documentation
- **`EXTRACTION_GUIDE.md`** - Detailed extraction workflow and documentation

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

# Consolidate chapter text (optional)
python consolidate_chapter_text.py

# Verify data quality
python verify_quality.py
```

## Data File Location

The shared data file `cism_questions.json` is stored in the parent directory so it can be accessed by:
- Data processing scripts (for cleaning and validation)
- Web application (for serving to users)
- CLI application (for command-line practice)

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

## Note

Specialized/one-off scripts have been removed to keep the toolkit focused on essential data preparation tasks.
