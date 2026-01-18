"""Shared test fixtures and configuration."""

import os
import tempfile
import pytest


@pytest.fixture
def sample_cv_data():
    """A complete sample CV data dictionary for testing."""
    return {
        "FirstName": "John",
        "LastName": "Doe",
        "StreetName": "Main Street",
        "HouseNumber": "42",
        "City": "Berlin",
        "Country": "Germany",
        "TelephoneNumber": "+49123456789",
        "EmailAddress": "john.doe@example.com",
        "Sex": "M",
        "DateOfBirth": "15.03.1990",
        "Nationality": "German",
        "Workplace1": "Tech Corp",
        "Dates1": "01.01.2018 - 31.12.2020",
        "Occupation1": "Senior Software Engineer",
        "MainActivities1": "Developed cloud applications, led team of 5 developers",
        "Workplace2": "StartupXYZ",
        "Dates2": "01.06.2015 - 31.12.2017",
        "Occupation2": "Junior Developer",
        "MainActivities2": "Built web applications, maintained databases",
        "Workplace3": "",
        "Dates3": "",
        "Occupation3": "",
        "MainActivities3": "",
        "HighSchool": "Berlin Technical High School",
        "College/University": "Technical University of Munich",
        "SubjectsStudied": "Computer Science, Software Engineering, Mathematics",
        "YearsStudied": "4",
        "QualificationsAwarded": "Bachelor of Science in Computer Science",
        "Master1": "Master of Computer Science",
        "Master2": "",
        "CommunicationSkills": "Excellent presentation skills, team collaboration",
        "OrganizationalManagerialSkills": "Project management, agile methodologies, Scrum",
        "JobRelatedSkills": "Python, Java, cloud computing, databases, machine learning",
        "ComputerSkills": "Python, JavaScript, Docker, AWS, PostgreSQL, Git",
        "OtherSkills": "Problem solving, analytical thinking",
        "DrivingLicense": "B",
        "MotherLanguage": "German",
        "ModernLanguage1": "English",
        "Level1": "C1",
        "ModernLanguage2": "French",
        "Level2": "B1",
        "Publications": "Machine Learning in Cloud Computing, IEEE 2020",
        "Presentations": "PyCon Germany 2019",
        "Projects": "Open source contributor to Django, Personal ML project",
        "Conferences": "AWS Summit 2020, Google I/O 2019",
        "HonoursAndAwards": "Best Graduate 2015, Hackathon Winner 2018",
        "Memberships": "IEEE Computer Society, Python Software Foundation",
        "ShortDescription": "Analytical, innovative, detail-oriented problem solver who enjoys teamwork and continuous learning",
        "Hobbies": "programming, chess, hiking, reading technology books",
        "PersonalityTypeMB": "",
        "PersonalityTypeBF": "",
        "Score": 0,
    }


@pytest.fixture
def minimal_cv_data():
    """Minimal valid CV data with only required fields."""
    return {
        "FirstName": "Jane",
        "LastName": "Smith",
        "EmailAddress": "",
        "DateOfBirth": "",
    }


@pytest.fixture
def empty_cv_data():
    """Empty CV data for testing validation."""
    return {
        "FirstName": "",
        "LastName": "",
    }


@pytest.fixture
def temp_dir():
    """Create a temporary directory for file operations."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def sample_cv_file(temp_dir):
    """Create a sample CV file for testing parsing."""
    content = """Curriculum Vitae

First-Name : Sarah
Last-Name : Mitchell
Street Name : Oak Avenue
House Number : 123
City : Munich
Country : Germany
Telephone Number : +49-89-1234567
E-mail Address : sarah.mitchell@email.com
Sex : F
Date of Birth : 22.05.1992
Nationality : German

Work Experience:

Workplace 1 : TechStart GmbH
Dates : 01.03.2020 - current
Occupation : Lead Developer
Main activities : Leading development team, architecture design

Workplace 2 : WebAgency
Dates : 15.06.2017 - 28.02.2020
Occupation : Web Developer
Main activities : Full-stack development, client projects

Education:

High school : Munich Technical School
College/University : Ludwig Maximilian University
Subjects studied : Computer Science, AI
Years studied : 4
Qualifications awarded : Bachelor in Computer Science
Master 1 : Master in Artificial Intelligence
Master 2 :

Skills:

Communication skills : Team leadership, presentations
Organizational / managerial skills : Agile, project management
Job-related skills : Machine learning, data analysis
Computer skills : Python, TensorFlow, React, Docker
Other skills : Critical thinking
Driving license : B

Languages:

Mother Language : German
Modern Language 1 : English
Level1 : C2
Modern Language 2 : Spanish
Level2 : A2

Additional Information:

Publications : AI for Healthcare, Nature 2021
Presentations : MLConf 2020
Projects : Open source ML framework
Conferences : NeurIPS 2021
Honours and awards : Dean's List 2016
Memberships : ACM Member

Short Description : Creative, analytical, innovative thinker who loves solving complex problems
Hobbies : machine learning, reading, yoga, travel
"""
    filepath = os.path.join(temp_dir, "test_cv.txt")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath


@pytest.fixture
def introverted_person():
    """CV data for a person with introverted traits."""
    return {
        "FirstName": "Alex",
        "LastName": "Introvert",
        "ShortDescription": "Reserved, analytical, thoughtful, independent thinker who prefers working alone",
        "Hobbies": "reading, chess, writing, programming, meditation",
        "CommunicationSkills": "Written communication",
        "ComputerSkills": "Python, research",
    }


@pytest.fixture
def extroverted_person():
    """CV data for a person with extroverted traits."""
    return {
        "FirstName": "Emma",
        "LastName": "Extrovert",
        "ShortDescription": "Outgoing, energetic, enthusiastic, loves meeting people and socializing",
        "Hobbies": "team sports, networking, parties, public speaking, dancing",
        "CommunicationSkills": "Excellent public speaking, team leadership",
        "ComputerSkills": "Marketing tools",
    }
