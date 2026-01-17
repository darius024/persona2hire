"""CV file parsing functionality."""


def read_cv_file(filepath: str) -> dict:
    """
    Read and parse a CV from a structured text file.
    
    Args:
        filepath: Path to the CV text file
        
    Returns:
        Dictionary containing all CV data fields
    """
    with open(filepath, "rt") as file:
        text = file.readlines()
    
    cv_data = {}
    
    def read_field(line_index: int, field_name: str):
        """Extract value from a line after the colon."""
        if line_index < len(text):
            parts = text[line_index].split(':')
            if len(parts) > 1:
                cv_data[field_name] = parts[1].strip()
            else:
                cv_data[field_name] = ""
        else:
            cv_data[field_name] = ""
    
    # Name
    read_field(2, "FirstName")
    read_field(3, "LastName")
    
    # Address
    read_field(5, "StreetName")
    read_field(6, "HouseNumber")
    read_field(7, "City")
    read_field(8, "Country")
    
    # Contact
    read_field(9, "TelephoneNumber")
    read_field(10, "EmailAddress")
    
    # Info
    read_field(12, "Sex")
    read_field(13, "DateOfBirth")
    read_field(14, "Nationality")
    
    # Work Experience
    read_field(17, "Workplace1")
    read_field(18, "Dates1")
    read_field(19, "Occupation1")
    read_field(20, "MainActivities1")
    read_field(21, "Workplace2")
    read_field(22, "Dates2")
    read_field(23, "Occupation2")
    read_field(24, "MainActivities2")
    read_field(25, "Workplace3")
    read_field(26, "Dates3")
    read_field(27, "Occupation3")
    read_field(28, "MainActivities3")
    
    # Education and Training
    read_field(31, "HighSchool")
    read_field(32, "College/University")
    read_field(33, "SubjectsStudied")
    read_field(34, "YearsStudied")
    read_field(35, "QualificationsAwarded")
    read_field(36, "Master1")
    read_field(37, "Master2")
    
    # Personal Skills
    read_field(40, "CommunicationSkills")
    read_field(41, "OrganizationalManagerialSkills")
    read_field(42, "JobRelatedSkills")
    read_field(43, "ComputerSkills")
    read_field(44, "OtherSkills")
    read_field(45, "DrivingLicense")
    
    # Languages
    read_field(48, "MotherLanguage")
    read_field(50, "ModernLanguage1")
    read_field(51, "Level1")
    read_field(52, "ModernLanguage2")
    read_field(53, "Level2")
    
    # Additional Information
    read_field(56, "Publications")
    read_field(57, "Presentations")
    read_field(58, "Projects")
    read_field(59, "Conferences")
    read_field(60, "HonoursAndAwards")
    read_field(61, "Memberships")
    
    # Short Description
    read_field(63, "ShortDescription")
    
    # Hobbies
    read_field(65, "Hobbies")
    
    # Initialize personality type fields
    cv_data["PersonalityTypeMB"] = ""
    cv_data["PersonalityTypeBF"] = ""
    cv_data["Score"] = 0
    
    return cv_data
