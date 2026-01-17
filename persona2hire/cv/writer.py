"""CV file writing functionality."""

import os


def write_cv_file(person: dict, output_dir: str = None) -> str:
    """
    Write a CV to a structured text file.
    
    Args:
        person: Dictionary containing CV data
        output_dir: Directory to save the CV file (default: ./CVs)
        
    Returns:
        Path to the created file
    """
    if output_dir is None:
        output_dir = os.path.join(os.getcwd(), "CVs")
    
    # Create directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate filename from name
    first_name = person.get("FirstName", "Unknown")
    last_name = person.get("LastName", "Person")
    file_path = os.path.join(output_dir, f"{first_name}{last_name}.txt")
    
    with open(file_path, 'w') as file:
        file.write("Curriculum Vitae \n \n")
        file.write(f"First-Name : {person.get('FirstName', '')}\n")
        file.write(f"Last-Name : {person.get('LastName', '')}\n")
        file.write("Address : \n")
        file.write(f"    Street Name : {person.get('StreetName', '')}\n")
        file.write(f"    House Number : {person.get('HouseNumber', '')}\n")
        file.write(f"    City : {person.get('City', '')}\n")
        file.write(f"    Country : {person.get('Country', '')}\n")
        file.write(f"Telephone Number : {person.get('TelephoneNumber', '')}\n")
        file.write(f"E-mail Address : {person.get('EmailAddress', '')}\n\n")
        file.write(f"Sex : {person.get('Sex', '')}\n")
        file.write(f"Date of Birth : {person.get('DateOfBirth', '')}\n")
        file.write(f"Nationality : {person.get('Nationality', '')}\n\n")
        file.write("Work Experience : \n")
        file.write(f"    Workplace 1 : {person.get('Workplace1', '')}\n")
        file.write(f"        Dates : {person.get('Dates1', '')}\n")
        file.write(f"        Occupation : {person.get('Occupation1', '')}\n")
        file.write(f"        Main activities : {person.get('MainActivities1', '')}\n")
        file.write(f"    Workplace 2 : {person.get('Workplace2', '')}\n")
        file.write(f"        Dates : {person.get('Dates2', '')}\n")
        file.write(f"        Occupation : {person.get('Occupation2', '')}\n")
        file.write(f"        Main activities : {person.get('MainActivities2', '')}\n")
        file.write(f"    Workplace 3 : {person.get('Workplace3', '')}\n")
        file.write(f"        Dates : {person.get('Dates3', '')}\n")
        file.write(f"        Occupation : {person.get('Occupation3', '')}\n")
        file.write(f"        Main activities : {person.get('MainActivities3', '')}\n\n")
        file.write("Education and Training : \n")
        file.write(f"    High school : {person.get('HighSchool', '')}\n")
        file.write(f"    College/University : {person.get('College/University', '')}\n")
        file.write(f"        Subjects studied : {person.get('SubjectsStudied', '')}\n")
        file.write(f"        Years studied : {person.get('YearsStudied', '')}\n")
        file.write(f"    Qualifications awarded : {person.get('QualificationsAwarded', '')}\n")
        file.write(f"    Master 1 : {person.get('Master1', '')}\n")
        file.write(f"    Master 2 : {person.get('Master2', '')}\n\n")
        file.write("Personal Skills : \n")
        file.write(f"    Communication skills : {person.get('CommunicationSkills', '')}\n")
        file.write(f"    Organizational / managerial skills : {person.get('OrganizationalManagerialSkills', '')}\n")
        file.write(f"    Job-related skills : {person.get('JobRelatedSkills', '')}\n")
        file.write(f"    Computer skills : {person.get('ComputerSkills', '')}\n")
        file.write(f"    Other skills : {person.get('OtherSkills', '')}\n")
        file.write(f"    Driving License : {person.get('DrivingLicense', '')}\n\n")
        file.write("Languages : \n")
        file.write(f"    Mother Language : {person.get('MotherLanguage', '')}\n")
        file.write("    Other Languages : \n")
        file.write(f"        Modern Language 1 : {person.get('ModernLanguage1', '')}\n")
        file.write(f"            Level 1 : {person.get('Level1', '')}\n")
        file.write(f"        Modern Language 2 : {person.get('ModernLanguage2', '')}\n")
        file.write(f"            Level 2 : {person.get('Level2', '')}\n\n")
        file.write("Additional Information : \n")
        file.write(f"    Publications : {person.get('Publications', '')}\n")
        file.write(f"    Presentations : {person.get('Presentations', '')}\n")
        file.write(f"    Projects : {person.get('Projects', '')}\n")
        file.write(f"    Conferences : {person.get('Conferences', '')}\n")
        file.write(f"    Honours and awards : {person.get('HonoursAndAwards', '')}\n")
        file.write(f"    Memberships : {person.get('Memberships', '')}\n\n")
        file.write(f"Short Description : {person.get('ShortDescription', '')}\n\n")
        file.write(f"Hobbies : {person.get('Hobbies', '')}\n\n")
    
    return file_path
