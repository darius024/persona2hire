"""CV file writing functionality."""

import os
import re
from datetime import datetime
from typing import Optional


def write_cv_file(
    person: dict, output_dir: Optional[str] = None, overwrite: bool = False
) -> str:
    """
    Write a CV to a structured text file.

    Args:
        person: Dictionary containing CV data
        output_dir: Directory to save the CV file (default: ./CVs)
        overwrite: If True, overwrite existing file; if False, append number

    Returns:
        Path to the created file

    Raises:
        ValueError: If required fields are missing
        OSError: If file cannot be written
    """
    # Validate required fields
    first_name = _sanitize_text(person.get("FirstName", ""))
    last_name = _sanitize_text(person.get("LastName", ""))

    if not first_name and not last_name:
        raise ValueError("CV must have at least a first name or last name")

    # Set up output directory
    if output_dir is None:
        output_dir = os.path.join(os.getcwd(), "CVs")

    # Create directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Generate safe filename
    file_path = _generate_unique_filepath(output_dir, first_name, last_name, overwrite)

    # Write the CV file
    _write_cv_content(file_path, person)

    return file_path


def _sanitize_filename(name: str) -> str:
    """
    Sanitize a string to be safe for use in filenames.

    Removes or replaces characters that are invalid in filenames
    across different operating systems.
    """
    if not name:
        return ""

    # Replace spaces and common problematic characters
    safe_name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "", name)
    safe_name = safe_name.replace(" ", "_")
    safe_name = safe_name.strip("._")

    # Limit length to prevent filesystem issues
    return safe_name[:50]


def _sanitize_text(text: str) -> str:
    """Sanitize text input by stripping whitespace."""
    if text is None:
        return ""
    return str(text).strip()


def _generate_unique_filepath(
    output_dir: str, first_name: str, last_name: str, overwrite: bool
) -> str:
    """
    Generate a unique filepath for the CV file.

    If overwrite is False and file exists, appends a number to make it unique.
    """
    # Create base filename
    safe_first = _sanitize_filename(first_name) or "Unknown"
    safe_last = _sanitize_filename(last_name) or "Person"
    base_name = f"{safe_first}_{safe_last}"

    file_path = os.path.join(output_dir, f"{base_name}.txt")

    if overwrite or not os.path.exists(file_path):
        return file_path

    # Find a unique filename by appending numbers
    counter = 1
    while os.path.exists(file_path):
        file_path = os.path.join(output_dir, f"{base_name}_{counter}.txt")
        counter += 1
        if counter > 1000:  # Safety limit
            raise OSError(f"Too many CV files for {base_name}")

    return file_path


def _write_cv_content(file_path: str, person: dict) -> None:
    """Write the CV content to a file in the standard format."""

    def get_field(key: str, default: str = "") -> str:
        """Safely get a field value."""
        value = person.get(key)
        if value is None:
            return default
        return str(value).strip()

    with open(file_path, "w", encoding="utf-8") as file:
        # Header
        file.write("Curriculum Vitae\n")
        file.write("       \n")

        # Personal Information
        file.write(f"First-Name : {get_field('FirstName')}\n")
        file.write(f"Last-Name : {get_field('LastName')}\n")
        file.write("Address :\n")
        file.write(f"    Street Name : {get_field('StreetName')}\n")
        file.write(f"    House Number : {get_field('HouseNumber')}\n")
        file.write(f"    City : {get_field('City')}\n")
        file.write(f"    Country : {get_field('Country')}\n")
        file.write(f"Telephone Number : {get_field('TelephoneNumber')}\n")
        file.write(f"E-mail Address : {get_field('EmailAddress')}\n")
        file.write("\n")

        file.write(f"Sex : {get_field('Sex')}\n")
        file.write(f"Date of Birth : {get_field('DateOfBirth')}\n")
        file.write(f"Nationality : {get_field('Nationality')}\n")
        file.write("\n")

        # Work Experience
        file.write("Work Experience :\n")
        for i in [1, 2, 3]:
            file.write(f"\tWorkplace {i} : {get_field(f'Workplace{i}')}\n")
            file.write(f"\t    Dates : {get_field(f'Dates{i}')}\n")
            file.write(f"\t    Occupation : {get_field(f'Occupation{i}')}\n")
            file.write(f"        Main activities : {get_field(f'MainActivities{i}')}\n")
        file.write("\n")

        # Education
        file.write("Education and Training :\n")
        file.write(f"\tHigh school : {get_field('HighSchool')}\n")
        file.write(f"\tCollege/University : {get_field('College/University')}\n")
        file.write(f"\t    Subjects studied : {get_field('SubjectsStudied')}\n")
        file.write(f"\t    Years studied : {get_field('YearsStudied')}\n")
        file.write(f"\tQualifications awarded : {get_field('QualificationsAwarded')}\n")
        file.write(f"\tMaster 1 : {get_field('Master1')}\n")
        file.write(f"\tMaster 2 : {get_field('Master2')}\n")
        file.write("\n")

        # Skills
        file.write("Personal Skills :\n")
        file.write(f"\tCommunication skills : {get_field('CommunicationSkills')}\n")
        file.write(
            f"\tOrganizational / managerial skills : {get_field('OrganizationalManagerialSkills')}\n"
        )
        file.write(f"\tJob-related skills : {get_field('JobRelatedSkills')}\n")
        file.write(f"\tComputer skills : {get_field('ComputerSkills')}\n")
        file.write(f"\tOther skills : {get_field('OtherSkills')}\n")
        file.write(f"\tDriving license : {get_field('DrivingLicense')}\n")
        file.write("\n")

        # Languages
        file.write("Languages :\n")
        file.write(f"\tMother Language : {get_field('MotherLanguage')}\n")
        file.write("\tOther Languages :\n")
        file.write(f"\t    Modern Language 1 : {get_field('ModernLanguage1')}\n")
        file.write(f"\t        Level1 : {get_field('Level1')}\n")
        file.write(f"\t    Modern Language 2 : {get_field('ModernLanguage2')}\n")
        file.write(f"\t        Level2 : {get_field('Level2')}\n")
        file.write("\n")

        # Additional Information
        file.write("Additional Information:\n")
        file.write(f"    Publications : {get_field('Publications')}\n")
        file.write(f"    Presentations : {get_field('Presentations')}\n")
        file.write(f"    Projects : {get_field('Projects')}\n")
        file.write(f"    Conferences : {get_field('Conferences')}\n")
        file.write(f"    Honours and awards : {get_field('HonoursAndAwards')}\n")
        file.write(f"    Memberships : {get_field('Memberships')}\n")
        file.write("\n")

        # Description and Hobbies
        file.write(f"Short Description : {get_field('ShortDescription')}\n")
        file.write("\n")
        file.write(f"Hobbies : {get_field('Hobbies')}\n")


def create_empty_cv() -> dict:
    """
    Create an empty CV dictionary with all fields initialized.

    Returns:
        Dictionary with all CV fields set to empty strings or default values
    """
    return {
        "FirstName": "",
        "LastName": "",
        "StreetName": "",
        "HouseNumber": "",
        "City": "",
        "Country": "",
        "TelephoneNumber": "",
        "EmailAddress": "",
        "Sex": "",
        "DateOfBirth": "",
        "Nationality": "",
        "Workplace1": "",
        "Dates1": "",
        "Occupation1": "",
        "MainActivities1": "",
        "Workplace2": "",
        "Dates2": "",
        "Occupation2": "",
        "MainActivities2": "",
        "Workplace3": "",
        "Dates3": "",
        "Occupation3": "",
        "MainActivities3": "",
        "HighSchool": "",
        "College/University": "",
        "SubjectsStudied": "",
        "YearsStudied": "",
        "QualificationsAwarded": "",
        "Master1": "",
        "Master2": "",
        "CommunicationSkills": "",
        "OrganizationalManagerialSkills": "",
        "JobRelatedSkills": "",
        "ComputerSkills": "",
        "OtherSkills": "",
        "DrivingLicense": "",
        "MotherLanguage": "",
        "ModernLanguage1": "",
        "Level1": "",
        "ModernLanguage2": "",
        "Level2": "",
        "Publications": "",
        "Presentations": "",
        "Projects": "",
        "Conferences": "",
        "HonoursAndAwards": "",
        "Memberships": "",
        "ShortDescription": "",
        "Hobbies": "",
        "PersonalityTypeMB": "",
        "PersonalityTypeBF": "",
        "Score": 0,
    }


def cv_to_string(person: dict) -> str:
    """
    Convert a CV dictionary to a formatted string.

    Useful for previewing CV content without writing to a file.

    Args:
        person: Dictionary containing CV data

    Returns:
        Formatted CV string
    """
    import io

    buffer = io.StringIO()

    # Temporarily write to string buffer
    original_write = _write_cv_content

    def get_field(key: str, default: str = "") -> str:
        value = person.get(key)
        if value is None:
            return default
        return str(value).strip()

    lines = [
        "Curriculum Vitae",
        "",
        f"Name: {get_field('FirstName')} {get_field('LastName')}",
        f"Location: {get_field('City')}, {get_field('Country')}",
        f"Email: {get_field('EmailAddress')}",
        "",
        "Work Experience:",
    ]

    for i in [1, 2, 3]:
        workplace = get_field(f"Workplace{i}")
        if workplace:
            lines.append(f"  - {workplace} ({get_field(f'Dates{i}')})")
            lines.append(f"    {get_field(f'Occupation{i}')}")

    lines.extend(
        [
            "",
            f"Education: {get_field('QualificationsAwarded')}",
            f"Skills: {get_field('ComputerSkills')}",
        ]
    )

    return "\n".join(lines)
