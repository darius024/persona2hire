from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import os
# import pandas as pd
# import numpy as np
# import datetime
from datetime import date
import webbrowser


window = Tk()
window.title("CV-Personality App")
window.configure(bg='black')
window.state("zoomed")
# window.geometry("1400x800")
# window.configure(width=window.winfo_screenwidth(), height=window.winfo_screenheight())

Person = []

def ReadFile(CV):
    with open(CV, "rt") as file:
        text = file.readlines()
    char = ':'

    CVData = {}

    def Read(i: int, word: char):
        list = text[i].split(char)
        if len(list) != 1:
            CVData[word] = list[1]
        else:
            CVData[word] = ""
    # Name
    Read(2, "FirstName")
    Read(3, "LastName")

    # Address
    Read(5, "StreetName")
    Read(6, "HouseNumber")
    Read(7, "City")
    Read(8, "Country")

    # Contact
    Read(9, "TelephoneNumber")
    Read(10, "EmailAddress")

    # Info
    Read(12, "Sex")
    Read(13, "Date0fBirth")
    Read(14, "Nationality")

    # WorkExperience
    Read(17, "Workplace1")
    Read(18, "Dates1")
    Read(19, "Occupation1")
    Read(20, "MainActivities1")
    Read(21, "Workplace2")
    Read(22, "Dates2")
    Read(23, "Occupation2")
    Read(24, "MainActivities2")
    Read(25, "Workplace3")
    Read(26, "Dates3")
    Read(27, "Occupation3")
    Read(28, "MainActivities3")

    # EducationTraining
    Read(31, "HighSchool")
    Read(32, "College/University")
    Read(33, "SubjectsStudied")
    Read(34, "YearsStudied")
    Read(35, "QualificationsAwarded")
    Read(36, "Master1")
    Read(37, "Master2")

    # PersonalSkills
    Read(40, "CommunicationSkills")
    Read(41, "OrganizationalManagerialSkills")
    Read(42, "JobRelatedSkills")
    Read(43, "ComputerSkills")
    Read(44, "OtherSkills")
    Read(45, "DrivingLicense")

    # Languages
    Read(48, "MotherLanguage")
    Read(50, "ModernLanguage1")
    Read(51, "Level1")
    Read(52, "ModernLanguage2")
    Read(53, "Level2")

    # AdditionalInformation
    Read(56, "Publications")
    Read(57, "Presentations")
    Read(58, "Projects")
    Read(59, "Conferences")
    Read(60, "HonoursAndAwards")
    Read(61, "Memberships")

    # Short Description
    Read(63, "ShortDescription")

    # Hobbies
    Read(65, "Hobbies")

    CVData["PersonalityTypeMB"] = ""
    CVData["PersonalityTypeBF"] = ""

    Person.append(CVData)

#####################################################################################################################################
#Functions

entrydata = []
entrycriteria = []
pressed = 0

JobSectors = {
    "Animals_VeterinaryScience": {
        "School/College": ["high school", "university", "college", "veterinary", "medicine", "life sciences", "research",
                           "institute", "agricultural", "animal", "care", "bioscience", "health", "welfare", "science"],
        "WorkExperience": ["veterenian", "assistant", "caretaker", "animal", "technician", "zoo", "aquarium",
                           "animal shelter", "animal control", "stable", "kennel", "groomers", "trainers", "park",
                           "veterinary office", "clinic", "hospital", "rescue leagues", "humane societies", "pet store",
                           "wildlife", "laboratory", "slaughterhouse", "medical", "research", "care", "animal welfare",
                           "animal conservation", "equine sport"],
        "Skills": ["caring for others", "communication", "critical thinking", "active listening", "customer service",
                   "decision making", "independence", "investigation", "animal care", "observing behaviour",
                   "physical fitness", "problem solving", "recording information", "biology", "science"],
        "ExtraSkills": [],
        "Personality": [],
        "School/College_Score": 0,
        "WorkExperience_Score": 0,
        "Skills_Score": 0,
        "ExtraSkills_Score": 0,
        "Personality_Score": 0
    },
    "Farming_Horticulture_Forestry": {
        "School/College": ["high school", "university", "college", "farming", "horticulture", "forestry", "ecosystem",
                           "agri-biosciences", "agricultural", "science", "agri-food", "environment", "management",
                           "agricultural engineering", "soil", "agricultural mechanics", "agricultural technology",
                           "land"],
        "WorkExperience": ["horticulture", "forestry", "agriculture", "landscaping", "farm", "agri", "agronomy",
                           "quality assurance", "production", "technician", "business", "quality control", "beef",
                           "forest worker", "agricultural inspector", "horticultural manager", "soil scientist",
                           "florist", "laboratory", "dairy industry", "conservation", "nature", "environment",
                           "stud groom", "grounds person", "managing", "land", "crops", "livestock", "outdoors",
                           "research institute", "production farm", "nursery", "parks", "botanic garden",
                           "conservation area"],
        "Skills": ["active learning", "communication", "crop management", "active listening", "data analysis",
                   "statistics", "decision making", "developing relationships", "education", "training", "adaptability",
                   "independence", "initiative", "leadership", "maintaining machinery", "negotiation", "animal care"],
        "ExtraSkills": [],
        "Personality": [],
        "School/College_Score": 0,
        "WorkExperience_Score": 0,
        "Skills_Score": 0,
        "ExtraSkills_Score": 0,
        "Personality_Score": 0
    },
    "Food_Beverages": {
        "School/College": ["high school", "university", "college", "food", "food health", "nutrition", "baker", "bakery",
                           "patisserie", "bar", "cookery", "culinary arts", "management", "chocolatier", "food service",
                           "food technologist", "health", "fishmonger", "apprenticeship", "production", "distribution",
                           "preparation", "serving", "cook"],
        "WorkExperience": ["food science", "restaurant", "nightlife", "specialist", "artisan foods", "beverages",
                           "food", "culinary", "butcher", "chef", "health and safety", "barista", "catering assistant",
                           "nutritionist", "sommelier", "food scientist", "waiting staff", "waiter", "waitress", "bar",
                           "food chemist", "cafeteria", "cafe", "pizzeria", "kitchen", "food truck", "dietitians",
                           "team member", "production", "distribution", "preparation", "serving", "cook"],
        "Skills": ["communication", "customer service", "education", "training", "food production",
                   "maintaining machinery", "managing resources", "physical activity", "quality control", "research",
                   "time management", "budgeting"],
        "ExtraSkills": [],
        "Personality": [],
        "School/College_Score": 0,
        "WorkExperience_Score": 0,
        "Skills_Score": 0,
        "ExtraSkills_Score": 0,
        "Personality_Score": 0
    },
    "Maritime_Fishing_Aquaculture": {
        "School/College": ["high school", "university", "college","maritime", "marine", "fishing", "aquaculture",
                           "navigation", "naval transport", "marine engineering", "aquaponic", "marine science",
                           "marine biology", "marine zoology", "seafood"],
        "WorkExperience": ["maritime", "aquaculture", "fishing", "fish farming", "maritime tourism", "marine science", "marine technology",
                           "shipping", "maritime transport", "seafood", "fish farm", "naval", "coastguard",
                           "marine engineer", "deckhand", "hydrologist", "oceanographer", "lifeguard", "geologist",
                           "marine biologist", "sale", "seafood", "kitchen", "distribution", "boat", "ship", "sea",
                           "ocean", "shell"],
        "Skills": ["communication", "active listening", "geography", "maintaining machinery", "managing resources",
                   "animal care", "operating machinery", "people management", "physical fitness", "teamwork", "technology"],
        "ExtraSkills": [],
        "Personality": [],
        "School/College_Score": 0,
        "WorkExperience_Score": 0,
        "Skills_Score": 0,
        "ExtraSkills_Score": 0,
        "Personality_Score": 0
    },
    "Biological_Chemical_Pharmaceutical_Science": {
        "School/College": ["high school", "university", "college", "drug", "chemical", "science", "biological",
                           "biopharma", "biosciences", "pharmaceutical", "chemistry", "biology", "analytical",
                           "medicine"],
        "WorkExperience": ["biology", "chemistry", "pharmaceutical", "science", "assistant", "laboratory", "research",
                           "analytical", "agri", "bioscience", "chemist", "biotechnician", "production operator",
                           "bio", "clinic", "quality specialist", "monitor", "effect"],
        "Skills": ["chemistry", "complying with regulations", "critical thinking", "data analyses", "statistics",
                   "engineering", "health", "lab work", "manufacturing", "maths", "operating machinery", "biology",
                   "problem solving", "public health", "quality control", "recording information", "teamwork"],
        "ExtraSkills": [],
        "Personality": [],
        "School/College_Score": 0,
        "WorkExperience_Score": 0,
        "Skills_Score": 0,
        "ExtraSkills_Score": 0,
        "Personality_Score": 0
    },
    "BiomedicalTechnologies_Medtech": {
        "School/College": ["high school", "university", "college", "biomedical", "technology", "tehnologies", "medtech",
                           "research", "development", "plastics", "polymer", "clinical trials", "medical", "medicine",
                           "therapeutics", "science", "applied science", "laboratory", "chemistry", "biology",
                           "diagnosis", "prevention", "treatment", "diseases"],
        "WorkExperience": ["laboratory", "hospital", "clinic", "biomedical", "molecular diagnostics", "technician",
                           "biomedical electronics", "biotechnology", "biopharmaceutical", "science", "assistant",
                           "analyst", "informatics", "research", "bioengineering", "cloning", "molecular", "biology",
                           "health care", "facilities", "equipment", "medical device", "diagnosis", "prevention",
                           "treatment", "diseases", "monitor", "development", "manufacturing"],
        "Skills": ["chemistry", "complying with regulations", "conducting experiments", "creating",
                   "following processes", "critical thinking", "data analysis", "statistics", "electronics",
                   "engineering", "lab work", "manufacturing", "maths", "operating machinery", "problem solving",
                   "quality control", "recording information", "biology", "teamwork"],
        "ExtraSkills": [],
        "Personality": [],
        "School/College_Score": 0,
        "WorkExperience_Score": 0,
        "Skills_Score": 0,
        "ExtraSkills_Score": 0,
        "Personality_Score": 0
    },
    "Computers_ICT": {
        "School/College": ["high school", "university", "college", "software", "programming", "hardware", "manufacturing",
                           "internet", "computing", "gaming", "computer", "stem", "computer science", "technology",
                           "information technology", "data science", "computer engineering", "digital", "robotics", "ai",
                           "ict", "security", "data", "network", "electronics", "manufacture", "sales"],
        "WorkExperience": ["software", "programming", "hardware", "manufacturing", "internet", "computing", "gaminng",
                           "computer", "ict", "stem", "network", "engineer", "it", "system", "web", "web developer",
                           "system analyst", "software engineer", "computer engineering", "application", "developer",
                           "security analyst", "graphics", "graphics programmer", "game", "digital", "animation",
                           "game designer", "esports", "adobe", "internet", "electronics", "manufacture", "sales",
                           "development", "microsoft", "apple", "linux", "windows"],
        "Skills": ["communication", "critical thinking", "data analysis", "design", "electronics", "manufacturing",
                   "maths", "problem solving", "programming", "project management", "quality control",
                   "recording information", "teamwork", "technology", "using computers", "python", "javascript", "java",
                   "c#", "c", "c++", "php", "sql", "go", "html", "css", "swift", "security", "graphics", "web", "email",
                   "social media", "word", "excel", "outlook", "powerpoint", "onenote", "access", "hardware",
                   "web development", "open source", "data structures", "coding", "machine learning", "debugging",
                   "cryptography", "windows", "linux", "ios", "virus", "antivirus", "ubuntu", "network", "ai",
                   "photoshop", "crypto", "games", "forensics", "phishing", "robots", "operating systems", "3d printing",
                   "esports", "arduino", "machine"],
        "ExtraSkills": [],
        "Personality": [],
        "School/College_Score": 0,
        "WorkExperience_Score": 0,
        "Skills_Score": 0,
        "ExtraSkills_Score": 0,
        "Personality_Score": 0
    },
    "Construction_Architecture_Property": {
        "School/College": ["high school", "university", "college", "construction", "architecture", "property",
                           "building", "architectural", "technology", "property", "auctioneer", "estate agency",
                           "design", "plumbing", "brickwork", "carpentry", "joinery", "electrical", "plastering",
                           "bricklaying", "safety", "gas"],
        "WorkExperience": ["construction", "architecture", "surveying", "construction project", "planning", "trades",
                           "construction management", "civil engineering", "property management", "auctioneer",
                           "road", "railway", "stadium", "building", "home", "apartment", "hotel", "architect",
                           "planner", "engineer", "materials", "equipment", "labourer", "steel worker", "pipe layer",
                           "scaffolder", "asphalt layer", "demolition", "carpenter", "site technician", "glazier",
                           "stonemason", "welder", "plumber", "bricklayer", "tiler", "plasterer", "bridge", "surveyor",
                           "designer", "structural engineer", "building technician", "driller", "geotechnician",
                           "radiographer", "cartographer", "draughtsperson", "carpenter", "electrical", "plasterer",
                           "painter", "groundworks person", "engineer", "gas"],
        "Skills": ["practical", "coordination", "planning", "manual labour", "team work", "independence", "underground",
                   "wood", "steel", "machine", "technical", "complying with regulations", "critical thinking",
                   "data analysis", "decision making", "design", "tunnel", "engineering", "safety", "independence",
                   "leadership", "maintaining machinery", "managing resources", "operating machinery", "adaptability",
                   "people management", "physical activity", "physical fitness", "prioritising work", "persuasion"],
        "ExtraSkills": [],
        "Personality": [],
        "School/College_Scores": [],
        "WorkExperience_Scores": [],
        "Skills_Scores": [],
        "ExtraSkills_Scores": [],
        "Personality_Scores": []
    },
    "Earth_Environment": {
        "School/College": ["high school", "university", "college", "earth", "environment", "nature", "biology",
                           "ecology", "energy", "conservation", "ecosystem", "climate", "climate change",
                           "sustainable energy", "protect", "earth science", "environmental science", "renewable",
                           "technologies", "wild", "pollution", "law", "economy", "agricultural", "geography",
                           "archeology", "biodiversity", "park", "habitat", "resource", "atmosphere"],
        "WorkExperience": ["earth", "environment", "protect", "climate change", "science", "energy", "sustainable",
                           "recycling", "economy", "agency", "environmental legislation", "resources", "meteorologist",
                           "human activities", "environmental scientist", "environmental inspector", "impact",
                           "renewable energy", "geologist", "ecologist", "nature", "phenomena", "office environment",
                           "outdoors", "energy engineer", "quarry", "conservation", "surveyor", "recycling", "landscape",
                           "water", "environmental technician", "arboriculture", "driller", "turbine", "scientist",
                           "sustainability", "microbiologist", "environmental consultant", "laboratory", "analyst",
                           "animal species", "habitats", "warning", "mineral resource", "atmosphere", "greenhouse",
                           "green", "reservation", "fuels" , "natural hazards", "solar", "wave", "soils", "vulcano",
                           "earthquake", "tsunami", "industrial site", "office", "marine biologist","geographer",
                           "environmental chemist", "wildlife biologist", "water quality", "consulting company"],
        "Skills": ["fuels", "greenhouse gasses", "ground", "mineral", "natural hazards", "chemistry", "communication",
                   "computing with regulations", "critical thinking", "data analysis", "enforcing laws", "regulations",
                   "engineering", "geography", "geology", "analysing system", "managing resources", "observation",
                   "assessment", "animal care", "physics", "problem solving", "recording information", "science",
                   "writing"],
        "ExtraSkills": [],
        "Personality": [],
        "School/College_Scores": [],
        "WorkExperience_Scores": [],
        "Skills_Scores": [],
        "ExtraSkills_Scores": [],
        "Personality_Scores": []
    },
    "Engineering_Manufacturing_Energy": {
        "School/College": ["high school", "university", "school", "engineering", "manufacturing", "energy", "chemical",
                           "civil", "electrical", "mechanical", "technology", "polytechnic", "machinery", "electrical",
                           "electronic", "engineering", "mechanical", "utilities", "chemical engineering"],
        "WorkExperience": ["engineer", "manufacturing", "energy", "science", "maths", "chemical", "civil", "electrical",
                           "mechanical", "utilities", "maths", "physics", "business", "communications", "healthcare",
                           "materials", "pharmaceuticals", "physical infrastructure", "transport", "water", "mechanic",
                           "radiographer", "naval", "patent", "energy engineer", "wood", "utility specialist",
                           "computer scientist", "construction", "electrical", "technologist", "consultant", "worker",
                           "horologist", "industrial", "automation", "automotive", "production operator",
                           "manufacturing team member", "operator", "industrial plant", "office", "worksite",
                           "production site", "factory", "plant", "mill", "assembler", "fabricator", "baker",
                           "upholsterer", "welder", "cutter", "woodworker", "sewer", "tailor"],
        "Skills": ["communication", "design", "electronics", "engineering", "health", "safety", "maintaining machinery",
                   "managing resources", "manufacturing", "maths", "attention to detail", "problem solving",
                   "project management", "project planning", "quality control", "recording information", "teamwork",
                   "technology", "using computers"],
        "ExtraSkills": [],
        "Personality": [],
        "School/College_Scores": [],
        "WorkExperience_Scores": [],
        "Skills_Scores": [],
        "ExtraSkills_Scores": [],
        "Personality_Scores": []
    },
    "Physics_Mathematics_SpaceScience": {
        "School/College": ["high school", "university", "college", "physics", "mathematics", "space", "science",
                           "research", "statistics", "data analysis", "astronomy", "technology"],
        "WorkExperience": ["academia", "research", "teach", "mathematics", "space", "physics", "statistics",
                           "data analysis", "space science", "tech", "space agency", "statistician", "chemistry",
                           "astronomy", "earth sciences", "mathematical", "algorithms", "models",
                           "computational techniques", "formulae", "meteorologist", "weather forecaster", "financial",
                           "data scientist", "actuary", "physicist", "astronaut", "mathematician", "software engineer",
                           "risk analyst", "it", "epidemiologist", "mechanical engineer", "laboratory", "workshop",
                           "hospital", "research center", "observatory", "development companies", "space exploration",
                           "medicine", "robotics", "spaceship", "computational physicist"],
        "Skills": ["collect data", "sort data", "analyse data", "logical thinking", "analytical", "complex",
                   "communication", "conducting experiments", "data analysis", "statistics", "education", "engineering",
                   "lab work", "maths", "operating machinery", "physiscs", "attention to detail", "problem solving",
                   "project management", "quality control", "recording information", "science", "teamwork"],
        "ExtraSkills": [],
        "Personality": [],
        "School/College_Scores": [],
        "WorkExperience_Scores": [],
        "Skills_Scores": [],
        "ExtraSkills_Scores": [],
        "Personality_Scores": []
    },
    "Healthcare": {
        "School/College": ["high school", "university", "college", "medicine", "nursery", "midwifery", "paramedic",
                           "pharmacy", "dentistry", "medical"],
        "WorkExperience": ["medicine", "healthcare", "doctor", "medic", "nurse", "paramedic"],
        "Skills": [],
        "ExtraSkills": [],
        "Personality": [],
        "School/College_Scores": [],
        "WorkExperience_Scores": [],
        "Skills_Scores": [],
        "ExtraSkills_Scores": [],
        "Personality_Scores": []
    },
    "Leisure_Sport_Fitness": {
        "School/College": [],
        "WorkExperience": [],
        "Skills": [],
        "ExtraSkills": [],
        "Personality": [],
        "School/College_Scores": [],
        "WorkExperience_Scores": [],
        "Skills_Scores": [],
        "ExtraSkills_Scores": [],
        "Personality_Scores": []
    },
    "Psychology_SocialCare": {
        "School/College": [],
        "WorkExperience": [],
        "Skills": [],
        "ExtraSkills": [],
        "Personality": [],
        "School/College_Scores": [],
        "WorkExperience_Scores": [],
        "Skills_Scores": [],
        "ExtraSkills_Scores": [],
        "Personality_Scores": []
    },
    "Art_Craft_Design": {
        "School/College": [],
        "WorkExperience": [],
        "Skills": [],
        "ExtraSkills": [],
        "Personality": [],
        "School/College_Scores": [],
        "WorkExperience_Scores": [],
        "Skills_Scores": [],
        "ExtraSkills_Scores": [],
        "Personality_Scores": []
    },
    "Fashion_Beauty": {
        "School/College": [],
        "WorkExperience": [],
        "Skills": [],
        "ExtraSkills": [],
        "Personality": [],
        "School/College_Scores": [],
        "WorkExperience_Scores": [],
        "Skills_Scores": [],
        "ExtraSkills_Scores": [],
        "Personality_Scores": []
    },
    "Media_Film_Publishing": {
        "School/College": [],
        "WorkExperience": [],
        "Skills": [],
        "ExtraSkills": [],
        "Personality": [],
        "School/College_Scores": [],
        "WorkExperience_Scores": [],
        "Skills_Scores": [],
        "ExtraSkills_Scores": [],
        "Personality_Scores": []
    },
    "Music_PerformingArts": {
        "School/College": [],
        "WorkExperience": [],
        "Skills": [],
        "ExtraSkills": [],
        "Personality": [],
        "School/College_Scores": [],
        "WorkExperience_Scores": [],
        "Skills_Scores": [],
        "ExtraSkills_Scores": [],
        "Personality_Scores": []
    },
    "Community_Voluntary": {
        "School/College": [],
        "WorkExperience": [],
        "Skills": [],
        "ExtraSkills": [],
        "Personality": [],
        "School/College_Scores": [],
        "WorkExperience_Scores": [],
        "Skills_Scores": [],
        "ExtraSkills_Scores": [],
        "Personality_Scores": []
    },
    "Education_Teaching": {
        "School/College": [],
        "WorkExperience": [],
        "Skills": [],
        "ExtraSkills": [],
        "Personality": [],
        "School/College_Scores": [],
        "WorkExperience_Scores": [],
        "Skills_Scores": [],
        "ExtraSkills_Scores": [],
        "Personality_Scores": []
    },
    "History_Culture_Languages": {
        "School/College": [],
        "WorkExperience": [],
        "Skills": [],
        "ExtraSkills": [],
        "Personality": [],
        "School/College_Scores": [],
        "WorkExperience_Scores": [],
        "Skills_Scores": [],
        "ExtraSkills_Scores": [],
        "Personality_Scores": []
    },
    "Law_Legal": {
        "School/College": [],
        "WorkExperience": [],
        "Skills": [],
        "ExtraSkills": [],
        "Personality": [],
        "School/College_Scores": [],
        "WorkExperience_Scores": [],
        "Skills_Scores": [],
        "ExtraSkills_Scores": [],
        "Personality_Scores": []
    },
    "PublicAdministration_Politics_EU": {
        "School/College": [],
        "WorkExperience": [],
        "Skills": [],
        "ExtraSkills": [],
        "Personality": [],
        "School/College_Scores": [],
        "WorkExperience_Scores": [],
        "Skills_Scores": [],
        "ExtraSkills_Scores": [],
        "Personality_Scores": []
    },
    "Security_Defence_LawEnforcement": {
        "School/College": [],
        "WorkExperience": [],
        "Skills": [],
        "ExtraSkills": [],
        "Personality": [],
        "School/College_Scores": [],
        "WorkExperience_Scores": [],
        "Skills_Scores": [],
        "ExtraSkills_Scores": [],
        "Personality_Scores": []
    },
    "Accountancy_Taxation": {
        "School/College": [],
        "WorkExperience": [],
        "Skills": [],
        "ExtraSkills": [],
        "Personality": [],
        "School/College_Scores": [],
        "WorkExperience_Scores": [],
        "Skills_Scores": [],
        "ExtraSkills_Scores": [],
        "Personality_Scores": []
    },
    "Banking_FinancialServices": {
        "School/College": [],
        "WorkExperience": [],
        "Skills": [],
        "ExtraSkills": [],
        "Personality": [],
        "School/College_Scores": [],
        "WorkExperience_Scores": [],
        "Skills_Scores": [],
        "ExtraSkills_Scores": [],
        "Personality_Scores": []
    },
    "Insurance": {
        "School/College": [],
        "WorkExperience": [],
        "Skills": [],
        "ExtraSkills": [],
        "Personality": [],
        "School/College_Scores": [],
        "WorkExperience_Scores": [],
        "Skills_Scores": [],
        "ExtraSkills_Scores": [],
        "Personality_Scores": []
    },
    "Advertising_Marketing_PublicRelations": {
        "School/College": [],
        "WorkExperience": [],
        "Skills": [],
        "ExtraSkills": [],
        "Personality": [],
        "School/College_Scores": [],
        "WorkExperience_Scores": [],
        "Skills_Scores": [],
        "ExtraSkills_Scores": [],
        "Personality_Scores": []
    },
    "BusinessManagement_HumanResources": {
        "School/College": [],
        "WorkExperience": [],
        "Skills": [],
        "ExtraSkills": [],
        "Personality": [],
        "School/College_Scores": [],
        "WorkExperience_Scores": [],
        "Skills_Scores": [],
        "ExtraSkills_Scores": [],
        "Personality_Scores": []
    },
    "Clerical_Administration": {
        "School/College": [],
        "WorkExperience": [],
        "Skills": [],
        "ExtraSkills": [],
        "Personality": [],
        "School/College_Scores": [],
        "WorkExperience_Scores": [],
        "Skills_Scores": [],
        "ExtraSkills_Scores": [],
        "Personality_Scores": []
    },
    "Sales_Retail_Purchasing": {
        "School/College": [],
        "WorkExperience": [],
        "Skills": [],
        "ExtraSkills": [],
        "Personality": [],
        "School/College_Scores": [],
        "WorkExperience_Scores": [],
        "Skills_Scores": [],
        "ExtraSkills_Scores": [],
        "Personality_Scores": []
    },
    "Tourism_Hospitality": {
        "School/College": [],
        "WorkExperience": [],
        "Skills": [],
        "ExtraSkills": [],
        "Personality": [],
        "School/College_Scores": [],
        "WorkExperience_Scores": [],
        "Skills_Scores": [],
        "ExtraSkills_Scores": [],
        "Personality_Scores": []
    },
    "Transport_Logistics": {
        "School/College": [],
        "WorkExperience": [],
        "Skills": [],
        "ExtraSkills": [],
        "Personality": [],
        "School/College_Scores": [],
        "WorkExperience_Scores": [],
        "Skills_Scores": [],
        "ExtraSkills_Scores": [],
        "Personality_Scores": []
    }
}
Functions = {
    0: ["assistant", "intern", "trainee", "apprentice", "worker", "labourer", "employee"],
    1: ["representative", "specialist", "coordinator", "analyst", "administrator", "generalist", "consultant",
        "associate", "technician", "agent", "surveyor", "engineer"],
    2: ["manager", "head", "hod"],
    3: ["director", "vp"],
    4: ["coo", "cfo", "cto", "cmo", "chro", "cpo", "chief", "vice president", "officer"],
    5: ["chief executive officer", "ceo", "president"],
    6: ["chairman"]
}

Qualifications = {
    1: ["gcse", "grades d-g", "l1", "level 1", "foundation", "entry level", "traineeship", "nvq level 1"],
    2: ["grades a-c", "l2", "level 2", "intermediate apprenticeship", "nvq level 2"],
    3: ["a-level", "a2", "as", "t-level", "l3", "level 3", "certificate", "advanced apprenticeship", "nvq level 3"],
    4: ["bachelor", "university degree", "undergraduate degree", "ba", "bsc", "foundation degree", "fda", "fdsc", "hnd",
        "hnc", "higher national", "higher apprenticeship", "nvq level 4", "foundation degree"],
    5: ["master", "ma", "msc", "mphil", "nvq level 5", "degree apprenticeship"],
    6: ["phd", "doctorate"]
}

Languages = {
    1: ["romanian", "bulgarian", "hungarian", "bulgarian", "korean", "javanese", "tamil", "turkish",
        "bengali", "vietnamese", "marathi", "egyptian", "iranian", "polish", "indonesian", "gujarati", "malayalam",
        "yoruba", "hausa", "ukrainian", "igbo", "sindhi", "dutch",  "amharic", "magahi", "thai", "saraiki", "somali",
        "sinhalese", "nigerian", "bavarian", "greek", "kazakh", "deccan", "zulu", "tunisian", "rundi", "czech",
        "sylheti", "xiang", "sundanese", "kannada", "tagalog", "gan", "cebuano", "khmer", "turkmen", "croatian",
        "kurdish", "marwari", "haryanvi", "dhundhari", "hmong", "belarusian", "mossi"],
    2: ["hindi", "bengali", "arabic", "french", "german", "russian", "portuguese", "punjabi", "japanese", "italian",
        "latin", "telugu"],
    3: ["english", "mandarin", "chinese", "spanish"]
}

Top50Universities = {


}

Top100Universities = {

}




BigFive = {
    "openness": [],
    "conscientiousness": [],
    "extroversion": [],
    "agreeableness": [],
    "neuroticism": []
}

PersonalityTypes = {
    "ISTJ": {
        "Name": "Logistician",
        "Traits": [],
        "Description": "A Logistician (ISTJ) is someone with the Introverted, Observant, Thinking, and Judging "
                       "personality traits. These people tend to be reserved yet willful, with a rational outlook on"
                       "life. They compose their actions carefully and carry them out with methodical purpose.",
        "Strengths": ["honest, direct, strong-willed, dutiful, very responsible, calm, practical, jacks-of-all-trades"],
        "Weaknesses": ["stubborn, insensitive, always by the book, judgmentall"],
        "WebSite": "https://www.16personalities.com/istj-personality"
    },
    "ISFJ": {
        "Name": "Defender",
        "Traits": [],
        "Description": "A Defender (ISFJ) is someone with the Introverted, Observant, Feeling, and Judging personality traits. These people tend to be warm and unassuming in their own steady way. They’re efficient and responsible, giving careful attention to practical details in their daily lives.",
        "Strengths": ["supportive, reliable, observant, enthusiastic, hardworking, good practical skills"],
        "Weaknesses": ["overly humble, taking things personally, repressing their feelings, overcommitted, reluctant to change"],
        "WebSite": "https://www.16personalities.com/isfj-personality"
    },
    "INFJ": {
        "Name": "Advocate",
        "Traits": [],
        "Description": "An Advocate (INFJ) is someone with the Introverted, Intuitive, Feeling, and Judging personality traits. They tend to approach life with deep thoughtfulness and imagination. Their inner vision, personal values, and a quiet, principled version of humanism guide them in all things.",
        "Strengths": ["creative, insightful, principled, passionate, altruistic"],
        "Weaknesses": ["sensitive to criticism, reluctant to open up, perfectionistic, prone to burnout"],
        "WebSite": "https://www.16personalities.com/infj-personality"
    },
    "INTJ": {
        "Name": "Arhitect",
        "Traits": [],
        "Description": "An Architect (INTJ) is a person with the Introverted, Intuitive, Thinking, and Judging personality traits. These thoughtful tacticians love perfecting the details of life, applying creativity and rationality to everything they do. Their inner world is often a private, complex one.",
        "Strengths": ["rational, informed, independent, determined, curious, original"],
        "Weaknesses": ["arrogant, dismissive of emotions, overly critical, combative, socially clueless"],
        "WebSite": "https://www.16personalities.com/intj-personality"
    },
    "ISTP": {
        "Name": "Virtuoso",
        "Traits": [],
        "Description": "A Virtuoso (ISTP) is someone with the Introverted, Observant, Thinking, and Prospecting personality traits. They tend to have an individualistic mindset, pursuing goals without needing much external connection. They engage in life with inquisitiveness and personal skill, varying their approach as needed.",
        "Strengths": ["optimistic, energetic, creative, practical, spontaneous, rational, great in a crisis, relaxed"],
        "Weaknesses": ["stubborn, insensitive, private, reserved, easily bored, dislike commitment, risky behaviour"],
        "WebSite": "https://www.16personalities.com/istp-personality"
    },
    "ISFP": {
        "Name": "Adventurer",
        "Traits": [],
        "Description": "An Adventurer (ISFP) is a person with the Introverted, Observant, Feeling, and Prospecting personality traits. They tend to have open minds, approaching life, new experiences, and people with grounded warmth. Their ability to stay in the moment helps them uncover exciting potentials.",
        "Strengths": ["charming, sensitive, imaginative, passionate, curious, artistic"],
        "Weaknesses": ["fiercely independent, unpredictable, easily stressed, overly competitive, fluctuating self-esteem"],
        "WebSite": "https://www.16personalities.com/isfp-personality"
    },
    "INFP": {
        "Name": "Mediator",
        "Traits": [],
        "Description": "A Mediator (INFP) is someone who possesses the Introverted, Intuitive, Feeling, and Prospecting personality traits. These rare personality types tend to be quiet, open-minded, and imaginative, and they apply a caring and creative approach to everything they do.",
        "Strengths": ["empathetic, generous, open-minded, creative, passionate idealistic"],
        "Weaknesses": ["unrealistic, self-isolating, unfocused, emotionally vulnerable, self-critical"],
        "WebSite": "https://www.16personalities.com/infp-personality"
    },
    "INTP": {
        "Name": "Logician",
        "Traits": [],
        "Description": "A Logician (INTP) is someone with the Introverted, Intuitive, Thinking, and Prospecting personality traits. These flexible thinkers enjoy taking an unconventional approach to many aspects of life. They often seek out unlikely paths, mixing willingness to experiment with personal creativity.",
        "Strengths": ["analytical, original, open-minded, curious, objective"],
        "Weaknesses": ["disconnected, insensitive, dissatisfied, impatient, perfectionistic"],
        "WebSite": "https://www.16personalities.com/intp-personality"
    },
    "ESTP": {
        "Name": "Entrepreneur",
        "Traits": [],
        "Description": "An Entrepreneur (ESTP) is someone with the Extraverted, Observant, Thinking, and Prospecting personality traits. They tend to be energetic and action-oriented, deftly navigating whatever is in front of them. They love uncovering life’s opportunities, whether socializing with others or in more personal pursuits.",
        "Strengths": ["bold, rational, practical, original, perceptive, direct, sociable"],
        "Weaknesses": ["insensitive, impatient, risk-prone, unstructured, defiant"],
        "WebSite": "https://www.16personalities.com/estp-personality"
    },
    "ESFP": {
        "Name": "Entertainer",
        "Traits": [],
        "Description": "An Entertainer (ESFP) is a person with the Extraverted, Observant, Feeling, and Prospecting personality traits. These people love vibrant experiences, engaging in life eagerly and taking pleasure in discovering the unknown. They can be very social, often encouraging others into shared activities.",
        "Strengths": ["bold, original, aesthetics and showmanship, practical, observant, excellent people skills"],
        "Weaknesses": ["sensitive, conflict-averse, easily bored, poor long-term planners, unfocused"],
        "WebSite": "https://www.16personalities.com/esfp-personality"
    },
    "ENFP": {
        "Name": "Campaigner",
        "Traits": [],
        "Description": "A Campaigner (ENFP) is someone with the Extraverted, Intuitive, Feeling, and Prospecting personality traits. These people tend to embrace big ideas and actions that reflect their sense of hope and goodwill toward others. Their vibrant energy can flow in many directions.",
        "Strengths": ["curious, perceptive, enthusiastic, excellent communicators, festive, good-natured"],
        "Weaknesses": ["people-pleasing, unfocused, disorganized, overly accommodating, overly optimistic, restless"],
        "WebSite": "https://www.16personalities.com/enfp-personality"
    },
    "ENTP": {
        "Name": "Debater",
        "Traits": [],
        "Description": "A Debater (ENTP) is a person with the Extraverted, Intuitive, Thinking, and Prospecting personality traits. They tend to be bold and creative, deconstructing and rebuilding ideas with great mental agility. They pursue their goals vigorously despite any resistance they might encounter.",
        "Strengths": ["knowledgeable, quick thinkers, original, excellent brainstormers, charismatic, energetic"],
        "Weaknesses": ["argumentative, insensitive, intolerant, difficult to focus"],
        "WebSite": "https://www.16personalities.com/entp-personality"
    },
    "ESTJ": {
        "Name": "Executive",
        "Traits": [],
        "Description": "An Executive (ESTJ) is someone with the Extraverted, Observant, Thinking, and Judging personality traits. They possess great fortitude, emphatically following their own sensible judgment. They often serve as a stabilizing force among others, able to offer solid direction amid adversity.",
        "Strengths": ["dedicated, strong-willed, direct, honest, loyal, patient, reliable, excellent organizer"],
        "Weaknesses": ["inflexible, stubborn, judgmental, too focused on social status, difficult to relax and express emotion"],
        "WebSite": "https://www.16personalities.com/estj-personality"
    },
    "ESFJ": {
        "Name": "Consul",
        "Traits": [],
        "Description": "A Consul (ESFJ) is a person with the Extraverted, Observant, Feeling, and Judging personality traits. They are attentive and people-focused, and they enjoy taking part in their social community. Their achievements are guided by decisive values, and they willingly offer guidance to others.",
        "Strengths": ["strong practical skills, strong sense of duty, very loyal, sensitive, warm, good at connecting with others"],
        "Weaknesses": ["inflexible, reluctant to innovate and improvise, vulnerable to criticism, often too needy, too selfless"],
        "WebSite": "https://www.16personalities.com/esfj-personality"
    },
    "ENFJ": {
        "Name": "Protagonist",
        "Traits": [],
        "Description": "A Protagonist (ENFJ) is a person with the Extraverted, Intuitive, Feeling, and Judging personality traits. These warm, forthright types love helping others, and they tend to have strong ideas and values. They back their perspective with the creative energy to achieve their goals.",
        "Strengths": ["receptive, reliable, passionate, altruistic, charismatic"],
        "Weaknesses": ["unrealistic, overly idealistic, condescending, intense, overly, empathetic"],
        "WebSite": "https://www.16personalities.com/enfj-personality"
    },
    "ENTJ": {
        "Name": "Commander",
        "Traits": [],
        "Description": "A Commander (ENTJ) is someone with the Extraverted, Intuitive, Thinking, and Judging personality traits. They are decisive people who love momentum and accomplishment. They gather information to construct their creative visions but rarely hesitate for long before acting on them.",
        "Strengths": ["efficient, energetic, self-confident, strong-willed, strategic thinkers, charismatic, inspiring"],
        "Weaknesses": ["stubborn, dominant, intolerant, impatient, arrogant, poor handling of emotions, cold, ruthless"],
        "WebSite": "https://www.16personalities.com/entj-personality"
    }
}

Domains = {
    "I": {
        "introverted": {
            "words": ["introverted", "shy", "quiet", "reticent", "introspective", "reclusive", "thinker", "anxious", "reserved"],
            "score": 0
        },
        "loneliness": {
            "words": ["lonely", "independent", "isolated", "desolate", "reclusive"],
            "score": 0
        },
        "listener": {
            "words": ["listener", "open-minded", "observer", "perceptive", "compassionate", "emphatic"],
            "score": 0
        },
        "reserved": {
            "words": ["reserved", "quiet", "anxious", "antisocial"],
            "score": 0
        },
        "SCORE": 0
    },
    "E": {
        "extroverted": {
            "words": ["extroverted", "outgoing", "sociable", "talkative", "friendly"],
            "score": 0
        },
        "outgoing": {
            "words": ["outgoing", "out-going", "affectionate", "demonstrative"],
            "score": 0
        },
        "sociable": {
            "words": ["sociable", "talkative", "friendly", "compasionable", "approachable", "cordial"],
            "score": 0
        },
        "enthusiastic": {
            "words": ["enthusiastic", "keen", "eager", "passionate", "avid", "energetic", "feeling"],
            "score": 0
        },
        "SCORE": 0
    },
    "S": {
        "analytical": {
            "words": ["analytical", "logical", "scientific", "methodical"],
            "score": 0
        },
        "realistic": {
            "words": ["realistic", "practical", "pragmatic", "truthful", "rational", "real"],
            "score": 0
        },
        "systematic": {
            "words": ["systematic", "structured", "organized", "planned", "well-ordered"],
            "score": 0
        },
        "practical": {
            "words": ["practical", "empirical", "actual", "active", "applied", "experential", "effective", "qualified"],
            "score": 0
        },
        "SCORE": 0
    },
    "N": {
        "creative": {
            "words": ["creative", "artistic", "visionary", "imaginative", "inspired", "talented", "original"],
            "score": 0
        },
        "idealistic": {
            "words": ["idealistic", "utopian", "romantic", "unrealistic", "optimistic", "idealized", "dreamer", "utopian"],
            "score": 0
        },
        "visionary": {
            "words": ["visionary", "imaginative", "inventive", "ingenious", "insightful", "introspective", "ambitious"],
            "score": 0
        },
        "inventive": {
            "words": ["inventive", "creative", "original", "skilful", "innovative", "ingenious", "artistic"],
            "score": 0
        },
        "SCORE": 0
    },
    "T": {
        "intellectual": {
            "words": ["smart", "clever", "wise", "intelligent"],
            "score": 0
        },
        "logical": {
            "words": ["logical", "smart", "analytical", "rational", "intelligent", "valid", "coherent", "organized"],
            "score": 0
        },
        "rational": {
            "words": ["rational", "reasoned", "logical", "coherent", "sensible", "deliberate", "balanced", "judicious"],
            "score": 0
        },
        "judgemental": {
            "words": ["judgemental", "narrow-minded", "judgy", "critical", "negative", "subjective"],
            "score": 0
        },
        "SCORE": 0
    },
    "F": {
        "empathetic": {
            "words": [ "affectionate", "understanding", "intuitive", "spiritual", "open", "listener", "comprehensive"],
            "score": 0
        },
        "considerate": {
            "words": ["considerate", "attentive", "thoughtful", "mindful", "obliging", "amiable", "generous", "discreet", "solicitous", "alert", "careful", "cautious"],
            "score": 0
        },
        "sensitive": {
            "words": ["sensitive", "afraid", "emotive", "anxious", "influenceable"],
            "score": 0
        },
        "conscientious": {
            "words": ["conscientious", "considerate", "attentive", "thoughtful", "mindful", "obliging", "amiable", "generous", "discreet", "solicitous", "alert", "careful", "cautious"],
            "score": 0
        },
        "SCORE": 0
    },
    "J": {
        "reserved": {
            "words": ["reserved", "restrained", "reticent", "private", "cautious"],
            "score": 0
        },
        "organized": {
            "words": ["organized", "organizer", "systematic", "arranged", "coordinated", "oriented", "disciplined",
                      "precise", "regular", "meticulous", "controlled", "reasonable"],
            "score": 0
        },
        "logical": {
            "words": ["logical", "smart", "analytical", "rational", "intelligent", "valid", "coherent", "organized"],
            "score": 0
        },
        "stubborn": {
            "words": ["stubborn", "headstrong", "subjective", "firm", "determined", "inflexible"],
            "score": 0
        },
        "SCORE": 0
    },
    "P": {
        "flexible": {
            "words": ["adaptable", "open", "fearless", "brave", "creative", "innovator"],
            "score": 0
        },
        "spontaneous": {
            "words": ["unpredictable", "impulsive", "spontaneous", "happy", "flexible"],
            "score": 0
        },
        "action-oriented": {
            "words": ["action-oriented", "active", "applied", "practical", "proactive", "enterprising", "pragmatist", "advanced", "interactive"],
            "score": 0
        },
        "open-minded": {
            "words": ["curious", "non-judgemental", "open", "respectable", "lovable", "appreciative"],
            "score": 0
        },
        "SCORE": 0
    }
}

Hobbies = {
    "words": ["reading", "travelling", "animal", "gardening", "board games", "knitting", "embroidery", "upcycling",
              "drawing", "painting", "writing", "photography", "graphic design", "volunteer", "cooking", "baking",
              "watching", "films", "documentaries", "walking", "pet", "dancing", "wood crafting", "pottery", "sculpting",
              "chess", "language learning", "acting", "squash", "blog", "social media", "sing", "card games",
              "listening to music", "going out"],
    "domain": [],
    "trait": [],
    "sports": ["basketball", "golf", "running", "walking", "soccer", "volleyball", "badminton", "yoga", "pilates",
               "swimming", "skating", "rugby", "darts", "football", "barre", "tai chi", "stretching", "bowling",
               "hockey", "surfing", "tennis", "baseball", "gymnastics", "climbing", "karate", "horse", "snowboarding",
               "cycling", "archery", "boxing"]
}


"""PersonalityTypes = {
    "ISTJ": ["responsible", "sincere", "analytical", "reserved", "realistic", "systematic", "hardworking", "trustworthy", "practical judgement"],
    "ISFJ": ["warm", "considerate", "gentle", "responsible", "pragmatic", "thorough", "devoted", "helpful"],
    "INFJ": ["idealistic", "organized", "insightful", "dependable", "compassionate", "gentle", "harmony", "cooperation"],
    "INTJ": ["innovative", "independent", "strategic", "logical", "reserved", "insightful"],
    "ISTP": ["action-oriented", "logical", "analytical", "spontaneous", "reserved", "independent", "adventurous"],
    "ISFP": ["gentle", "sensitive", "nurturing", "helpful", "flexible", "realistic"],
    "INFP": ["sensitive", "creative", "idealistic", "perceptive", "caring", "loyal"],
    "INTP": ["intellectual", "logical", "precise", "reserved", "flexible", "imaginative"],
    "ESTP": ["outgoing", "realistic", "action-oriented", "curious", "versatile", "spontaneous"],
    "ESFP": ["playful", "enthusiastic", "friendly", "spontaneous", "tactful", "flexible"],
    "ENFP": ["enthusiastic", "creative", "spontaneous", "optimistic", "supportive", "playful"],
    "ENTP": ["inventive", "enthusiastic", "strategic", "enterprising", "inquisitive", "versatile"],
    "ESTJ": ["efficient", "outgoing", "analytical", "systematic", "dependable", "realistic"],
    "ESFJ": ["friendly", "outgoing", "reliable", "conscientious", "organized", "practical"],
    "ENFJ": ["caring", "enthusiastic", "idealistic", "organized", "diplomatic", "responsible"],
    "ENTJ": ["strategic", "logical", "efficient", "outgoing", "ambitious", "independent"]
}"""

def AnalyzeJob(person: int, sector: str):
    # SCORE = 0

    # Job Score
    JobScore = 0
    highschool_score = 0
    subjects_score = 0
    college_university_score = 0
    qualification_word_score = 0
    qualification_level_score = 1
    master_score = 0
    years_studied = int(Person[person]["YearsStudied"])


    highschool = (Person[person]["HighSchool"].lower()).split(" ")
    for word in highschool:
        if word in JobSectors[sector]["School/College"]:
            highschool_score += 1
    """college_university = (Person[person]["College/University"].lower()).split(" ")
    for word in college_university:
        if word in JobSectors[sector]["School/College"]:
            college_university_score += 1"""
    subjects = (Person[person]["SubjectsStudied"].lower()).split(",")
    for word in subjects:
        if word in JobSectors[sector]["School/College"]:
            subjects_score += 1
    qualifications = (Person[person]["QualificationsAwarded"].lower()).split(",")
    for word in qualifications:
        if word in JobSectors[sector]["School/College"]:
            qualification_word_score += 1
        for value in Qualifications:
            if word in Qualifications[value]:
                qualification_level_score += value
    master1 = (Person[person]["Master1"].lower()).split(" ")
    for word in master1:
        if word in JobSectors[sector]["School/College"]:
            master_score += 1
    master2 = (Person[person]["Master2"].lower()).split(" ")
    for word in master2:
        if word in JobSectors[sector]["School/College"]:
            master_score += 1

    college_nr = Person[person]["College/University"].lower().count("college") + \
                 Person[person]["College/University"].lower().count("university")
    college_university = Person[person]["College/University"].lower()
    subjects_nr = (Person[person]["SubjectsStudied"].lower()).count(",") + 1
    if college_university in Top50Universities:
        rank = 3
    elif college_university in Top100Universities:
        rank = 2
    else:
        rank = 1
    if college_nr != 0:
        college_university_score += college_nr * 5 * rank
        college_university_score += subjects_score * 3 + (subjects_nr - subjects_score)

    if highschool_score == 1:
        JobScore += 3
    elif highschool_score > 1:
        JobScore += 6

    JobScore += college_university_score * years_studied + qualification_word_score * \
               qualification_level_score * 2 + master_score

    # Work Score
    WorkScore = 0
    workscore1 = 0
    workscore2 = 0
    workscore3 = 0
    if Person[person]["Dates1"] != "":
        dates1 = Person[person]["Dates1"].split("-")
        date1_start = dates1[0]
        date1_finish = dates1[1]
        date1_str1 = date1_start.split(".")
        date1_str2 = date1_finish.split(".")
        # date1_1 = datetime.datetime(date1_str1[2], date1_str1[1], date1_str1[0])
        # date1_2 = datetime.datetime(date1_str2[2], date1_str2[1], date1_str2[0])
        date1_1 = date(int(date1_str1[2]), int(date1_str1[1]), int(date1_str1[0]))
        if date1_finish == "current":
            date1_2 = date.today()
        else:
            date1_2 = date(int(date1_str2[2]), int(date1_str2[1]), int(date1_str2[0]))
        time1 = (date1_2 - date1_1).days / 365
    else:
        time1 = 0
    if Person[person]["Dates2"] != "":
        dates2 = Person[person]["Dates2"].split("-")
        date2_start = dates2[0]
        date2_finish = dates2[1]
        date2_str1 = date2_start.split(".")
        date2_str2 = date2_finish.split(".")
        # date2_1 = datetime.datetime(date1_str1[2], date1_str1[1], date1_str1[0])
        # date2_2 = datetime.datetime(date1_str2[2], date1_str2[1], date1_str2[0])
        date2_1 = date(int(date2_str1[2]), int(date2_str1[1]), int(date2_str1[0]))
        if date2_finish == "current":
            date2_2 = date.today()
        else:
            #date2_2 = date(int(date2_str2[2]), int(date2_str2[1]), int(date2_str2[0]))
            date2_2 = date.today()
            print(date2_finish[0])
        time2 = (date2_2 - date2_1).days / 365
    else:
        time2 = 0
    if Person[person]["Dates3"] != "":
        dates3 = Person[person]["Dates3"].split("-")
        date3_start = dates3[0]
        date3_finish = dates3[1]
        date3_str1 = date3_start.split(".")
        date3_str2 = date3_finish.split(".")
        # date3_1 = datetime.datetime(date1_str1[2], date1_str1[1], date1_str1[0])
        # date3_2 = datetime.datetime(date1_str2[2], date1_str2[1], date1_str2[0])
        date3_1 = date(int(date3_str1[2]), int(date3_str1[1]), int(date3_str1[0]))
        if date3_finish == "current":
            date3_2 = date.today()
        else:
            # date3_2 = date(int(date3_str2[2]), int(date3_str2[1]), int(date3_str2[0]))
            date3_2 = date.today()
            print(date3_finish[0])
        time3 = (date3_2 - date3_1).days / 365
    else:
        time3 = 0
    if Person[person]["Workplace1"] != "":
        workscore1 += 2
    if Person[person]["Workplace2"] != "":
        workscore2 += 2
    if Person[person]["Workplace3"] != "":
        workscore3 += 2

    if workscore1 != 0:
        function1_score = 1
        workplace1 = (Person[person]["Workplace1"].lower()).split(" ")
        for word in workplace1:
            word.replace(",", "")
            if word in JobSectors[sector]["WorkExperience"]:
                workscore1 += 3
        occupation1 = (Person[person]["Workplace1"].lower()).split(",")
        for word in occupation1:
            if word in JobSectors[sector]["WorkExperience"]:
                workscore1 += 1
            for value in Functions:
                if word in Functions[value]:
                    function1_score += value
        main_activities1 = (Person[person]["MainActivities1"].lower()).split(",")
        for word in main_activities1:
            if word in JobSectors[sector]["WorkExperience"]:
                workscore1 += 0.5
        WorkScore += workscore1 * function1_score * time1

    if workscore2 != 0:
        function2_score = 1
        workplace2 = (Person[person]["Workplace2"].lower()).split(" ")
        for word in workplace2:
            word.replace(",", "")
            if word in JobSectors[sector]["WorkExperience"]:
                workscore2 += 3
        occupation2 = (Person[person]["Workplace2"].lower()).split(",")
        for word in occupation2:
            if word in JobSectors[sector]["WorkExperience"]:
                workscore2 += 1
            for value in Functions:
                if word in Functions[value]:
                    function2_score += value
        main_activities2 = (Person[person]["MainActivities2"].lower()).split(",")
        for word in main_activities2:
            if word in JobSectors[sector]["WorkExperience"]:
                workscore2 += 0.5
        WorkScore += workscore2 * function2_score * time2

    if workscore3 != 0:
        function3_score = 1
        workplace3 = (Person[person]["Workplace3"].lower()).split(" ")
        for word in workplace3:
            word.replace(",", "")
            if word in JobSectors[sector]["WorkExperience"]:
                workscore3 += 3
        occupation3 = (Person[person]["Workplace3"].lower()).split(",")
        for word in occupation3:
            if word in JobSectors[sector]["WorkExperience"]:
                workscore3 += 1
            for value in Functions:
                if word in Functions[value]:
                    function3_score += value
        main_activities3 = (Person[person]["MainActivities3"].lower()).split(",")
        for word in main_activities3:
            if word in JobSectors[sector]["WorkExperience"]:
                workscore3 += 0.5
        WorkScore += workscore3 * function3_score * time3

    # Language
    LanguageScore = 0
    language_mother_score = 0
    language_modern_score = 0
    level1 = 1
    level2 = 1
    mother_language = Person[person]["MotherLanguage"].lower()
    modern_language1 = Person[person]["ModernLanguage1"].lower()
    modern_language2 = Person[person]["ModernLanguage2"].lower()
    for value in Languages:
        if mother_language in Languages[value]:
            language_mother_score += value
        if modern_language1 in Languages[value]:
            match Person[person]["Level1"].lower:
                case "a1":
                    level1 = 1
                case "a2":
                    level1 = 2
                case "b1":
                    level1 = 3
                case "b2":
                    level1 = 4
                case "c1":
                    level1 = 5
                case "c2":
                    level1 = 6
            language_modern_score += value * level1
        if modern_language2 in Languages[value]:
            match Person[person]["Level2"].lower:
                case "a1":
                    level2 = 1
                case "a2":
                    level2 = 2
                case "b1":
                    level2 = 3
                case "b2":
                    level2 = 4
                case "c1":
                    level2 = 5
                case "c2":
                    level2 = 6
            language_modern_score += value * level2
    LanguageScore += language_mother_score + language_modern_score

    # Skills Score
    SkillsScore = 0
    related_skills_score = 0
    extra_skills_score = 0
    communication_skills = (Person[person]["CommunicationSkills"].lower()).split(",")
    organizational_skills = (Person[person]["OrganizationalManagerialSkills"].lower()).split(",")
    job_skills = (Person[person]["JobRelatedSkills"].lower()).split(",")
    computer_skills = (Person[person]["ComputerSkills"].lower()).split(",")
    other_skills = (Person[person]["OtherSkills"].lower()).split(",")
    for word in JobSectors[sector]["Skills"]:
        if word in communication_skills:
            related_skills_score += 1
        if word in organizational_skills:
            related_skills_score += 1
        if word in job_skills:
            related_skills_score += 2
        if word in computer_skills:
            related_skills_score += 1
    for word in job_skills:
        if word in JobSectors[sector]["WorkExperience"]:
            related_skills_score += 2
    for word in JobSectors[sector]["ExtraSkills"]:
        if word not in JobSectors[sector]["Skills"]:
            if word in communication_skills:
                extra_skills_score += 1
            if word in organizational_skills:
                extra_skills_score += 1
            if word in job_skills:
                extra_skills_score += 2
            if word in computer_skills:
                extra_skills_score += 1
            if word in other_skills:
                extra_skills_score += 1
    if Person[person]["DrivingLicense"] != "":
        driving_skills = 4
    else:
        driving_skills = 0
    SkillsScore = related_skills_score * 5 + extra_skills_score * 2.5 + driving_skills

    # Additional Information
    InformationScore = 0
    InformationScore += (Person[person]["Publications"].count(",") + 1) * 2
    InformationScore += (Person[person]["Presentations"].count(",") + 1) * 2
    InformationScore += (Person[person]["Projects"].count(",") + 1) * 2
    InformationScore += (Person[person]["Conferences"].count(",") + 1) * 2
    InformationScore += (Person[person]["HonoursAndAwards"].count(",") + 1) * 3
    InformationScore += (Person[person]["Memberships"].count(",") + 1) * 3

    # Personality
    PersonalityScore = 0
    type = Person[person]["PersonalityTypeMB"]

    SCORE = JobScore + WorkScore + SkillsScore + LanguageScore + InformationScore + PersonalityScore
    return SCORE

def AnalyzeJobs(person):
    JobList = []
    for sector in JobSectors:
        pair = (sector, AnalyzeJob(person, sector))
        JobList.append(pair)
    JobList.sort(key=lambda x: x[1], reverse=True)
    return JobList


def AnalyzePersonality(person: int):
    PersonalityScore = 0
    DomainIE_I = 0
    DomainIE_E = 0
    DomainSN_S = 0
    DomainSN_N = 0
    DomainTF_T = 0
    DomainTF_F = 0
    DomainJP_J = 0
    DomainJP_P = 0
    hobbies = (Person[person]["Hobbies"].lower()).split(",")
    description = (Person[person]["ShortDescription"].lower()).split(",")
    """for word in description:
        for domain in Domains:
            for trait in Domains[domain]:
                if word in Domains[domain][trait]["words"]:
                    Domains[domain][trait]["score"] += 1"""
    for word in hobbies:
        if word in Hobbies["words"]:
            index = Hobbies["words"].index(word)
            Domains[Hobbies["domain"][index]][Hobbies["trait"][index]]["score"] += 1

    """for trait, value in Domains["I"]:
        DomainIE_I += Domains["I"][trait]["score"]
    for trait in Domains["E"]:
        DomainIE_E += Domains["E"][trait]["score"]
    for trait in Domains["S"]:
        DomainSN_S += Domains["S"][trait]["score"]
    for trait in Domains["N"]:
        DomainSN_N += Domains["N"][trait]["score"]
    for trait in Domains["T"]:
        DomainTF_T += Domains["T"][trait]["score"]
    for trait in Domains["F"]:
        DomainTF_F += Domains["F"][trait]["score"]
    for trait in Domains["J"]:
        DomainJP_J += Domains["J"][trait]["score"]
    for trait in Domains["I"]:
        DomainJP_P += Domains["P"][trait]["score"]"""

    DomainIE = DomainIE_I + DomainIE_E + 1
    DomainSN = DomainSN_S + DomainSN_N + 1
    DomainTF = DomainTF_T + DomainTF_F + 1
    DomainJP = DomainJP_J + DomainJP_P + 1

    I = DomainIE_I / DomainIE * 100
    E = DomainIE_E / DomainIE * 100
    S = DomainSN_S / DomainSN * 100
    N = DomainSN_N / DomainSN * 100
    T = DomainTF_T / DomainTF * 100
    F = DomainTF_F / DomainTF * 100
    J = DomainJP_J / DomainJP * 100
    P = DomainJP_P / DomainJP * 100

    if I > E:
        Person[person]["PersonalityTypeMB"] += "I"
    else:
        Person[person]["PersonalityTypeMB"] += "E"
    if S > N:
        Person[person]["PersonalityTypeMB"] += "S"
    else:
        Person[person]["PersonalityTypeMB"] += "N"
    if T > F:
        Person[person]["PersonalityTypeMB"] += "T"
    else:
        Person[person]["PersonalityTypeMB"] += "F"
    if J > P:
        Person[person]["PersonalityTypeMB"] += "J"
    else:
        Person[person]["PersonalityTypeMB"] += "P"


    for trait, value in Domains["I"]:
        DomainIE_I += Domains["I"][trait]["score"]
    for trait in Domains["E"]:
        DomainIE_E += Domains["E"][trait]["score"]
    DomainIE = DomainIE_I + DomainIE_E
    I = DomainIE_I / DomainIE * 100
    E = DomainIE_E / DomainIE * 100
    if I > E:
        Person[person]["PersonalityTypeMB"] += "I"
    else:
        Person[person]["PersonalityTypeMB"] += "E"



def MakeLabelCV(frame, text, row, column, entry_width):
    label = Label(frame, text = text,
                   bg = "darkorange", fg = "white",
                   height = 1,
                   font = ('calibre', 14))
    label.grid(row = row, column = column, sticky = 'e', padx=10, pady=10, ipady=3)
    if entry_width != 0:
        name = StringVar()
        entrydata.append(name)
        entry = Entry(frame, textvariable=name, width=entry_width, font = ('calibre', 12))
        entry.grid(row=row, column=column+1, columnspan= 3, sticky='w', padx=30, pady=10, ipady=3)

def MakeCV():
    directory = "CVs"
    parent_dir = "D:/"
    path = os.path.join(parent_dir, directory)
    try:
       os.mkdir(path)
    except FileExistsError:
        pass
    file_path = path + "/" + Person[-1]["FirstName"] + Person[-1]["LastName"] + ".txt"
    # Insert CV
    listbox.insert(END, file_path)

    with open(file_path, 'w') as file:
        file.write("Curriculum Vitae \n \n")
        file.write("First-Name : " + Person[-1]["FirstName"] + "\n")
        file.write("Last-Name : " + Person[-1]["LastName"] + "\n")
        file.write("Address : " + "\n")
        file.write("    Street Name : " + Person[-1]["StreetName"] + "\n")
        file.write("    House Number : " + Person[-1]["HouseNumber"] + "\n")
        file.write("    City : " + Person[-1]["City"] + "\n")
        file.write("    Country : " + Person[-1]["Country"] + "\n")
        file.write("Telephone Number : " + Person[-1]["TelephoneNumber"] + "\n")
        file.write("E-mail Address : " + Person[-1]["E-mailAddress"] + "\n\n")
        file.write("Sex : " + Person[-1]["Sex"] + "\n")
        file.write("Date of Birth : " + Person[-1]["DateOfBirth"] + "\n")
        file.write("Nationality : " + Person[-1]["Nationality"] + "\n\n")
        file.write("Work Experience : " + "\n")
        file.write("    Workplace 1 : " + Person[-1]["Workplace1"] + "\n")
        file.write("        Dates : " + Person[-1]["Dates1"] + "\n")
        file.write("        Occupation : " + Person[-1]["Occupation1"] + "\n")
        file.write("        Main activities : " + Person[-1]["MainActivities1"] + "\n")
        file.write("    Workplace 2 : " + Person[-1]["Workplace2"] + "\n")
        file.write("        Dates : " + Person[-1]["Dates2"] + "\n")
        file.write("        Occupation : " + Person[-1]["Occupation2"] + "\n")
        file.write("        Main activities : " + Person[-1]["MainActivities2"] + "\n")
        file.write("    Workplace 3 : " + Person[-1]["Workplace3"]+ "\n")
        file.write("        Dates : " + Person[-1]["Dates3"] + "\n")
        file.write("        Occupation : " + Person[-1]["Occupation3"] + "\n")
        file.write("        Main activities : " + Person[-1]["MainActivities3"] + "\n\n")
        file.write("Education and Training : " + "\n")
        file.write("    High school : " + Person[-1]["HighSchool"] + "\n")
        file.write("    College/University : " + Person[-1]["College"] + "\n")
        file.write("        Subjects studied : " + Person[-1]["SubjectsStudied"] + "\n")
        file.write("        Years studied : " + Person[-1]["YearsStudied"] + "\n")
        file.write("    Qualifications awarded : " + Person[-1]["QualificationsAwarded"] + "\n")
        file.write("    Master 1 : " + Person[-1]["Master1"] + "\n")
        file.write("    Master 2 : " + Person[-1]["Master2"] + "\n\n")
        file.write("Personal Skills : " + "\n")
        file.write("    Communication skills : " + Person[-1]["CommunicationSkills"] + "\n")
        file.write("    Organizational / managerial skills : " + Person[-1]["OrganizationalManagerialSkills"] + "\n")
        file.write("    Job-related skills : " + Person[-1]["JobRelatedSkills"] + "\n")
        file.write("    Computer skills : " + Person[-1]["ComputerSkills"] + "\n")
        file.write("    Other skills : " + Person[-1]["OtherSkills"] + "\n")
        file.write("    Driving License : " + Person[-1]["DrivingLicense"] + "\n\n")
        file.write("Languages : " + "\n")
        file.write("    Mother Language : " + Person[-1]["MotherLanguage"] + "\n")
        file.write("    Other Languages : " + "\n")
        file.write("        Modern Language 1 : " + Person[-1]["ModernLanguage1"] + "\n")
        file.write("            Level 1 : " + Person[-1]["Level1"] + "\n")
        file.write("        Modern Language 2 : " + Person[-1]["ModernLanguage2"]+ "\n")
        file.write("            Level 2 : " + Person[-1]["Level2"] + "\n\n")
        file.write("Additional Information : " + "\n")
        file.write("    Publications : " + Person[-1]["Publicaions"] + "\n")
        file.write("    Presentations : " + Person[-1]["Presentations"] + "\n")
        file.write("    Projects : " + Person[-1]["Projects"] + "\n")
        file.write("    Conferences : " + Person[-1]["Conferences"] + "\n")
        file.write("    Honours and awards : " + Person[-1]["HonoursAndAwards"] + "\n")
        file.write("    Memberships : " + Person[-1]["Memberships"] + "\n\n")
        file.write("Short Description : " + Person[-1]["ShortDescription"] + "\n\n")
        file.write("Hobbies : " + Person[-1]["Hobbies"] + "\n\n")


def WindowCV():
    CV = Toplevel(window)
    CV.title("New CV")
    CV.configure(bg='white')
    CV.state("zoomed")
    #CV.geometry("1400x800")

    entrydata.clear()

    # Read EntryData + Close CV Window + Make CV Txt
    def UploadCV():
        CVData = {
            "FirstName": entrydata[0].get(),
            "LastName": entrydata[1].get(),
            "StreetName": entrydata[2].get(),
            "HouseNumber": entrydata[3].get(),
            "City": entrydata[4].get(),
            "Country": entrydata[5].get(),
            "TelephoneNumber": entrydata[6].get(),
            "EmailAddress": entrydata[7].get(),
            "Sex": entrydata[8].get(),
            "Date0fBirth": entrydata[9].get(),
            "Nationality": entrydata[10].get(),
            "Workplace1": entrydata[11].get(),
            "Dates1": entrydata[12].get(),
            "Occupation1": entrydata[13].get(),
            "MainActivities1": entrydata[14].get(),
            "Workplace2": entrydata[15].get(),
            "Dates2": entrydata[16].get(),
            "Occupation2": entrydata[17].get(),
            "MainActivities2": entrydata[18].get(),
            "Workplace3": entrydata[19].get(),
            "Dates3": entrydata[20].get(),
            "Occupation3": entrydata[21].get(),
            "MainActivities3": entrydata[22].get(),
            "HighSchool": entrydata[23].get(),
            "College/University": entrydata[24].get(),
            "SubjectsStudied": entrydata[25].get(),
            "YearsStudied": entrydata[26].get(),
            "QualificationsAwarded": entrydata[27].get(),
            "Master1": entrydata[28].get(),
            "Master2": entrydata[29].get(),
            "CommunicationSkills": entrydata[30].get(),
            "OrganizationalManagerialSkills": entrydata[31].get(),
            "JobRelatedSkills": entrydata[32].get(),
            "ComputerSkills": entrydata[33].get(),
            "OtherSkills": entrydata[34].get(),
            "DrivingLicense": entrydata[35].get(),
            "MotherLanguage": entrydata[36].get(),
            "ModernLanguage1": entrydata[37].get(),
            "Level1": entrydata[38].get(),
            "ModernLanguage2": entrydata[39].get(),
            "Level2": entrydata[40].get(),
            "Publications": entrydata[41].get(),
            "Presentations": entrydata[42].get(),
            "Projects": entrydata[43].get(),
            "Conferences": entrydata[44].get(),
            "HonoursAndAwards": entrydata[45].get(),
            "Memberships": entrydata[46].get(),
            "ShortDescription": entrydata[47].get(),
            "Hobbies": entrydata[48].get(),
            "PersonalityTypeMB": "",
            "PersonalityTypeBF": ""
        }
        Person.append(CVData)
        CV.destroy()
        MakeCV()
        """filepath = person[l].Name.firstname + person[l].Name.lastname + ".txt"
        file.append(str(l + 1))
        listbox.insert(END, filepath)"""

    # Scroll with Mouse
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def bind_to_mousewheel(event):
        canvas.bind_all("<MouseWheel>", on_mousewheel)

    def unbind_from_mousewheel(event):
        canvas.unbind_all("<MouseWheel>")

    # Frame of the whole CV window
    frame_window = Frame(CV, bg="indianred")
    frame_window.rowconfigure(0, weight=1)
    frame_window.columnconfigure(0, weight=1)
    frame_window.pack(expand=True, fill=BOTH)

    # Canvas + Scrollbar
    canvas = Canvas(frame_window, bg="firebrick")
    canvas.grid(row=0, column=0, sticky='nwes')
    scrollbar = Scrollbar(frame_window, orient="vertical", command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky='ns')

    # Frame in Canvas
    frame = Frame(canvas, relief="groove", bg="palegoldenrod")

    # Frames in the Main Frame
    # Frame of the Title
    frame_title = Frame(frame, bg="darkgray", height=200)
    frame_title.pack(side=TOP, fill=BOTH, expand=True)
    label = Label(frame_title, text="Curriculum Vitae", bg="slategray", fg="white", height=1,
                  font=('helvetica', 26, "bold", "underline"))
    label.place(relx=0.5, rely=0.1, anchor='n')

    # Frame of the CV
    frame_CV = Frame(frame, relief="groove", bg="palegoldenrod")
    frame_CV.pack(side=TOP, fill=BOTH, expand=True)

    # Frame of the Bottom
    frame_bottom = Frame(frame, bg="orange", height=300)
    frame_bottom.pack(side=BOTTOM, fill=BOTH, expand=True)
    button_upload = Button(frame_bottom, text="Upload CV", command=UploadCV,
                           bg="saddlebrown", fg="white", activebackground="sandybrown", activeforeground="white",
                           height=3, width=10, font=('calibre', 20))
    button_upload.place(relx=0.5,  rely=0.5, anchor=CENTER)

    canvas.columnconfigure(0, weight=1)
    canvas.rowconfigure(0, weight=1)
    frame_CV.columnconfigure(0, weight=1)
    frame_CV.columnconfigure(1, weight=1)
    frame_CV.columnconfigure(2, weight=1)
    frame_CV.columnconfigure(3, weight=1)
    frame_CV.columnconfigure(4, weight=1)
    frame_CV.columnconfigure(5, weight=1)
    frame_CV.columnconfigure(6, weight=1)
    frame_CV.columnconfigure(7, weight=1)
    frame_CV.columnconfigure(8, weight=1)

    canvas.create_window((0, 0), window=frame, anchor='nw')

    # Make the Labels and Entries
    MakeLabelCV(frame_CV, "First-Name : ", 0, 0, 25)
    MakeLabelCV(frame_CV, "Last-Name : ", 1, 0, 25)
    MakeLabelCV(frame_CV, "Address : ", 2, 0, 0)
    MakeLabelCV(frame_CV, "Street Name : ", 3, 1, 60)
    MakeLabelCV(frame_CV, "House Number : ", 4, 1, 10)
    MakeLabelCV(frame_CV, "City : ", 5, 1, 30)
    MakeLabelCV(frame_CV, "Country : ", 6, 1, 30)
    MakeLabelCV(frame_CV, "Telephone Number : ", 7, 0, 25)
    MakeLabelCV(frame_CV, "E-mail Address : ", 8, 0, 25)
    MakeLabelCV(frame_CV, "Sex : ", 9, 0, 10)
    MakeLabelCV(frame_CV, "Date of Birth : ", 10, 0, 20)
    MakeLabelCV(frame_CV, "Nationality : ", 11, 0, 20)
    MakeLabelCV(frame_CV, "Work Experience : ", 12, 0, 0)
    MakeLabelCV(frame_CV, "Workplace 1 : ", 13, 1, 40)
    MakeLabelCV(frame_CV, "Dates : ", 14, 2, 20)
    MakeLabelCV(frame_CV, "Occupation : ", 15, 2, 40)
    MakeLabelCV(frame_CV, "Main activities : ", 16, 2, 50)
    MakeLabelCV(frame_CV, "Workplace 2 : ", 17, 1, 40)
    MakeLabelCV(frame_CV, "Dates : ", 18, 2, 20)
    MakeLabelCV(frame_CV, "Occupation : ", 19, 2, 40)
    MakeLabelCV(frame_CV, "Main activities : ", 20, 2, 50)
    MakeLabelCV(frame_CV, "Workplace 3 : ", 21, 1, 40)
    MakeLabelCV(frame_CV, "Dates : ", 22, 2, 20)
    MakeLabelCV(frame_CV, "Occupation : ", 23, 2, 40)
    MakeLabelCV(frame_CV, "Main activities : ", 24, 2, 50)
    MakeLabelCV(frame_CV, "Education and Training : ", 25, 0, 0)
    MakeLabelCV(frame_CV, "High school : ", 26, 1, 40)
    MakeLabelCV(frame_CV, "College/University : ", 27, 1, 40)
    MakeLabelCV(frame_CV, "Subjects studied : ", 28, 1, 50)
    MakeLabelCV(frame_CV, "Years studied : ", 29, 1, 50)
    MakeLabelCV(frame_CV, "Qualifications awarded : ", 30, 1, 50)
    MakeLabelCV(frame_CV, "Master 1 : ", 31, 1, 50)
    MakeLabelCV(frame_CV, "Master 2 : ", 32, 1, 50)
    MakeLabelCV(frame_CV, "Personal Skills : ", 33, 0, 0)
    MakeLabelCV(frame_CV, "Communication skills : ", 34, 1, 60)
    MakeLabelCV(frame_CV, "Organizational / managerial skills : ", 35, 1, 60)
    MakeLabelCV(frame_CV, "Job-related skills : ", 36, 1, 60)
    MakeLabelCV(frame_CV, "Computer skills : ", 37, 1, 60)
    MakeLabelCV(frame_CV, "Other skills : ", 38, 1, 60)
    MakeLabelCV(frame_CV, "Driving license : ", 39, 1, 15)
    MakeLabelCV(frame_CV, "Languages : ", 40, 0, 0)
    MakeLabelCV(frame_CV, "Mother Language : ", 41, 1, 30)
    MakeLabelCV(frame_CV, "Other Languages : ", 42, 1, 0)
    MakeLabelCV(frame_CV, "Modern Language 1 : ", 43, 2, 30)
    MakeLabelCV(frame_CV, "Level1 : ", 44, 3, 10)
    MakeLabelCV(frame_CV, "Modern Language 2 : ", 45, 2, 30)
    MakeLabelCV(frame_CV, "Level2 : ", 46, 3, 10)
    MakeLabelCV(frame_CV, "Additional Information: ", 47, 0, 0)
    MakeLabelCV(frame_CV, "Publications : ", 48, 1, 60)
    MakeLabelCV(frame_CV, "Presentations : ", 49, 1, 60)
    MakeLabelCV(frame_CV, "Projects : ", 50, 1, 60)
    MakeLabelCV(frame_CV, "Conferences : ", 51, 1, 60)
    MakeLabelCV(frame_CV, "Honours and awards : ", 52, 1, 60)
    MakeLabelCV(frame_CV, "Memberships : ", 53, 1, 60)
    MakeLabelCV(frame_CV, "Short Description : ", 54, 0, 100)
    MakeLabelCV(frame_CV, "Hobbies : ", 55, 0, 100)

    frame.update_idletasks()
    canvas.configure(yscrollcommand=scrollbar.set,
                     scrollregion=canvas.bbox("all"))
    canvas.bind("<Enter>", bind_to_mousewheel)
    canvas.bind("<Leave>", unbind_from_mousewheel)


def ApplyData():
    global pressed
    pressed = 1

def SelectData():
    # New Window Data
    data = Toplevel(window)
    data.title("Select Data")
    data.configure(bg='snow')
    data_width = 900
    data_height = 400
    position_right = int(data.winfo_screenwidth()/2 - data_width/2)
    position_down = int(data.winfo_screenheight()/2 - data_height/2)
    data.geometry("900x400+{}+{}".format(position_right, position_down))

    entrycriteria.clear()

    # Label Text
    label_text = Label(data, text="Choose the criteria in which the candidates should fit.",
                       bg="lawngreen", fg="black", font=('calibre', 16))
    label_text.place(relx=0.5, rely=0.1, anchor=CENTER)

    # Nationality
    name = StringVar()
    entrycriteria.append(name)
    label_nationality = Label(data, text="Nationalities:", bg="darkslategray", fg="white", font=('calibre', 14))
    label_nationality.place(relx=0.1, rely=0.225)
    entry_nationality = Entry(data, textvariable=name, bg="thistle", fg="black", width=40, font=('calibre', 14))
    entry_nationality.place(relx=0.26, rely=0.225)

    # Age
    name = StringVar()
    entrycriteria.append(name)
    label_age1 = Label(data, text="Between:", bg="darkslategray", fg="white", font=('calibre', 14))
    label_age1.place(relx=0.1, rely=0.35)
    entry_age1 = Entry(data, textvariable=name, bg="thistle", fg="black", width=5, font=('calibre', 14))
    entry_age1.place(relx=0.23, rely=0.35)
    name = StringVar()
    entrycriteria.append(name)
    label_age2 = Label(data, text="and", bg="darkslategray", fg="white", font=('calibre', 14))
    label_age2.place(relx=0.33, rely=0.35)
    entry_age2 = Entry(data, textvariable=name, bg="thistle", fg="black", width=5, font=('calibre', 14))
    entry_age2.place(relx=0.41, rely=0.35)
    label_age3 = Label(data, text="years", bg="darkslategray", fg="white", font=('calibre', 14))
    label_age3.place(relx=0.51, rely=0.35)

    # Sex
    name = StringVar()
    entrycriteria.append(name)
    label_sex = Label(data, text="Sex:", bg="darkslategray", fg="white", font=('calibre', 14))
    label_sex.place(relx=0.1, rely=0.475)
    entry_sex = Entry(data, textvariable=name, bg="thistle", fg="black", width=5, font=('calibre', 14))
    entry_sex.place(relx=0.18, rely=0.475)

    # Experience
    name = StringVar()
    entrycriteria.append(name)
    label_experience1 = Label(data, text="Minimum experience:", bg="darkslategray", fg="white", font=('calibre', 14))
    label_experience1.place(relx=0.1, rely=0.6)
    entry_experience1 = Entry(data, textvariable=name, bg="thistle", fg="black", width=5, font=('calibre', 14))
    entry_experience1.place(relx=0.36, rely=0.6)
    label_experience2 = Label(data, text="years", bg="darkslategray", fg="white", font=('calibre', 14))
    label_experience2.place(relx=0.45, rely=0.6)

    # Skills
    name = StringVar()
    entrycriteria.append(name)
    label_skills = Label(data, text="Skills:", bg="darkslategray", fg="white", font=('calibre', 14))
    label_skills.place(relx=0.1, rely=0.725)
    entry_skills = Entry(data, textvariable=name, bg="thistle", fg="black", width=50, font=('calibre', 14))
    entry_skills.place(relx=0.19, rely=0.725)

    # Languages
    name = StringVar()
    entrycriteria.append(name)
    label_languages = Label(data, text="Languages:", bg="darkslategray", fg="white", font=('calibre', 14))
    label_languages.place(relx=0.1, rely=0.85)
    entry_languages = Entry(data, textvariable=name, bg="thistle", fg="black", width=50, font=('calibre', 14))
    entry_languages.place(relx=0.25, rely=0.85)

    # Button Apply
    button_apply = Button(data, text="Apply", command=ApplyData,
                          bg="royalblue", fg="white", activebackground="cornflowerblue", activeforeground="white",
                          height=1, width=10, font=('calibre', 20))
    button_apply.place(relx=0.8, rely=0.5, anchor=CENTER)

def OpenShowList():
    List = Toplevel(window)
    List.title("Results of the Analyze")
    List.configure(bg="dimgray")
    List.state("zoomed")

    CandidatesList = AnalyzeData()
    nr = 0
    max_nr = 5

    # Title List
    label_title = Label(List, text="List of Candidates", bg="silver", fg="white", font=('calibre', 26, 'bold'))
    label_title.place(relx=0.5, rely=0.1, anchor=S)

    # Candidates List
    """label_jobs = Label(List, text="", bg="gainsboro", fg="black", font=('calibre', 18))
    label_jobs.place(relx=0.28, rely=0.26)"""
    """listbox_jobs = Listbox(Jobs, height=20, width=60, selectmode="extended", fg="black", font=('calibre', 14))
    listbox_jobs.place(relx=0.28, rely=0.3)"""
    style = ttk.Style()
    style.configure("Treeview.Heading", font=('calibre', 16, 'bold'))
    style.configure("Treeview", font=('calibre', 14))
    treeview = ttk.Treeview(List, columns=("candidate", "points"), show='headings', height=20, selectmode="extended")
    treeview.place(relx=0.28, rely=0.3)
    treeview.heading("candidate", text="Candidate Name")
    treeview.heading("points", text="Points")
    treeview.column("# 1", anchor=CENTER, width=400, stretch=NO)
    treeview.column("# 2", anchor=CENTER, width=400, stretch=NO)

    print(CandidatesList)
    for person in range(len(CandidatesList)):
        nr += 1
        treeview.insert('', END, values=(str(nr) + ". " + Person[person]["FirstName"] + " " + Person[person]["LastName"],  int(Person[person]["Score"])))
        # listbox_jobs.insert(END, str(nr) + " " + word[0])
        if(nr == max_nr):
            break


def AnalyzeData():
    sector = list_jobs.get(list_jobs.curselection())
    for person in range(len(Person)):
        Person[person]["Score"] = 0
        AnalyzePersonality(person)
        Person[person]["Score"] += AnalyzeJob(person, sector)
    List = sorted(Person, key=lambda ind: ind["PersonalityTypeMB"], reverse=True)
    return List



def ButtonAnalyzePressed():
    OpenShowList()
    AnalyzeData()
    jobchosen = job.get()
    global pressed
    if pressed == 1:
        nationality = entrycriteria[0].get
        age_min = entrycriteria[1].get
        age_max = entrycriteria[2].get
        sex = entrycriteria[3].get
        experience_years = entrycriteria[4].get
        skills = entrycriteria[5].get
        languages = entrycriteria[6].get
    pressed = 0


def ButtonMakePressed():
    WindowCV()


def OpenFile():
    filepath = askopenfilename(filetypes=[("Text Files", "*.txt")])
    if not filepath:
        return
    ReadFile(filepath)
    listbox.insert(END, filepath)


def RemoveFile(person):
    """indice = ""
    for item in selected_indice:
        indice = str(item)"""
    Person.pop(person)
    listbox.delete(person)

def OpenWebSite(url):
    webbrowser.open(url, new=1)


def OpenShowPersonality(person: int):
    Personality = Toplevel(window)
    Personality.title("Personality Type")
    Personality.configure(bg='midnightblue')
    Personality.state("zoomed")

    AnalyzePersonality(person)
    typeMB = Person[person]["PersonalityTypeMB"]
    typeBF = "conscientiousness"
    description = PersonalityTypes[typeMB]["Description"]
    website = PersonalityTypes[typeMB]["WebSite"]
    strengths = ""
    for word in PersonalityTypes[typeMB]["Strengths"]:
        strengths += word + ", "
    strengths_text = strengths[:-2]
    weaknesses = ""
    for word in PersonalityTypes[typeMB]["Weaknesses"]:
        weaknesses += word + ", "
    weaknesses_text = weaknesses[:-2]

    # Title Personality
    label_title = Label(Personality, text="Personality Analysis", bg="midnightblue", fg="white",
                        font=('calibre', 26, 'bold'))
    label_title.place(relx=0.5, rely=0.1, anchor=S)

    # Type Myers-Briggs
    label_text_MB = Label(Personality, text="Type of Personality by Myers-Briggs Test:", bg="lightsteelblue",
                          fg="black", font=('calibre', 18))
    label_text_MB.place(relx=0.1, rely=0.25)
    label_type_MB = Label(Personality, text=typeMB, bg="lightsteelblue",
                          fg="black", font=('calibre', 18))
    label_type_MB.place(relx=0.8, rely=0.25)

    # Type Big Five
    label_text_BF = Label(Personality, text="Type of Personality by Big Five Test:", bg="lightsteelblue", fg="black",
                          font=('calibre', 18))
    label_text_BF.place(relx=0.1, rely=0.35)
    label_type_BF = Label(Personality, text=typeBF, bg="lightsteelblue",
                          fg="black", font=('calibre', 18))
    label_type_BF.place(relx=0.8, rely=0.35)

    # Description
    label_description = Label(Personality, text="Description:", bg="lightsteelblue", fg="white", font=('calibre', 18))
    label_description.place(relx=0.1, rely=0.45)
    text_description = Text(Personality, height=5, width=90, bg="bisque", fg="black", font=('calibre', 16))
    text_description.place(relx=0.1, rely=0.50)
    text_description.insert(END, description)

    # Strengths and Weaknesses
    label_text_strengths = Label(Personality, text="Strengths:", bg="mediumorchid", fg="white", font=('calibre', 16))
    label_text_strengths.place(relx=0.1, rely=0.75)
    label_strengths = Label(Personality, text=strengths_text, bg="thistle", fg="black", font=('calibre', 16))
    label_strengths.place(relx=0.2, rely=0.75)
    label_text_weaknesses = Label(Personality, text="Weaknesses:", bg="mediumorchid", fg="white", font=('calibre', 16))
    label_text_weaknesses.place(relx=0.1, rely=0.8)
    label_weaknesses = Label(Personality, text=weaknesses_text, bg="thistle", fg="black", font=('calibre', 16))
    label_weaknesses.place(relx=0.2, rely=0.8)

    # WebSite
    label_website = Label(Personality, text="Website:", bg="lightyellow", fg="black", font=('calibre', 16))
    label_website.place(relx=0.1, rely=0.9)
    button_webpage = Button(Personality, text="Find More About Your Personality",
                            command=lambda url=website: OpenWebSite(url),
                            bg="salmon", fg="white", activebackground="lightsalmon", activeforeground="white",
                            height=1, width=40, font=('calibre', 16))
    button_webpage.place(relx=0.2, rely=0.9)

def OpenShowJobs(person):
    Jobs = Toplevel(window)
    Jobs.title("Suitable Jobs")
    Jobs.configure(bg="dimgray")
    Jobs.state("zoomed")

    JobList = AnalyzeJobs(person)
    nr = 0
    max_nr = 3

    # Title Job
    label_title = Label(Jobs, text="Jobs Analysis", bg="silver", fg="white", font=('calibre', 26, 'bold'))
    label_title.place(relx=0.5, rely=0.1, anchor=S)

    # Job List
    label_jobs = Label(Jobs, text="List of suitable jobs:", bg="gainsboro", fg="black", font=('calibre', 18))
    label_jobs.place(relx=0.28, rely=0.26)
    """listbox_jobs = Listbox(Jobs, height=20, width=60, selectmode="extended", fg="black", font=('calibre', 14))
    listbox_jobs.place(relx=0.28, rely=0.3)"""
    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Calibri', 16, 'bold'))
    style.configure("Treeview", font=('Calibri', 14))
    treeview_jobs = ttk.Treeview(Jobs, columns=("job", "score"), show='headings', height=20, selectmode="extended")
    treeview_jobs.place(relx=0.28, rely=0.3)
    treeview_jobs.heading("job", text="Job")
    treeview_jobs.heading("score", text="Score")
    treeview_jobs.column("# 1", anchor=CENTER, width=400, stretch=YES)
    treeview_jobs.column("# 2", anchor=CENTER, width=400, stretch=YES)

    for word in JobList:
        print(word)
        nr += 1
        treeview_jobs.insert('', END, values=(str(nr) + ". " + word[0], int(word[1])))
        # listbox_jobs.insert(END, str(nr) + " " + word[0])
        if(nr == max_nr):
            break


def ListAction(btn):
    selected_indice = listbox.curselection()
    person = int(''.join(map(str, selected_indice)))
    match btn:
        case "RemoveFile":
            RemoveFile(person)
        case "ShowJobs":
            OpenShowJobs(person)
        case "ShowPersonality":
            OpenShowPersonality(person)

def ShowList(list, relx, rely):
    list.place(relx=relx, rely=rely)"""

def ShowList(event):
    list_jobs.place(relx=0.5, rely=0.1, anchor=N)
def HideList(event):
    list_jobs.place_forget()
def ListboxSelect(event):
    domain = list_jobs.get(list_jobs.curselection())
    entry.delete(0, END)
    entry.insert(0, domain)
    HideList(event)

#####################################################################################################################################
#Window Elements

# Job applied
job = StringVar()
label_job = Label(window, text="Job applied:", bg="black", fg="white",
                  height=1, width=30, font=('calibre', 16))
label_job.place(relx=0.35, rely=0.1, anchor=S)
entry = Entry(window, textvariable=job, width=27, font=('calibre', 16))
entry.place(relx=0.5, rely=0.1, anchor=S)
# entry.focus_set()

joblist = []
list_jobs = Listbox(window, height=10, width=37, selectmode="extended", fg="black", font=('calibre', 12))
for sector in JobSectors:
    joblist.append(sector)
    list_jobs.insert(END, sector)
entry.bind('<Enter>', ShowList)
entry.bind('<Leave>', HideList)
list_jobs.bind('<Enter>', ShowList)
list_jobs.bind('<Leave>', HideList)
list_jobs.bind('<<ListboxSelect>>', ListboxSelect)

button_job = Button(window, text="Select Data", command=SelectData,
                    bg="indianred", fg="white", activebackground="lightcoral", activeforeground="white",
                    height=1, width=12, font=('calibre', 18))
button_job.place(relx=0.7, rely=0.1, anchor=CENTER)


# Buton Make CV
button_make = Button(window, text="Make CV", command=ButtonMakePressed,
                     bg="orange", fg="white", activebackground="wheat", activeforeground="white",
                     height=2, width=15, font=('calibre', 20))
button_make.place(relx=0.7, rely=0.22, anchor=CENTER)

# Button Choose File
button_file = Button(window, text="Choose File", command=OpenFile,
                     bg="purple", fg="white", activebackground="plum", activeforeground="white",
                     height=2, width=10, font=('calibre', 20))
button_file.place(relx=0.5, rely=0.4, anchor=CENTER)

# List of files
frame = Frame(window, relief="raised", bg="darkgray", width=600, height=300, padx=10, borderwidth=1)
frame.place(relx=0.5, rely=0.7, anchor=CENTER)
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)

listbox = Listbox(frame, height=15, width=60, selectmode="extended", fg="dodgerblue", font=('calibre', 12))
scrollbar = Scrollbar(frame, orient='vertical', command=listbox.yview)

listbox.config(yscrollcommand=scrollbar.set)
listbox.grid(column=0, row=0, sticky='nwes')
scrollbar.grid(column=1, row=0, sticky='ns')

# Button Analyze Data
button_analyze = Button(window, text="Analyze data", command=ButtonAnalyzePressed,
                        bg="teal", fg="white", activebackground="paleturquoise", activeforeground="white",
                        height=3, width=10, font=('calibre', 20))
button_analyze.place(relx=0.8, rely=0.7, anchor=CENTER)


# Button Remove
button_remove = Button(window, text="Remove", command=lambda btn="RemoveFile": ListAction(btn),
                       bg="sienna", fg="white", activebackground="rosybrown", activeforeground="white",
                       height=1, width=10, font=('calibre', 18))
button_remove.place(relx=0.36, rely=0.95, anchor=CENTER)

button_jobs = Button(window, text="Show Jobs", command=lambda btn="ShowJobs": ListAction(btn),
                     bg="darkgoldenrod", fg="white", activebackground="gold", activeforeground="white",
                     height=1, width=10, font=('calibre', 18))
button_jobs.place(relx=0.48, rely=0.95, anchor=CENTER)

button_personality = Button(window, text="Show Personality", command=lambda btn="ShowPersonality": ListAction(btn),
                            bg="paleturquoise", fg="black", activebackground="azure", activeforeground="black",
                            height=1, width=15, font=('calibre', 18))
button_personality.place(relx=0.62, rely=0.95, anchor=CENTER)


#####################################################################################################################################
# Finish



window.mainloop()