# CV-Personality App

A desktop application for analyzing CVs (Curriculum Vitae) and matching candidates to job sectors based on their qualifications and personality traits.

## Features

- **CV Parsing**: Load structured CV text files
- **CV Creation**: Create new CVs through a form-based interface
- **Job Matching**: Analyze candidates against 30+ job sectors
- **Personality Analysis**: Determine Myers-Briggs (MBTI) personality types
- **Candidate Ranking**: Rank candidates for specific positions

## Requirements

- Python 3.10 or higher (uses `match-case` statements)
- Tkinter (included with Python standard library)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/CV-Personality_App.git
   cd CV-Personality_App
   ```

2. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

## Usage

Run the application:
```bash
python CV.py
```

### Main Features

1. **Select Job Sector**: Choose from the dropdown menu
2. **Load CVs**: Click "Choose File" to load existing CV text files
3. **Create CV**: Click "Make CV" to create a new CV through the form
4. **Analyze**: Click "Analyze data" to rank candidates for the selected job
5. **View Details**: Select a candidate and click "Show Jobs" or "Show Personality"

## CV File Format

CVs must follow the structure defined in `CV.txt`. See `CV_ex.txt` for an example.

## Job Sectors

The application supports analysis across multiple sectors including:
- Animals & Veterinary Science
- Computers & ICT
- Engineering & Manufacturing
- Healthcare
- And many more...

## License

This project is open source.
