"""
CV file parsing functionality.

This module handles reading and parsing structured CV text files into Python
dictionaries that can be processed by the analysis modules.

CV File Format
==============
CVs must follow the template structure in templates/cv_template.txt with
colon-separated key-value pairs:

    First-Name : John
    Last-Name : Doe
    City : London
    
    Work Experience :
        Workplace 1 : Company Ltd
            Dates : 01.01.2020 - current
            Occupation : Software Developer
            Main activities : Python, APIs, testing

Parsing Approach
================
The parser uses a **label-based approach** rather than line-position parsing:

1. Each line is scanned for known field labels (case-insensitive)
2. If a label is found, the value after the colon is extracted
3. For nested fields (work experience), context is tracked to associate
   sub-fields (Dates, Occupation) with the correct Workplace number

This makes the parser tolerant of:
- Extra blank lines
- Varied whitespace around colons ("Key:" vs "Key :" vs "Key  :")
- Reordered sections

Supported Date Formats
======================
Date fields (DateOfBirth, Dates1/2/3) accept multiple formats:
- DD.MM.YYYY (European): 01.06.2020
- MM/DD/YYYY (US): 06/01/2020
- YYYY-MM-DD (ISO): 2020-06-01
- Month YYYY: June 2020
- YYYY: 2020 (year only, assumes Jan 1)

Date ranges use hyphen: "01.01.2020 - 31.12.2023" or "01.01.2020 - current"

Encoding Handling
=================
The parser attempts UTF-8 first, falling back to Latin-1 for older files.

Known Limitations
=================
1. Requires specific template structure - free-form CVs not supported
2. Field labels must be in English
3. Maximum 3 work experience entries
4. No support for PDFs, Word docs, or other formats
5. Nested structures beyond 2 levels not supported

Usage
=====
    from persona2hire.cv.parser import read_cv_file, validate_cv_data
    
    # Parse a CV file
    cv_data = read_cv_file("path/to/cv.txt")
    
    # Validate required fields
    is_valid, errors = validate_cv_data(cv_data)
    
    # Get summary
    summary = get_cv_summary(cv_data)
"""

import re
from typing import Optional


# Field mappings: (label in file, key in dict)
FIELD_MAPPINGS = [
    ("First-Name", "FirstName"),
    ("Last-Name", "LastName"),
    ("Street Name", "StreetName"),
    ("House Number", "HouseNumber"),
    ("City", "City"),
    ("Country", "Country"),
    ("Telephone Number", "TelephoneNumber"),
    ("E-mail Address", "EmailAddress"),
    ("Sex", "Sex"),
    ("Date of Birth", "DateOfBirth"),
    ("Nationality", "Nationality"),
    ("Workplace 1", "Workplace1"),
    ("Workplace 2", "Workplace2"),
    ("Workplace 3", "Workplace3"),
    ("High school", "HighSchool"),
    ("College/University", "College/University"),
    ("Subjects studied", "SubjectsStudied"),
    ("Years studied", "YearsStudied"),
    ("Qualifications awarded", "QualificationsAwarded"),
    ("Master 1", "Master1"),
    ("Master 2", "Master2"),
    ("Communication skills", "CommunicationSkills"),
    ("Organizational / managerial skills", "OrganizationalManagerialSkills"),
    ("Job-related skills", "JobRelatedSkills"),
    ("Computer skills", "ComputerSkills"),
    ("Other skills", "OtherSkills"),
    ("Driving license", "DrivingLicense"),
    ("Mother Language", "MotherLanguage"),
    ("Modern Language 1", "ModernLanguage1"),
    ("Level1", "Level1"),
    ("Modern Language 2", "ModernLanguage2"),
    ("Level2", "Level2"),
    ("Publications", "Publications"),
    ("Presentations", "Presentations"),
    ("Projects", "Projects"),
    ("Conferences", "Conferences"),
    ("Honours and awards", "HonoursAndAwards"),
    ("Memberships", "Memberships"),
    ("Short Description", "ShortDescription"),
    ("Hobbies", "Hobbies"),
]

# Work experience fields are parsed specially (nested under workplace)
WORK_FIELDS = [
    ("Dates", "Dates"),
    ("Occupation", "Occupation"),
    ("Main activities", "MainActivities"),
]

# All valid CV field keys
CV_FIELDS = [
    "FirstName",
    "LastName",
    "StreetName",
    "HouseNumber",
    "City",
    "Country",
    "TelephoneNumber",
    "EmailAddress",
    "Sex",
    "DateOfBirth",
    "Nationality",
    "Workplace1",
    "Dates1",
    "Occupation1",
    "MainActivities1",
    "Workplace2",
    "Dates2",
    "Occupation2",
    "MainActivities2",
    "Workplace3",
    "Dates3",
    "Occupation3",
    "MainActivities3",
    "HighSchool",
    "College/University",
    "SubjectsStudied",
    "YearsStudied",
    "QualificationsAwarded",
    "Master1",
    "Master2",
    "CommunicationSkills",
    "OrganizationalManagerialSkills",
    "JobRelatedSkills",
    "ComputerSkills",
    "OtherSkills",
    "DrivingLicense",
    "MotherLanguage",
    "ModernLanguage1",
    "Level1",
    "ModernLanguage2",
    "Level2",
    "Publications",
    "Presentations",
    "Projects",
    "Conferences",
    "HonoursAndAwards",
    "Memberships",
    "ShortDescription",
    "Hobbies",
    "PersonalityTypeMB",
    "PersonalityTypeBF",
    "Score",
]


def read_cv_file(filepath: str) -> dict:
    """
    Read and parse a CV from a structured text file.

    This parser is robust against formatting variations by searching for
    field labels rather than relying on fixed line positions.

    Args:
        filepath: Path to the CV text file

    Returns:
        Dictionary containing all CV data fields

    Raises:
        FileNotFoundError: If the file doesn't exist
        UnicodeDecodeError: If the file encoding is unsupported
    """
    try:
        with open(filepath, "rt", encoding="utf-8") as file:
            content = file.read()
    except UnicodeDecodeError:
        # Fallback to latin-1 for older files
        with open(filepath, "rt", encoding="latin-1") as file:
            content = file.read()

    lines = content.split("\n")
    cv_data = _initialize_empty_cv()

    # Track current workplace for associating dates/occupation/activities
    current_workplace = 0

    for i, line in enumerate(lines):
        # Skip empty lines
        if not line.strip():
            continue

        # Check for workplace markers
        for wp_num in [1, 2, 3]:
            if f"Workplace {wp_num}" in line:
                current_workplace = wp_num
                value = _extract_value(line)
                if value:
                    cv_data[f"Workplace{wp_num}"] = value
                break
        else:
            # Check for work experience subfields
            if current_workplace > 0:
                for label, key_base in WORK_FIELDS:
                    if _line_contains_label(line, label):
                        value = _extract_value(line)
                        if value:
                            cv_data[f"{key_base}{current_workplace}"] = value
                        break

            # Check for regular field mappings
            for label, key in FIELD_MAPPINGS:
                if _line_contains_label(line, label):
                    value = _extract_value(line)
                    if value:
                        cv_data[key] = value
                    break

    return cv_data


def _initialize_empty_cv() -> dict:
    """Create an empty CV dictionary with all fields initialized."""
    cv_data = {field: "" for field in CV_FIELDS}
    cv_data["PersonalityTypeMB"] = ""
    cv_data["PersonalityTypeBF"] = ""
    cv_data["Score"] = 0
    return cv_data


def _line_contains_label(line: str, label: str) -> bool:
    """
    Check if a line contains a field label.

    Handles variations like:
    - "First-Name :" vs "First-Name:" vs "First-Name  :"
    """
    # Create a pattern that matches the label followed by optional whitespace and colon
    pattern = re.escape(label) + r"\s*:"
    return bool(re.search(pattern, line, re.IGNORECASE))


def _extract_value(line: str) -> str:
    """
    Extract the value after the colon in a line.

    Handles multiple colons (e.g., URLs, times) by only splitting on the first one.
    """
    if ":" not in line:
        return ""

    # Split on first colon only
    parts = line.split(":", 1)
    if len(parts) > 1:
        return parts[1].strip()
    return ""


def validate_cv_data(cv_data: dict) -> tuple[bool, list[str]]:
    """
    Validate CV data for required fields and data integrity.

    Args:
        cv_data: Dictionary containing CV data

    Returns:
        Tuple of (is_valid, list of error messages)
    """
    errors = []

    # Required fields
    required_fields = ["FirstName", "LastName"]
    for field in required_fields:
        if not cv_data.get(field, "").strip():
            errors.append(f"Missing required field: {field}")

    # Validate email format if provided
    email = cv_data.get("EmailAddress", "")
    if email and not _is_valid_email(email):
        errors.append(f"Invalid email format: {email}")

    # Validate years studied is numeric if provided
    years = cv_data.get("YearsStudied", "")
    if years and not years.isdigit():
        # Try to extract number
        try:
            int(years)
        except ValueError:
            errors.append(f"Years studied should be a number: {years}")

    # Validate date format for DateOfBirth if provided
    dob = cv_data.get("DateOfBirth", "")
    if dob and not _is_valid_date_format(dob):
        errors.append(f"Date of birth should be in DD.MM.YYYY format: {dob}")

    return len(errors) == 0, errors


def _is_valid_email(email: str) -> bool:
    """Check if email has a valid format."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def _is_valid_date_format(date_str: str) -> bool:
    """Check if date matches DD.MM.YYYY format."""
    pattern = r"^\d{1,2}\.\d{1,2}\.\d{4}$"
    return bool(re.match(pattern, date_str))


def get_cv_summary(cv_data: dict) -> str:
    """
    Generate a brief summary of CV data.

    Args:
        cv_data: Dictionary containing CV data

    Returns:
        Summary string
    """
    first_name = cv_data.get("FirstName", "Unknown")
    last_name = cv_data.get("LastName", "")

    # Count work experiences
    work_count = sum(1 for i in [1, 2, 3] if cv_data.get(f"Workplace{i}"))

    # Get education
    education = cv_data.get("QualificationsAwarded", "") or cv_data.get(
        "HighSchool", ""
    )

    # Count languages
    lang_count = 1  # Mother language
    if cv_data.get("ModernLanguage1"):
        lang_count += 1
    if cv_data.get("ModernLanguage2"):
        lang_count += 1

    return (
        f"{first_name} {last_name} - {work_count} work experience(s), "
        f"{education}, {lang_count} language(s)"
    )
