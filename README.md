# Persona2Hire

A desktop application for analyzing CVs (Curriculum Vitae) and matching candidates to job sectors based on their qualifications, skills, and MBTI personality types.

## Features

- **CV Parsing**: Robust key-based parsing of structured CV text files
- **CV Creation**: Create new CVs through a modern form-based interface with validation
- **Job Matching**: Analyze candidates against 30+ job sectors with normalized scoring (0-100)
- **Personality Analysis**: Determine Myers-Briggs (MBTI) and Big Five personality profiles
- **Candidate Ranking**: Rank and compare candidates for specific positions
- **Score Breakdown**: View detailed scoring breakdown by category

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
├── run.py                     # Simple entry point
├── requirements.txt
├── .gitignore
└── README.md
```

## Requirements

- Python 3.10 or higher
- Tkinter (included with Python standard library)

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
3. **Analyze All** to rank all loaded candidates for the selected sector
4. **View Details** by selecting a candidate:
   - Click on a candidate row to see score breakdown
   - "Show Jobs Match" - See suitable job sectors ranked
   - "Show Personality" - See MBTI and Big Five personality analysis

### Creating a New CV

1. Click "Create New CV"
2. Fill in the form (First Name and Last Name are required)
3. Click "Create CV" to save

Created CVs are automatically saved to the `CVs/` directory.

## Scoring System

The job matching uses a normalized 0-100 scoring system:

| Category | Max Points | What It Measures |
|----------|------------|------------------|
| **Education** | 25 | Qualification level, subject match, university prestige |
| **Work Experience** | 30 | Years of experience, seniority, sector relevance |
| **Skills** | 20 | Required skills match, extra skills, driving license |
| **Languages** | 10 | Language proficiency and business value |
| **Soft Skills** | 10 | Communication, leadership, teamwork, etc. |
| **Additional** | 5 | Publications, awards, projects, conferences |

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

**Date Format**: DD.MM.YYYY (e.g., 01.06.2020)
**Date Ranges**: DD.MM.YYYY - DD.MM.YYYY or DD.MM.YYYY - current

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
