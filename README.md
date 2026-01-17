# Persona2Hire

A desktop application for analyzing CVs (Curriculum Vitae) and matching candidates to job sectors based on their qualifications and MBTI personality types.

## Features

- **CV Parsing**: Load structured CV text files
- **CV Creation**: Create new CVs through a form-based interface
- **Job Matching**: Analyze candidates against 30+ job sectors
- **Personality Analysis**: Determine Myers-Briggs (MBTI) personality types
- **Candidate Ranking**: Rank candidates for specific positions

## Project Structure

```
Persona2Hire/
├── persona2hire/              # Main package
│   ├── __init__.py
│   ├── main.py                # Application entry point
│   ├── data/                  # Data modules
│   │   ├── job_sectors.py     # Job sector definitions
│   │   ├── personality.py     # MBTI personality types
│   │   └── constants.py       # Functions, qualifications, languages
│   ├── analysis/              # Analysis modules
│   │   ├── job_analyzer.py    # Job matching algorithms
│   │   └── personality_analyzer.py  # Personality assessment
│   ├── cv/                    # CV file operations
│   │   ├── parser.py          # CV file parsing
│   │   └── writer.py          # CV file writing
│   └── gui/                   # GUI modules
│       ├── main_window.py     # Main application window
│       ├── cv_form.py         # CV creation form
│       ├── dialogs.py         # Filter dialogs
│       └── results.py         # Results display windows
├── templates/                 # CV templates
│   ├── cv_template.txt        # Empty CV template
│   └── cv_example.txt         # Example filled CV
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

1. **Select a Job Sector** from the dropdown menu
2. **Load CVs** by clicking "Choose File" and selecting files from `samples/`
3. **Analyze** by clicking "Analyze data" to rank candidates
4. **View Details** by selecting a candidate and clicking:
   - "Show Jobs" - See suitable job sectors
   - "Show Personality" - See MBTI personality analysis

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

## Personality Types

Uses the Myers-Briggs Type Indicator (MBTI) with 16 personality types:

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

## Contributing

Contributions are welcome! Feel free to:
- Add more job sectors with keywords
- Improve personality analysis algorithms
- Enhance the GUI
- Add new features

## License

This project is open source.

## Author

[darius024](https://github.com/darius024)
