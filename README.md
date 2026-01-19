# Persona2Hire

A desktop application for analyzing CVs (Curriculum Vitae) and matching candidates to job sectors based on their qualifications, skills, and MBTI personality types.

> **Project History**: This project originated as a high school computer science project in 2022. It was extended in 2026 with machine learning capabilities for adaptive scoring and continuous improvement.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [How It Works](#how-it-works)
  - [CV Parsing](#cv-parsing)
  - [Job Matching & Scoring](#job-matching--scoring)
  - [Personality Analysis](#personality-analysis)
  - [Machine Learning Pipeline](#machine-learning-pipeline)
- [Scoring System Deep Dive](#scoring-system-deep-dive)
- [Shortcomings & Limitations](#shortcomings--limitations)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Testing](#testing)

---

## Overview

Persona2Hire is a Python/Tkinter desktop application designed to help with candidate screening and job matching. It parses structured CV files, analyzes candidates against 30+ job sectors, and provides personality insights using MBTI and Big Five frameworks.

The system uses a **rule-based scoring algorithm** with optional **machine learning enhancement** that can adapt scores based on feedback and hiring outcomes.

---

## Features

| Feature | Description |
|---------|-------------|
| **CV Parsing** | Robust key-based parsing of structured text files with multi-format date support |
| **CV Creation** | Form-based interface for creating new CVs with validation |
| **Job Matching** | Analyze candidates against 30+ sectors with normalized 0-100 scoring |
| **Personality Analysis** | MBTI (16 types) and Big Five (OCEAN) personality profiling |
| **Skill Gap Analysis** | Identify missing skills for specific roles |
| **Candidate Ranking** | Sort and compare candidates for positions |
| **Filtering** | Filter by nationality, age, experience, skills, languages |
| **ML Scoring** | Optional adaptive scoring that learns from feedback |
| **Export** | Save analysis results to CSV |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Persona2Hire                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────┐   ┌────────────────┐   ┌─────────────────────────┐  │
│  │ CV Files   │──▶│ Parser         │──▶│ Structured CV Data      │  │
│  │ (.txt)     │   │ (parser.py)    │   │ (dict)                  │  │
│  └────────────┘   └────────────────┘   └───────────┬─────────────┘  │
│                                                     │                │
│                   ┌─────────────────────────────────┼────────────┐  │
│                   │                                 │            │  │
│                   ▼                                 ▼            │  │
│  ┌────────────────────────────┐   ┌────────────────────────────┐ │  │
│  │ Job Analyzer               │   │ Personality Analyzer       │ │  │
│  │ - Education scoring        │   │ - MBTI type detection      │ │  │
│  │ - Work experience scoring  │   │ - Big Five profiling       │ │  │
│  │ - Skills matching          │   │ - Career suggestions       │ │  │
│  │ - Language scoring         │   └────────────────────────────┘ │  │
│  │ - Soft skills scoring      │                                  │  │
│  └──────────────┬─────────────┘                                  │  │
│                 │                                                 │  │
│                 ▼                                                 │  │
│  ┌────────────────────────────┐   ┌────────────────────────────┐ │  │
│  │ Rule-Based Score           │◀─▶│ ML Pipeline (Optional)     │ │  │
│  │ (0-100 + personality bonus)│   │ - Feature extraction       │ │  │
│  └──────────────┬─────────────┘   │ - Gradient boosting model  │ │  │
│                 │                 │ - Score adjustment         │ │  │
│                 │                 └────────────────────────────┘ │  │
│                 ▼                                                 │  │
│  ┌────────────────────────────────────────────────────────────┐  │  │
│  │ GUI (Tkinter)                                               │  │  │
│  │ - Candidate list with scores                                │  │  │
│  │ - Score breakdown visualization                             │  │  │
│  │ - Filtering and ranking                                     │  │  │
│  └────────────────────────────────────────────────────────────┘  │  │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## How It Works

### CV Parsing

The parser (`persona2hire/cv/parser.py`) reads structured text files using a **label-based approach**:

1. **Label Detection**: Scans each line for known field labels (e.g., `First-Name :`, `Workplace 1 :`)
2. **Value Extraction**: Extracts text after the first colon on matching lines
3. **Nested Fields**: Tracks context (e.g., which workplace is being described) to associate dates, occupations, and activities correctly

**Supported Date Formats**:
- `DD.MM.YYYY` (European)
- `MM/DD/YYYY` (US)
- `YYYY-MM-DD` (ISO)
- `Month YYYY` (e.g., "June 2020")

The parser is fault-tolerant: it ignores unknown lines and handles encoding variations (UTF-8 with Latin-1 fallback).

### Job Matching & Scoring

The job analyzer (`persona2hire/analysis/job_analyzer.py`) calculates a score by evaluating six categories plus a personality bonus. Each job sector has associated keywords defined in `job_sectors.py`.

**How Matching Works**:
1. For each category, relevant CV fields are extracted
2. Text is normalized (lowercased, stripped)
3. Keywords from the sector definition are matched against the CV text
4. Matches are counted and converted to a normalized score
5. All category scores are summed for the total

**Example - Skills Matching**:
```python
# Sector defines required skills
required_skills = ["python", "sql", "git", "agile"]

# CV contains
computer_skills = "Python, JavaScript, Git, Docker"

# Matching: 2/4 required skills found (python, git)
# Score contribution: 50% of max skills points
```

### Personality Analysis

The personality analyzer (`persona2hire/analysis/personality_analyzer.py`) determines MBTI type from CV content:

1. **Text Sources**: Analyzes `ShortDescription`, `Hobbies`, and skills fields
2. **Word Matching**: Compares words against curated lists for each MBTI dimension:
   - **I/E**: introverted vs. extroverted traits
   - **S/N**: sensing (practical) vs. intuition (creative)
   - **T/F**: thinking (logical) vs. feeling (empathetic)
   - **J/P**: judging (organized) vs. perceiving (flexible)
3. **Hobby Mapping**: Specific hobbies contribute to personality scores (e.g., "reading" → Introversion, "sports" → Extroversion)
4. **Score Calculation**: For each dimension, the letter with the higher accumulated score is chosen

**Big Five (OCEAN)** analysis works similarly, matching words to high/low indicators for:
- Openness, Conscientiousness, Extroversion, Agreeableness, Neuroticism

### Machine Learning Pipeline

The ML system (added in 2026) enhances rule-based scores through learned adjustments:

**Feature Extraction** (`ml/feature_extractor.py`):
Converts CV data into 31 numerical features:

| Category | Features |
|----------|----------|
| Education (5) | level, field match, university prestige, years, has masters |
| Work (6) | total years, positions, seniority, field match, current employment, tenure |
| Skills (5) | required match, extra match, driving license, computer skills count, total skills |
| Languages (4) | count, has English, max level, mother tongue tier |
| Soft Skills (3) | categories matched, leadership, communication |
| Additional (4) | publications, awards, projects, memberships |
| Personality (4) | exact match, partial match, introversion, thinking scores |

**Model Training** (`ml/model.py`):
- Uses **Gradient Boosting Regression** (scikit-learn) or a simple linear model as fallback
- Trains on synthetic data generated to match realistic CV patterns
- Can be retrained with real feedback (hiring outcomes, score corrections)

**Score Adjustment**:
```python
# The ML model doesn't replace the rule-based score
# Instead, it provides an adjustment factor (capped at ±30%)
adjustment = min(1.3, max(0.7, ml_score / rule_score))
final_score = rule_score * adjustment
```

---

## Scoring System Deep Dive

### Category Weights

| Category | Max Points | Breakdown |
|----------|------------|-----------|
| **Education** | 25 | Qualification level (0-10) + Field match (0-10) + University prestige (0-5) |
| **Work Experience** | 30 | Years worked (0-12) + Seniority level (0-8) + Sector relevance (0-10) |
| **Skills** | 20 | Required skills match (70%) + Extra skills match (30%) + Driving license bonus |
| **Languages** | 10 | Mother tongue tier + Additional languages × proficiency level |
| **Soft Skills** | 10 | Categories matched (communication, leadership, teamwork, problem-solving, etc.) |
| **Additional** | 5 | Publications + Awards + Projects + Presentations + Memberships |
| **Personality Bonus** | +5 | Full bonus if MBTI matches sector preference, half for partial match |

### Detailed Scoring Logic

#### Education Score (25 points max)

**Qualification Level (0-10 points)**:
| Level | Keywords | Points |
|-------|----------|--------|
| 6 | PhD, Doctorate | 10 |
| 5 | Master's, MBA | 8.3 |
| 4 | Bachelor's, BSc, BA | 6.7 |
| 3 | Diploma, A-Levels | 5 |
| 2 | Certificate, Vocational | 3.3 |
| 1 | High School, GCSE | 1.7 |

**Field Match (0-10 points)**:
- Each matching keyword in subjects studied: +2 points
- Each matching keyword in qualifications: +1.5 points
- Each matching keyword in master's degrees: +2 points
- Capped at 10 points total

**University Prestige (0-5 points)**:
- Top 50 university: 5 points
- Top 100 university: 3.5 points
- Any university/college: 2 points

#### Work Experience Score (30 points max)

**Years of Experience (0-12 points)**:
- Calculated from date ranges in work history
- Formula: `min(12, total_years × 1.2)`
- 10+ years gives maximum points

**Seniority Level (0-8 points)**:
| Level | Keywords | Points |
|-------|----------|--------|
| 6 | Chairman, Founder, Owner | 8 |
| 5 | CEO, CTO, CFO, President | 6.7 |
| 4 | Director, VP, Senior Manager | 5.3 |
| 3 | Manager, Head, Project Manager | 4 |
| 2 | Senior, Lead, Specialist | 2.7 |
| 1 | Associate, Analyst, Developer | 1.3 |
| 0 | Intern, Junior, Entry-level | 0 |

**Sector Relevance (0-10 points)**:
- Each matching work keyword: +2.5 points
- Keywords from sector's `WorkExperience` list
- Capped at 10 points

#### Skills Score (20 points max)

```python
required_ratio = matched_required / total_required
extra_ratio = matched_extra / total_extra
score = (required_ratio × 0.7 + extra_ratio × 0.3) × 20
# Plus 1 point bonus if has valid driving license
```

#### Language Score (10 points max)

**Mother Tongue**:
- Tier 3 languages (English, Mandarin, Spanish, etc.): 3 points
- Tier 2 languages (Hindi, Russian, Korean, etc.): 2 points
- Tier 1 languages (others): 1 point

**Additional Languages**:
- Contribution = tier × proficiency_level × 0.5
- CEFR levels: A1=0.2, A2=0.3, B1=0.5, B2=0.7, C1=0.9, C2=1.0

#### Personality Bonus (+5 points max)

Each job sector defines preferred MBTI types:
- **Exact Match**: Full 5 points
- **Partial Match** (first 2 letters same): 2.5 points
- **No Match**: 0 points

Example: `Computers_ICT` prefers INTJ, INTP, ISTJ, ENTJ. An INTP candidate gets +5, an INFP gets +2.5 (IN match).

---

## Shortcomings & Limitations

### CV Parsing Limitations

1. **Rigid Format Requirement**: CVs must follow the specific template structure. Free-form CVs or PDFs are not supported.
2. **Single Language**: The parser expects English field labels; multi-language CVs may fail to parse correctly.
3. **Limited Work History**: Only 3 workplace entries are supported, which may not capture full career history.
4. **No Semantic Understanding**: The parser does pattern matching only; it cannot infer meaning from context.

### Scoring System Limitations

1. **Keyword-Based Matching**: Skills matching relies on exact keyword presence. "React.js" won't match "React", and synonyms aren't recognized.
2. **No Industry Context**: A senior developer at a startup is scored the same as one at a Fortune 500 company.
3. **Limited Soft Skills Assessment**: Soft skills are inferred from text presence, not demonstrated through behavioral examples.
4. **Static Weights**: Category weights are fixed and may not reflect actual importance for specific roles.
5. **No Salary/Compensation Context**: The system doesn't consider market value or compensation expectations.
6. **Recency Bias Absent**: Old experience and recent experience are weighted equally.

### Personality Analysis Limitations

1. **Text-Based Inference**: MBTI type is guessed from word patterns, not actual psychological assessment. Results should be treated as rough estimates only.
2. **Limited Signal**: Short descriptions and hobbies provide minimal data for accurate personality typing.
3. **Cultural Bias**: Word associations for personality traits reflect Western/English-speaking interpretations.
4. **Simplified Model**: The 16-type MBTI framework is itself scientifically debated; reducing it to keyword matching adds further simplification.

### Machine Learning Limitations

1. **Synthetic Training Data**: Initial model is trained on generated data, not real hiring outcomes.
2. **Cold Start Problem**: ML adjustment is minimal until enough feedback is collected.
3. **Feedback Quality Dependency**: Model improvement depends on accurate user feedback.
4. **Feature Engineering**: The 31 features may not capture all factors relevant to job success.
5. **Sector Generalization**: The model doesn't learn sector-specific patterns well with limited data.

### General Limitations

1. **No External Validation**: Skills claims aren't verified against certifications or tests.
2. **Bias Potential**: System may inadvertently favor certain educational or professional backgrounds.
3. **No Portfolio/Work Samples**: Creative or technical work quality isn't assessed.
4. **Single Point in Time**: The system analyzes current CV state without considering career trajectory patterns.

---

## Installation

### Requirements

- Python 3.10 or higher
- Tkinter (included with standard Python)
- Optional: scikit-learn, numpy (for ML features)

### Setup

   ```bash
# Clone the repository
git clone <repository-url>
   cd Persona2Hire

# Create virtual environment (recommended)
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
   pip install -r requirements.txt
   ```

---

## Usage

### Running the Application

```bash
python run.py
# or
python -m persona2hire.main
```

### Quick Start Guide

1. **Select Job Sector**: Choose from the dropdown (30+ sectors available)
2. **Load CVs**: Click "Load CV File(s)" and select from `samples/` folder
3. **Analyze**: Click "Analyze All" to score all loaded candidates
4. **View Details**: Click a candidate row to see:
   - Score breakdown with progress bars
   - Matched/missing skills
   - Personality analysis

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+N | Create New CV |
| Ctrl+O | Load CV Files |
| Ctrl+Enter | Analyze All |
| Ctrl+E | Export Results |
| Delete | Remove Selected |

### Using ML Scoring

```bash
# Train initial model
python -m scripts.train_model --initial --samples 200

# Check model status
python -m scripts.train_model --status

# Generate sample CVs
python -m scripts.generate_samples --count 20
```

---

## Project Structure

```
Persona2Hire/
├── persona2hire/              # Main package
│   ├── main.py                # Application entry point
│   ├── data/                  # Data definitions
│   │   ├── job_sectors.py     # 30+ sectors with keywords
│   │   ├── personality.py     # MBTI & Big Five definitions
│   │   └── constants.py       # Qualifications, languages, universities
│   ├── analysis/              # Analysis engines
│   │   ├── job_analyzer.py    # Scoring algorithm
│   │   └── personality_analyzer.py  # MBTI/Big Five analysis
│   ├── cv/                    # CV operations
│   │   ├── parser.py          # Text file parsing
│   │   └── writer.py          # CV file creation
│   ├── gui/                   # Tkinter interface
│   │   ├── main_window.py     # Main application window
│   │   ├── cv_form.py         # CV creation form
│   │   ├── dialogs.py         # Filter dialogs
│   │   └── results.py         # Results display
│   └── ml/                    # Machine learning (2026)
│       ├── feature_extractor.py  # 31 feature extraction
│       ├── model.py           # Gradient boosting model
│       ├── data_generator.py  # Synthetic data generation
│       ├── feedback.py        # Feedback collection
│       └── pipeline.py        # ML orchestration
├── scripts/                   # Utility scripts
│   ├── train_model.py         # ML model training
│   └── generate_samples.py    # Sample CV generation
├── docs/                      # Documentation
│   └── ML_PIPELINE.md         # ML system documentation
├── templates/                 # CV templates
├── samples/                   # Sample CV files
├── tests/                     # Test suite (114+ tests)
├── run.py                     # Simple entry point
├── requirements.txt           # Dependencies
└── pyproject.toml             # Project configuration
```

---

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=persona2hire

# Run specific test file
pytest tests/test_job_analyzer.py

# Run with verbose output
pytest -v
```

The test suite includes 114+ tests covering:
- CV parsing and validation
- CV file writing
- Job matching algorithms
- Candidate filtering
- Personality analysis
- Date format parsing
- ML feature extraction

---

## CV File Format

CVs must follow the template in `templates/cv_template.txt`:

```
Curriculum Vitae
       
First-Name : John
Last-Name : Doe
Address :
    Street Name : Main Street
    House Number : 123
    City : London
    Country : UK
Telephone Number : +44 123 456 789
E-mail Address : john.doe@email.com

Sex : M
Date of Birth : 15.06.1990
Nationality : British

Work Experience :
    Workplace 1 : Tech Company Ltd
        Dates : 01.01.2020 - current
        Occupation : Senior Developer
        Main activities : Python development, team leadership
...
```

See `samples/` for complete examples.

---

## Job Sectors

The system supports 30+ job sectors across categories:

| Category | Sectors |
|----------|---------|
| **Science** | Biological/Chemical/Pharmaceutical, Biomedical/Medtech, Physics/Mathematics |
| **Technology** | Computers/ICT, Engineering/Manufacturing |
| **Healthcare** | Healthcare, Psychology/Social Care |
| **Creative** | Art/Craft/Design, Media/Film, Music/Performing Arts, Fashion/Beauty |
| **Business** | Banking/Finance, Marketing/PR, Business Management, Accountancy |
| **Public** | Law, Education, Public Administration, Security/Defence |
| **Other** | Construction, Tourism, Transport/Logistics, Food/Beverages |

Each sector defines:
- **School/College keywords**: Education fields that match
- **WorkExperience keywords**: Relevant job titles and industries
- **Skills**: Required technical skills
- **ExtraSkills**: Nice-to-have advanced skills
- **Personality**: Preferred MBTI types
