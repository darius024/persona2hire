"""Synthetic training data generation for ML model."""

import random
import json
import os
from datetime import date, timedelta
from typing import Optional


# Sample data pools for generating realistic CVs
FIRST_NAMES = [
    "James", "Emma", "Michael", "Sophia", "William", "Olivia", "Alexander", "Isabella",
    "Benjamin", "Mia", "Lucas", "Charlotte", "Henry", "Amelia", "Sebastian", "Harper",
    "Daniel", "Evelyn", "Matthew", "Abigail", "David", "Emily", "Joseph", "Elizabeth",
    "Samuel", "Sofia", "John", "Avery", "Andrew", "Ella", "Thomas", "Scarlett",
    "Chen", "Wei", "Yuki", "Hiroshi", "Priya", "Raj", "Fatima", "Ahmed",
    "Maria", "Carlos", "Anna", "Erik", "Ingrid", "Lars", "Olga", "Ivan",
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Wilson", "Anderson", "Thomas",
    "Taylor", "Moore", "Jackson", "Martin", "Lee", "Thompson", "White", "Harris",
    "Clark", "Lewis", "Robinson", "Walker", "Hall", "Young", "King", "Wright",
    "Chen", "Wang", "Kim", "Patel", "Singh", "Müller", "Schmidt", "Schneider",
    "Fischer", "Weber", "Meyer", "Rossi", "Russo", "Ferrari", "Romano",
]

CITIES = [
    "New York", "London", "Berlin", "Paris", "Tokyo", "Sydney", "Toronto", "Amsterdam",
    "Munich", "Barcelona", "Singapore", "Dubai", "San Francisco", "Chicago", "Boston",
    "Seattle", "Austin", "Denver", "Atlanta", "Miami", "Vancouver", "Melbourne",
    "Stockholm", "Oslo", "Copenhagen", "Helsinki", "Vienna", "Zurich", "Dublin",
]

COUNTRIES = [
    "USA", "UK", "Germany", "France", "Japan", "Australia", "Canada", "Netherlands",
    "Spain", "Singapore", "UAE", "Switzerland", "Sweden", "Norway", "Denmark",
    "Finland", "Austria", "Ireland", "Italy", "Belgium", "Portugal",
]

NATIONALITIES = [
    "American", "British", "German", "French", "Japanese", "Australian", "Canadian",
    "Dutch", "Spanish", "Singaporean", "Swiss", "Swedish", "Norwegian", "Danish",
    "Finnish", "Austrian", "Irish", "Italian", "Belgian", "Portuguese", "Indian",
    "Chinese", "Korean", "Brazilian", "Mexican", "Polish", "Russian",
]

UNIVERSITIES = [
    ("MIT", 3), ("Stanford University", 3), ("Harvard University", 3),
    ("University of Cambridge", 3), ("University of Oxford", 3),
    ("ETH Zurich", 3), ("CalTech", 3), ("Princeton University", 3),
    ("Imperial College London", 2), ("University of Chicago", 2),
    ("University of Pennsylvania", 2), ("Yale University", 2),
    ("Columbia University", 2), ("Duke University", 2), ("NYU", 2),
    ("UCLA", 2), ("University of Toronto", 2), ("University of Sydney", 2),
    ("Technical University of Munich", 2), ("University of Amsterdam", 2),
    ("State University", 1), ("City College", 1), ("Regional University", 1),
    ("Community College", 1), ("Technical Institute", 1),
]

LANGUAGES = ["English", "German", "French", "Spanish", "Mandarin", "Japanese", "Portuguese", "Russian", "Arabic", "Italian"]
LANGUAGE_LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2", "Native", "Fluent"]

MBTI_TYPES = [
    "INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP",
]

# Sector-specific data for generating relevant CVs
SECTOR_PROFILES = {
    "Computers_ICT": {
        "subjects": ["Computer Science", "Software Engineering", "Information Technology", "Data Science", "Cybersecurity"],
        "qualifications": ["BSc Computer Science", "MSc Software Engineering", "PhD Computer Science", "BSc Information Systems"],
        "companies": ["Google", "Microsoft", "Amazon", "Meta", "Apple", "IBM", "Oracle", "SAP", "Salesforce", "TechCorp", "StartupXYZ", "DataSystems Inc"],
        "roles": ["Software Engineer", "Data Scientist", "DevOps Engineer", "System Administrator", "Full Stack Developer", "Backend Developer", "Frontend Developer", "Machine Learning Engineer"],
        "skills": ["Python", "Java", "JavaScript", "SQL", "AWS", "Docker", "Kubernetes", "Git", "Linux", "React", "Node.js", "TensorFlow", "Machine Learning", "Cloud Computing"],
        "activities": ["Developed web applications", "Built scalable APIs", "Implemented CI/CD pipelines", "Managed cloud infrastructure", "Led development team"],
        "personality": ["INTJ", "INTP", "ENTJ", "ISTJ"],
    },
    "Biological_Chemical_Pharmaceutical_Science": {
        "subjects": ["Biology", "Chemistry", "Biochemistry", "Pharmacology", "Molecular Biology", "Biotechnology"],
        "qualifications": ["BSc Biology", "MSc Biochemistry", "PhD Pharmacology", "BSc Chemistry"],
        "companies": ["Pfizer", "Roche", "Novartis", "Johnson & Johnson", "Merck", "AstraZeneca", "BioLab", "PharmaCorp", "Research Institute"],
        "roles": ["Research Scientist", "Lab Technician", "Quality Analyst", "R&D Manager", "Clinical Research Associate", "Regulatory Affairs Specialist"],
        "skills": ["PCR", "HPLC", "Mass Spectrometry", "Cell Culture", "Statistical Analysis", "GMP", "Laboratory Safety", "Research Methods"],
        "activities": ["Conducted research experiments", "Analyzed data using statistical methods", "Published research papers", "Managed laboratory operations"],
        "personality": ["INTJ", "ISTJ", "INTP", "INFJ"],
    },
    "Banking_Finance_Insurance": {
        "subjects": ["Finance", "Economics", "Accounting", "Business Administration", "Mathematics"],
        "qualifications": ["BSc Finance", "MBA", "MSc Economics", "CFA", "BSc Accounting"],
        "companies": ["Goldman Sachs", "JP Morgan", "Morgan Stanley", "Deutsche Bank", "HSBC", "Barclays", "Credit Suisse", "BlackRock", "Fidelity"],
        "roles": ["Financial Analyst", "Investment Banker", "Risk Manager", "Portfolio Manager", "Compliance Officer", "Trader", "Accountant"],
        "skills": ["Financial Modeling", "Excel", "Bloomberg", "Risk Analysis", "Valuation", "SQL", "Python", "VBA", "Financial Reporting"],
        "activities": ["Analyzed financial statements", "Managed investment portfolios", "Conducted risk assessments", "Prepared financial reports"],
        "personality": ["ENTJ", "ESTJ", "INTJ", "ISTJ"],
    },
    "Healthcare": {
        "subjects": ["Medicine", "Nursing", "Public Health", "Healthcare Administration", "Biomedical Science"],
        "qualifications": ["MD", "BSN", "MSc Public Health", "PhD Medicine", "RN License"],
        "companies": ["Mayo Clinic", "Johns Hopkins Hospital", "Cleveland Clinic", "Kaiser Permanente", "City Hospital", "Regional Medical Center"],
        "roles": ["Doctor", "Nurse", "Healthcare Administrator", "Medical Researcher", "Clinical Specialist", "Public Health Officer"],
        "skills": ["Patient Care", "Medical Diagnosis", "Clinical Research", "Healthcare Management", "EMR Systems", "Medical Documentation"],
        "activities": ["Provided patient care", "Conducted clinical research", "Managed healthcare operations", "Implemented health policies"],
        "personality": ["ISFJ", "INFJ", "ESFJ", "ENFJ"],
    },
    "Marketing_PR_Advertising": {
        "subjects": ["Marketing", "Communications", "Business Administration", "Public Relations", "Digital Marketing"],
        "qualifications": ["BSc Marketing", "MBA", "MSc Communications", "BA Public Relations"],
        "companies": ["WPP", "Omnicom", "Publicis", "Dentsu", "Creative Agency", "Digital Marketing Inc", "BrandCorp"],
        "roles": ["Marketing Manager", "Brand Strategist", "Social Media Manager", "PR Specialist", "Content Manager", "Digital Marketer"],
        "skills": ["SEO", "Social Media", "Content Marketing", "Google Analytics", "Photoshop", "CRM", "Market Research", "Copywriting"],
        "activities": ["Developed marketing campaigns", "Managed social media presence", "Conducted market research", "Created brand strategies"],
        "personality": ["ENFP", "ENTP", "ENFJ", "ESFP"],
    },
    "Education_Training": {
        "subjects": ["Education", "Pedagogy", "Psychology", "Subject Specialization", "Curriculum Development"],
        "qualifications": ["BA Education", "MSc Pedagogy", "PhD Education", "Teaching Certificate"],
        "companies": ["Public School", "Private Academy", "University", "Training Institute", "Education Consultancy"],
        "roles": ["Teacher", "Professor", "Curriculum Developer", "Education Consultant", "Training Manager", "Academic Coordinator"],
        "skills": ["Curriculum Design", "Classroom Management", "Educational Technology", "Assessment", "Mentoring", "Public Speaking"],
        "activities": ["Developed curriculum", "Taught students", "Conducted educational research", "Mentored junior teachers"],
        "personality": ["ENFJ", "INFJ", "ESFJ", "ISFJ"],
    },
    "Engineering_Manufacturing_Energy": {
        "subjects": ["Engineering", "Mechanical Engineering", "Electrical Engineering", "Industrial Engineering", "Energy Systems"],
        "qualifications": ["BSc Engineering", "MSc Mechanical Engineering", "PhD Engineering", "Professional Engineer License"],
        "companies": ["Siemens", "GE", "Bosch", "ABB", "Caterpillar", "Tesla", "Manufacturing Corp", "Energy Solutions"],
        "roles": ["Mechanical Engineer", "Electrical Engineer", "Project Engineer", "Manufacturing Manager", "Quality Engineer", "Energy Analyst"],
        "skills": ["CAD", "SolidWorks", "AutoCAD", "Project Management", "Lean Manufacturing", "Six Sigma", "Technical Documentation"],
        "activities": ["Designed mechanical systems", "Managed manufacturing processes", "Conducted quality testing", "Led engineering projects"],
        "personality": ["ISTJ", "INTJ", "ESTJ", "ENTJ"],
    },
    "Law_LegalServices": {
        "subjects": ["Law", "Legal Studies", "International Law", "Corporate Law", "Criminal Justice"],
        "qualifications": ["LLB", "JD", "LLM", "Bar Admission"],
        "companies": ["Law Firm", "Corporate Legal Department", "Government Agency", "Non-Profit Legal Aid", "International Court"],
        "roles": ["Lawyer", "Legal Counsel", "Paralegal", "Legal Researcher", "Judge", "Compliance Officer"],
        "skills": ["Legal Research", "Contract Drafting", "Litigation", "Negotiation", "Legal Writing", "Case Management"],
        "activities": ["Drafted legal documents", "Represented clients in court", "Conducted legal research", "Negotiated settlements"],
        "personality": ["INTJ", "ENTJ", "ISTJ", "ESTJ"],
    },
}

# Default sectors for other job types
DEFAULT_SECTOR_PROFILE = {
    "subjects": ["Business", "Management", "General Studies"],
    "qualifications": ["Bachelor's Degree", "Master's Degree", "Diploma"],
    "companies": ["Corporation", "Company Inc", "Business Ltd", "Organization"],
    "roles": ["Manager", "Specialist", "Coordinator", "Analyst", "Officer"],
    "skills": ["Communication", "Problem Solving", "Team Work", "Microsoft Office", "Time Management"],
    "activities": ["Managed projects", "Coordinated teams", "Analyzed data", "Prepared reports"],
    "personality": MBTI_TYPES,
}


def generate_synthetic_cv(
    target_sector: str = "",
    expected_score: Optional[float] = None,
    seed: Optional[int] = None
) -> dict:
    """
    Generate a synthetic CV with realistic data.

    Args:
        target_sector: Target job sector (affects content generation)
        expected_score: Expected score for this CV (0-100), affects quality
        seed: Random seed for reproducibility

    Returns:
        Dictionary containing synthetic CV data
    """
    if seed is not None:
        random.seed(seed)

    # Get sector profile
    profile = SECTOR_PROFILES.get(target_sector, DEFAULT_SECTOR_PROFILE)

    # Determine quality level based on expected score
    if expected_score is None:
        quality = random.choice(["low", "medium", "high"])
    elif expected_score >= 70:
        quality = "high"
    elif expected_score >= 40:
        quality = "medium"
    else:
        quality = "low"

    cv = {}

    # Personal information
    cv["FirstName"] = random.choice(FIRST_NAMES)
    cv["LastName"] = random.choice(LAST_NAMES)
    cv["StreetName"] = f"{random.randint(1, 999)} {random.choice(['Main', 'Oak', 'Park', 'Lake', 'Hill'])} Street"
    cv["HouseNumber"] = str(random.randint(1, 200))
    cv["City"] = random.choice(CITIES)
    cv["Country"] = random.choice(COUNTRIES)
    cv["TelephoneNumber"] = f"+{random.randint(1, 99)}-{random.randint(100, 999)}-{random.randint(1000000, 9999999)}"
    cv["EmailAddress"] = f"{cv['FirstName'].lower()}.{cv['LastName'].lower()}@email.com"
    cv["Sex"] = random.choice(["M", "F"])

    # Age based on quality (higher quality = more experience usually)
    if quality == "high":
        age = random.randint(30, 50)
    elif quality == "medium":
        age = random.randint(25, 40)
    else:
        age = random.randint(22, 35)

    birth_year = date.today().year - age
    cv["DateOfBirth"] = f"{random.randint(1, 28)}.{random.randint(1, 12)}.{birth_year}"
    cv["Nationality"] = random.choice(NATIONALITIES)

    # Work experience (more and better for higher quality)
    num_jobs = {"high": 3, "medium": 2, "low": 1}[quality]
    current_year = date.today().year

    for i in range(1, 4):
        if i <= num_jobs:
            company = random.choice(profile["companies"])
            role = random.choice(profile["roles"])

            # Calculate dates
            if i == 1:
                # Most recent job
                start_year = current_year - random.randint(1, 3)
                end_date = "current" if random.random() > 0.3 else f"01.12.{current_year}"
            else:
                start_year = current_year - random.randint(3 + (i * 2), 5 + (i * 3))
                end_year = start_year + random.randint(1, 3)
                end_date = f"01.12.{end_year}"

            start_date = f"01.01.{start_year}"

            # Seniority based on quality
            if quality == "high" and i == 1:
                role = "Senior " + role if "Senior" not in role else role

            cv[f"Workplace{i}"] = company
            cv[f"Dates{i}"] = f"{start_date} - {end_date}"
            cv[f"Occupation{i}"] = role
            cv[f"MainActivities{i}"] = ", ".join(random.sample(profile["activities"], min(2, len(profile["activities"]))))
        else:
            cv[f"Workplace{i}"] = ""
            cv[f"Dates{i}"] = ""
            cv[f"Occupation{i}"] = ""
            cv[f"MainActivities{i}"] = ""

    # Education
    cv["HighSchool"] = f"{random.choice(CITIES)} High School"

    # University prestige based on quality
    if quality == "high":
        uni_options = [u for u in UNIVERSITIES if u[1] >= 2]
    elif quality == "medium":
        uni_options = [u for u in UNIVERSITIES if u[1] >= 1]
    else:
        uni_options = UNIVERSITIES

    university, _ = random.choice(uni_options)
    cv["College/University"] = university

    cv["SubjectsStudied"] = ", ".join(random.sample(profile["subjects"], min(2, len(profile["subjects"]))))
    cv["YearsStudied"] = str(random.choice([3, 4, 5]))
    cv["QualificationsAwarded"] = random.choice(profile["qualifications"])

    # Masters based on quality
    if quality == "high" and random.random() > 0.3:
        cv["Master1"] = f"MSc {random.choice(profile['subjects'])}"
        cv["Master2"] = "" if random.random() > 0.2 else f"MBA"
    elif quality == "medium" and random.random() > 0.6:
        cv["Master1"] = f"MSc {random.choice(profile['subjects'])}"
        cv["Master2"] = ""
    else:
        cv["Master1"] = ""
        cv["Master2"] = ""

    # Skills
    num_skills = {"high": 6, "medium": 4, "low": 2}[quality]
    selected_skills = random.sample(profile["skills"], min(num_skills, len(profile["skills"])))
    cv["ComputerSkills"] = ", ".join(selected_skills[:4])
    cv["JobRelatedSkills"] = ", ".join(selected_skills[2:])
    cv["CommunicationSkills"] = random.choice(["Team collaboration", "Presentation skills", "Written communication", "Client relations"])
    cv["OrganizationalManagerialSkills"] = random.choice(["Project management", "Team leadership", "Agile methodologies", "Strategic planning"])
    cv["OtherSkills"] = random.choice(["Problem solving", "Critical thinking", "Analytical skills", "Creativity"])
    cv["DrivingLicense"] = random.choice(["B", "B", "B", "A, B", ""])

    # Languages
    cv["MotherLanguage"] = random.choice(LANGUAGES[:5])
    cv["ModernLanguage1"] = "English" if cv["MotherLanguage"] != "English" else "German"
    cv["Level1"] = random.choice(LANGUAGE_LEVELS[3:]) if quality == "high" else random.choice(LANGUAGE_LEVELS[1:5])

    if quality in ["high", "medium"] and random.random() > 0.4:
        cv["ModernLanguage2"] = random.choice([l for l in LANGUAGES if l != cv["MotherLanguage"] and l != cv["ModernLanguage1"]])
        cv["Level2"] = random.choice(LANGUAGE_LEVELS[:5])
    else:
        cv["ModernLanguage2"] = ""
        cv["Level2"] = ""

    # Additional information (more for higher quality)
    if quality == "high":
        cv["Publications"] = f"Paper on {random.choice(profile['subjects'])}, 2022"
        cv["HonoursAndAwards"] = random.choice(["Best Graduate", "Dean's List", "Excellence Award", "Industry Recognition"])
        cv["Projects"] = f"Led {random.choice(['innovation', 'research', 'development'])} project"
    elif quality == "medium":
        cv["Publications"] = "" if random.random() > 0.3 else f"Article on {random.choice(profile['subjects'])}"
        cv["HonoursAndAwards"] = "" if random.random() > 0.5 else "Academic Achievement"
        cv["Projects"] = "Personal projects, hackathon participation"
    else:
        cv["Publications"] = ""
        cv["HonoursAndAwards"] = ""
        cv["Projects"] = ""

    cv["Presentations"] = "" if quality == "low" else random.choice(["", "Conference presentation", "Workshop"])
    cv["Conferences"] = "" if quality == "low" else random.choice(["", "Industry conference 2023", ""])
    cv["Memberships"] = "" if quality == "low" else random.choice(["", "Professional Association", ""])

    # Personality
    if target_sector in SECTOR_PROFILES and random.random() > 0.3:
        cv["ShortDescription"] = _generate_description(profile.get("personality", MBTI_TYPES)[0])
        cv["PersonalityTypeMB"] = random.choice(profile.get("personality", MBTI_TYPES))
    else:
        cv["PersonalityTypeMB"] = random.choice(MBTI_TYPES)
        cv["ShortDescription"] = _generate_description(cv["PersonalityTypeMB"])

    cv["Hobbies"] = ", ".join(random.sample([
        "reading", "sports", "travel", "music", "cooking", "photography",
        "gaming", "hiking", "programming", "art", "volunteering", "languages"
    ], 3))

    cv["PersonalityTypeBF"] = ""
    cv["Score"] = 0

    return cv


def _generate_description(personality: str) -> str:
    """Generate personality description based on MBTI type."""
    traits = {
        "I": ["thoughtful", "reserved", "analytical", "focused"],
        "E": ["outgoing", "energetic", "social", "enthusiastic"],
        "S": ["practical", "detail-oriented", "reliable", "grounded"],
        "N": ["innovative", "creative", "visionary", "intuitive"],
        "T": ["logical", "objective", "analytical", "systematic"],
        "F": ["empathetic", "caring", "collaborative", "supportive"],
        "J": ["organized", "structured", "decisive", "methodical"],
        "P": ["flexible", "adaptable", "spontaneous", "open-minded"],
    }

    selected = []
    for letter in personality[:4]:
        if letter in traits:
            selected.append(random.choice(traits[letter]))

    return f"{', '.join(selected[:3])} professional with strong work ethic"


def generate_training_data(
    num_samples: int = 100,
    output_dir: Optional[str] = None,
    sectors: Optional[list[str]] = None
) -> list[dict]:
    """
    Generate a training dataset of synthetic CVs with expected scores.

    Args:
        num_samples: Number of CVs to generate
        output_dir: Directory to save generated data (optional)
        sectors: List of sectors to generate for (uses all if None)

    Returns:
        List of dictionaries with 'cv', 'sector', and 'expected_score' keys
    """
    if sectors is None:
        sectors = list(SECTOR_PROFILES.keys())

    training_data = []

    for i in range(num_samples):
        # Select sector
        sector = random.choice(sectors)

        # Generate score distribution (mix of low, medium, high)
        score_type = random.choices(
            ["low", "medium", "high"],
            weights=[0.3, 0.4, 0.3]
        )[0]

        if score_type == "high":
            expected_score = random.uniform(70, 95)
        elif score_type == "medium":
            expected_score = random.uniform(40, 70)
        else:
            expected_score = random.uniform(10, 40)

        # Generate CV
        cv = generate_synthetic_cv(
            target_sector=sector,
            expected_score=expected_score,
            seed=i * 42  # Reproducible
        )

        training_data.append({
            "cv": cv,
            "sector": sector,
            "expected_score": round(expected_score, 1),
        })

    # Save if output directory specified
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

        # Save as JSON
        json_path = os.path.join(output_dir, "training_data.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(training_data, f, indent=2)

        # Save individual CVs
        cvs_dir = os.path.join(output_dir, "cvs")
        os.makedirs(cvs_dir, exist_ok=True)

        for i, item in enumerate(training_data):
            cv_path = os.path.join(cvs_dir, f"cv_{i:04d}_{item['sector']}.json")
            with open(cv_path, "w", encoding="utf-8") as f:
                json.dump(item, f, indent=2)

    return training_data
