"""Job analysis and matching algorithms."""

from datetime import date
from ..data.job_sectors import JobSectors
from ..data.constants import Functions, Qualifications, Languages, Top50Universities, Top100Universities


def analyze_job(person: dict, sector: str) -> float:
    """
    Analyze a person's fit for a specific job sector.
    
    Args:
        person: Dictionary containing CV data
        sector: Job sector key from JobSectors
        
    Returns:
        Total score for the person-sector match
    """
    # Education Score
    job_score = _calculate_education_score(person, sector)
    
    # Work Experience Score
    work_score = _calculate_work_score(person, sector)
    
    # Language Score
    language_score = _calculate_language_score(person)
    
    # Skills Score
    skills_score = _calculate_skills_score(person, sector)
    
    # Additional Information Score
    information_score = _calculate_information_score(person)
    
    # Personality Score (placeholder for future implementation)
    personality_score = 0
    
    total_score = job_score + work_score + skills_score + language_score + information_score + personality_score
    return total_score


def analyze_jobs(person: dict) -> list:
    """
    Analyze a person's fit for all job sectors.
    
    Args:
        person: Dictionary containing CV data
        
    Returns:
        List of (sector, score) tuples sorted by score descending
    """
    job_list = []
    for sector in JobSectors:
        pair = (sector, analyze_job(person, sector))
        job_list.append(pair)
    job_list.sort(key=lambda x: x[1], reverse=True)
    return job_list


def _calculate_education_score(person: dict, sector: str) -> float:
    """Calculate education-related score."""
    highschool_score = 0
    subjects_score = 0
    college_university_score = 0
    qualification_word_score = 0
    qualification_level_score = 1
    master_score = 0
    
    years_studied = int(person.get("YearsStudied", 0) or 0)
    
    # High school matching
    highschool = person.get("HighSchool", "").lower().split(" ")
    for word in highschool:
        if word in JobSectors[sector]["School/College"]:
            highschool_score += 1
    
    # Subjects matching
    subjects = person.get("SubjectsStudied", "").lower().split(",")
    for word in subjects:
        if word.strip() in JobSectors[sector]["School/College"]:
            subjects_score += 1
    
    # Qualifications matching
    qualifications = person.get("QualificationsAwarded", "").lower().split(",")
    for word in qualifications:
        word = word.strip()
        if word in JobSectors[sector]["School/College"]:
            qualification_word_score += 1
        for value in Qualifications:
            if word in Qualifications[value]:
                qualification_level_score += value
    
    # Master's degrees
    master1 = person.get("Master1", "").lower().split(" ")
    for word in master1:
        if word in JobSectors[sector]["School/College"]:
            master_score += 1
    
    master2 = person.get("Master2", "").lower().split(" ")
    for word in master2:
        if word in JobSectors[sector]["School/College"]:
            master_score += 1
    
    # College/University scoring
    college_university = person.get("College/University", "").lower()
    college_nr = college_university.count("college") + college_university.count("university")
    subjects_nr = person.get("SubjectsStudied", "").lower().count(",") + 1
    
    # University ranking bonus
    if college_university in Top50Universities:
        rank = 3
    elif college_university in Top100Universities:
        rank = 2
    else:
        rank = 1
    
    if college_nr != 0:
        college_university_score += college_nr * 5 * rank
        college_university_score += subjects_score * 3 + (subjects_nr - subjects_score)
    
    # Calculate final job score
    job_score = 0
    if highschool_score == 1:
        job_score += 3
    elif highschool_score > 1:
        job_score += 6
    
    job_score += (college_university_score * years_studied + 
                  qualification_word_score * qualification_level_score * 2 + 
                  master_score)
    
    return job_score


def _calculate_work_score(person: dict, sector: str) -> float:
    """Calculate work experience score."""
    work_score = 0
    
    # Process each workplace
    for i in range(1, 4):
        workplace_key = f"Workplace{i}"
        dates_key = f"Dates{i}"
        occupation_key = f"Occupation{i}"
        activities_key = f"MainActivities{i}"
        
        if not person.get(workplace_key):
            continue
        
        workscore = 2  # Base score for having a workplace
        function_score = 1
        
        # Calculate time worked
        time_worked = _calculate_time_worked(person.get(dates_key, ""))
        
        # Workplace name matching
        workplace = person.get(workplace_key, "").lower().split(" ")
        for word in workplace:
            word = word.replace(",", "")
            if word in JobSectors[sector]["WorkExperience"]:
                workscore += 3
        
        # Occupation matching
        occupation = person.get(occupation_key, "").lower().split(",")
        for word in occupation:
            word = word.strip()
            if word in JobSectors[sector]["WorkExperience"]:
                workscore += 1
            # Check function level
            for value in Functions:
                if word in Functions[value]:
                    function_score = max(function_score, value + 1)
        
        # Main activities matching
        main_activities = person.get(activities_key, "").lower().split(",")
        for word in main_activities:
            if word.strip() in JobSectors[sector]["WorkExperience"]:
                workscore += 0.5
        
        work_score += workscore * function_score * time_worked
    
    return work_score


def _calculate_time_worked(dates_str: str) -> float:
    """Calculate years worked from date range string."""
    if not dates_str or "-" not in dates_str:
        return 0
    
    try:
        dates = dates_str.split("-")
        date_start = dates[0].strip()
        date_finish = dates[1].strip()
        
        date_parts_start = date_start.split(".")
        start_date = date(int(date_parts_start[2]), int(date_parts_start[1]), int(date_parts_start[0]))
        
        if date_finish.lower() == "current":
            end_date = date.today()
        else:
            date_parts_end = date_finish.split(".")
            end_date = date(int(date_parts_end[2]), int(date_parts_end[1]), int(date_parts_end[0]))
        
        return (end_date - start_date).days / 365
    except (ValueError, IndexError):
        return 0


def _calculate_language_score(person: dict) -> float:
    """Calculate language proficiency score."""
    language_mother_score = 0
    language_modern_score = 0
    
    mother_language = person.get("MotherLanguage", "").lower()
    modern_language1 = person.get("ModernLanguage1", "").lower()
    modern_language2 = person.get("ModernLanguage2", "").lower()
    
    for value in Languages:
        if mother_language in Languages[value]:
            language_mother_score += value
        
        if modern_language1 in Languages[value]:
            level1 = _get_language_level(person.get("Level1", ""))
            language_modern_score += value * level1
        
        if modern_language2 in Languages[value]:
            level2 = _get_language_level(person.get("Level2", ""))
            language_modern_score += value * level2
    
    return language_mother_score + language_modern_score


def _get_language_level(level_str: str) -> int:
    """Convert language level string to numeric value."""
    level_map = {"a1": 1, "a2": 2, "b1": 3, "b2": 4, "c1": 5, "c2": 6}
    return level_map.get(level_str.lower().strip(), 1)


def _calculate_skills_score(person: dict, sector: str) -> float:
    """Calculate skills matching score."""
    related_skills_score = 0
    extra_skills_score = 0
    
    communication_skills = [s.strip() for s in person.get("CommunicationSkills", "").lower().split(",")]
    organizational_skills = [s.strip() for s in person.get("OrganizationalManagerialSkills", "").lower().split(",")]
    job_skills = [s.strip() for s in person.get("JobRelatedSkills", "").lower().split(",")]
    computer_skills = [s.strip() for s in person.get("ComputerSkills", "").lower().split(",")]
    other_skills = [s.strip() for s in person.get("OtherSkills", "").lower().split(",")]
    
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
    
    # Driving license bonus
    driving_skills = 4 if person.get("DrivingLicense") else 0
    
    return related_skills_score * 5 + extra_skills_score * 2.5 + driving_skills


def _calculate_information_score(person: dict) -> float:
    """Calculate additional information score."""
    info_score = 0
    info_score += (person.get("Publications", "").count(",") + 1) * 2
    info_score += (person.get("Presentations", "").count(",") + 1) * 2
    info_score += (person.get("Projects", "").count(",") + 1) * 2
    info_score += (person.get("Conferences", "").count(",") + 1) * 2
    info_score += (person.get("HonoursAndAwards", "").count(",") + 1) * 3
    info_score += (person.get("Memberships", "").count(",") + 1) * 3
    return info_score
