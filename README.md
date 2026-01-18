# Persona2Hire

A desktop application for analyzing CVs (Curriculum Vitae) and matching candidates to job sectors based on their qualifications, skills, and MBTI personality types.

## Features

- **CV Parsing**: Robust key-based parsing of structured CV text files with multiple date format support
- **CV Creation**: Create new CVs through a modern form-based interface with validation
- **Job Matching**: Analyze candidates against 30+ job sectors with normalized scoring (0-100)
- **Personality-Job Matching**: Bonus points for MBTI personality types that match job sector preferences
- **Personality Analysis**: Determine Myers-Briggs (MBTI) and Big Five personality profiles
- **Skill Gap Analysis**: See what skills a candidate is missing for a specific role
- **Candidate Ranking**: Rank and compare candidates for specific positions
- **Score Breakdown**: Visual progress bars showing scores in each category
- **Candidate Filtering**: Filter candidates by nationality, age, experience, skills, and languages
- **Export to CSV**: Export analysis results to CSV for further processing
- **Keyboard Shortcuts**: Quick actions with Ctrl+N, Ctrl+O, Ctrl+Enter, Ctrl+E
- **Tooltips**: Hover over buttons for usage hints
- **Double-click Support**: Double-click a CV to instantly view personality analysis

## Project Structure

```
Persona2Hire/
├── persona2hire/              # Main package
│   ├── __init__.py
│   ├── main.py                # Application entry point
│   ├── data/                  # Data modules
│   │   ├── job_sectors.py     # Job sector definitions & keywords
│   │   ├── personality.py     # MBTI personality types & Big Five
│   │   └── constants.py       # Functions, qualifications, languages, universities
│   ├── analysis/              # Analysis modules
│   │   ├── job_analyzer.py    # Job matching algorithms (normalized 0-100 scoring)
│   │   └── personality_analyzer.py  # MBTI & Big Five assessment
│   ├── cv/                    # CV file operations
│   │   ├── parser.py          # Robust CV file parsing
│   │   └── writer.py          # CV file writing with validation
│   └── gui/                   # GUI modules
│       ├── main_window.py     # Main application window
│       ├── cv_form.py         # CV creation form
│       ├── dialogs.py         # Filter dialogs
│       └── results.py         # Results display windows
├── templates/                 # CV templates
│   └── cv_template.txt        # Empty CV template
├── samples/                   # Sample CVs for testing
│   ├── cv_example.txt         # Software developer profile
│   └── cv_example_2.txt       # Research scientist profile
├── tests/                     # Test suite
│   ├── conftest.py            # Shared fixtures
│   ├── test_parser.py         # CV parsing tests
│   ├── test_writer.py         # CV writing tests
│   ├── test_job_analyzer.py   # Job analysis tests
│   └── test_personality_analyzer.py  # Personality tests
├── run.py                     # Simple entry point
├── requirements.txt
├── pyproject.toml             # Project config & pytest settings
├── .gitignore
└── README.md
```

## Requirements

- Python 3.10 or higher
- Tkinter (included with Python standard library)
- pytest (for running tests)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/darius024/Persona2Hire.git
   cd Persona2Hire
   ```

2. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. (Optional) Install development dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python run.py
```

Or run as a module:
```bash
python -m persona2hire.main
```

### Quick Start

1. **Select a Job Sector** from the dropdown menu (or type to filter)
2. **Load CVs** by clicking "Load CV File(s)" and selecting files from `samples/`
3. **(Optional) Set Filter Criteria** to narrow down candidates
4. **Analyze All** to rank all loaded candidates for the selected sector
5. **View Details** by selecting a candidate:
   - Click on a candidate row to see score breakdown
   - "Show Jobs Match" - See suitable job sectors ranked
   - "Show Personality" - See MBTI and Big Five personality analysis
6. **Export Results** to save the analysis to a CSV file

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+N | Create New CV |
| Ctrl+O | Load CV Files |
| Ctrl+Enter | Analyze All |
| Ctrl+E | Export Results |
| Delete | Remove Selected |
| Escape | Close Dropdown |

### Creating a New CV

1. Click "Create New CV"
2. Fill in the form (First Name and Last Name are required)
3. Click "Create CV" to save

Created CVs are automatically saved to the `CVs/` directory.

## Scoring System

The job matching uses a normalized 0-100 scoring system with personality bonus:

| Category | Max Points | What It Measures |
|----------|------------|------------------|
| **Education** | 25 | Qualification level, subject match, university prestige |
| **Work Experience** | 30 | Years of experience, seniority, sector relevance |
| **Skills** | 20 | Required skills match, extra skills, driving license |
| **Languages** | 10 | Language proficiency and business value |
| **Soft Skills** | 10 | Communication, leadership, teamwork, etc. |
| **Additional** | 5 | Publications, awards, projects, conferences |
| **Personality Match** | +5 | Bonus if MBTI type matches sector preferences |

### Skill Gap Analysis

When viewing a candidate's score breakdown, you'll see:
- ✓ **Matched Skills**: Skills the candidate already has
- ✗ **Missing Required**: Essential skills to develop for this role
- ○ **Could Learn**: Optional advanced skills for career growth

## CV File Format

CVs must follow the structured format in `templates/cv_template.txt`:

```
Curriculum Vitae
       
First-Name : [Name]
Last-Name : [Name]
Address :
    Street Name : [Street]
    House Number : [Number]
    City : [City]
    Country : [Country]
...
```

**Supported Date Formats**:
- DD.MM.YYYY (European, e.g., 01.06.2020)
- MM/DD/YYYY (US, e.g., 06/01/2020)
- YYYY-MM-DD (ISO, e.g., 2020-06-01)
- Month YYYY (e.g., June 2020)

**Date Ranges**: `DD.MM.YYYY - DD.MM.YYYY` or `DD.MM.YYYY - current`

See `samples/` folder for complete examples.

## Job Sectors

The application supports 30+ job sectors including:

| Category | Sectors |
|----------|---------|
| **Science** | Biological/Chemical/Pharmaceutical, Biomedical/Medtech, Physics/Mathematics |
| **Technology** | Computers/ICT, Engineering/Manufacturing |
| **Healthcare** | Healthcare, Psychology/Social Care |
| **Creative** | Art/Craft/Design, Media/Film, Music/Performing Arts |
| **Business** | Banking/Finance, Marketing/PR, Business Management |
| **Other** | Law, Education, Construction, Tourism, Transport |

## Personality Analysis

### Myers-Briggs (MBTI)

Uses 16 personality types with percentage breakdown:

| Type | Name | Type | Name |
|------|------|------|------|
| INTJ | Architect | ENTJ | Commander |
| INTP | Logician | ENTP | Debater |
| INFJ | Advocate | ENFJ | Protagonist |
| INFP | Mediator | ENFP | Campaigner |
| ISTJ | Logistician | ESTJ | Executive |
| ISFJ | Defender | ESFJ | Consul |
| ISTP | Virtuoso | ESTP | Entrepreneur |
| ISFP | Adventurer | ESFP | Entertainer |

### Big Five (OCEAN)

Also analyzes Big Five personality traits:
- **O**penness
- **C**onscientiousness
- **E**xtroversion
- **A**greeableness
- **N**euroticism

## Testing

Run the test suite:
```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=persona2hire

# Run specific test file
pytest tests/test_parser.py
```

The test suite includes **114 tests** covering:
- CV parsing and validation
- CV file writing
- Job matching algorithms
- Candidate filtering
- Personality analysis (MBTI and Big Five)
- Date format parsing

## Contributing

Contributions are welcome! Feel free to:
- Add more job sectors with keywords
- Improve personality analysis algorithms
- Enhance the GUI
- Add new features
- Fix bugs

## License

This project is open source.

## Author

[darius024](https://github.com/darius024)
