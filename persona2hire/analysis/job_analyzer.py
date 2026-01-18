"""Job analysis and matching algorithms."""

from datetime import date
from ..data.job_sectors import JobSectors
from ..data.constants import (
    Functions,
    Qualifications,
    Languages,
    LanguageLevels,
    Top50Universities,
    Top100Universities,
    SoftSkills,
)


def analyze_job(person: dict, sector: str) -> float:
    """
    Analyze a person's fit for a specific job sector.

    Args:
        person: Dictionary containing CV data
        sector: Job sector key from JobSectors

    Returns:
        Total score for the person-sector match
    """
    if sector not in JobSectors:
        return 0

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

    # Soft Skills Score
    soft_skills_score = _calculate_soft_skills_score(person)

    total_score = (
        job_score
        + work_score
        + skills_score
        + language_score
        + information_score
        + soft_skills_score
    )
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
        score = analyze_job(person, sector)
        job_list.append((sector, score))
    job_list.sort(key=lambda x: x[1], reverse=True)
    return job_list


def _calculate_education_score(person: dict, sector: str) -> float:
    """Calculate education-related score."""
    score = 0
    sector_data = JobSectors[sector]
    education_keywords = sector_data.get("School/College", [])

    # Years studied bonus
    try:
        years_studied = int(person.get("YearsStudied", 0) or 0)
    except (ValueError, TypeError):
        years_studied = 0

    # High school matching
    highschool = person.get("HighSchool", "").lower()
    highschool_matches = sum(1 for kw in education_keywords if kw.lower() in highschool)
    score += highschool_matches * 2

    # College/University
    college = person.get("College/University", "").lower()

    # University ranking bonus
    university_bonus = _get_university_bonus(college)
    score += university_bonus

    # Subject matching
    subjects = person.get("SubjectsStudied", "").lower()
    subject_matches = sum(1 for kw in education_keywords if kw.lower() in subjects)
    score += subject_matches * 3

    # Qualification level
    qualifications = person.get("QualificationsAwarded", "").lower()
    qual_level = _get_qualification_level(qualifications)
    score += qual_level * 5

    # Qualification keyword matches
    qual_matches = sum(1 for kw in education_keywords if kw.lower() in qualifications)
    score += qual_matches * 2

    # Master's degrees
    master1 = person.get("Master1", "").lower()
    master2 = person.get("Master2", "").lower()
    master_matches = sum(
        1 for kw in education_keywords if kw.lower() in master1 or kw.lower() in master2
    )
    score += master_matches * 4

    # If they have masters, add bonus
    if master1 or master2:
        score += 10

    # Apply years studied multiplier
    if years_studied > 0:
        score *= 1 + years_studied * 0.1

    return score


def _get_university_bonus(college_text: str) -> int:
    """Get bonus points based on university ranking."""
    college_lower = college_text.lower()

    # Check Top 50
    for uni_name in Top50Universities:
        if uni_name in college_lower:
            return 30  # Top 50 bonus

    # Check Top 100
    for uni_name in Top100Universities:
        if uni_name in college_lower:
            return 20  # Top 100 bonus

    # Generic university mention
    if "university" in college_lower or "college" in college_lower:
        return 10

    return 0


def _get_qualification_level(qualifications_text: str) -> int:
    """Get the highest qualification level from text."""
    max_level = 0
    qual_lower = qualifications_text.lower()

    for level, keywords in Qualifications.items():
        for keyword in keywords:
            if keyword.lower() in qual_lower:
                max_level = max(max_level, level)

    return max_level


def _calculate_work_score(person: dict, sector: str) -> float:
    """Calculate work experience score."""
    score = 0
    sector_data = JobSectors[sector]
    work_keywords = sector_data.get("WorkExperience", [])

    # Process each workplace (1-3)
    for i in range(1, 4):
        workplace = person.get(f"Workplace{i}", "")
        dates = person.get(f"Dates{i}", "")
        occupation = person.get(f"Occupation{i}", "")
        activities = person.get(f"MainActivities{i}", "")

        if not workplace:
            continue

        # Base score for having work experience
        workplace_score = 5

        # Calculate time worked
        time_worked = _calculate_time_worked(dates)

        # Get seniority level
        seniority = _get_seniority_level(occupation)

        # Keyword matching in workplace
        workplace_lower = workplace.lower()
        for kw in work_keywords:
            if kw.lower() in workplace_lower:
                workplace_score += 3

        # Keyword matching in occupation
        occupation_lower = occupation.lower()
        for kw in work_keywords:
            if kw.lower() in occupation_lower:
                workplace_score += 2

        # Keyword matching in activities
        activities_lower = activities.lower()
        for kw in work_keywords:
            if kw.lower() in activities_lower:
                workplace_score += 1

        # Apply multipliers
        time_multiplier = 1 + (time_worked * 0.2)  # 20% bonus per year
        seniority_multiplier = 1 + (seniority * 0.15)  # 15% bonus per seniority level

        score += workplace_score * time_multiplier * seniority_multiplier

    return score


def _calculate_time_worked(dates_str: str) -> float:
    """Calculate years worked from date range string."""
    if not dates_str or "-" not in dates_str:
        return 0

    try:
        dates = dates_str.split("-")
        date_start = dates[0].strip()
        date_finish = dates[1].strip()

        # Parse start date
        date_parts_start = date_start.split(".")
        if len(date_parts_start) >= 3:
            start_date = date(
                int(date_parts_start[2]),
                int(date_parts_start[1]),
                int(date_parts_start[0]),
            )
        else:
            return 0

        # Parse end date
        if date_finish.lower() in ["current", "present", "now", "ongoing"]:
            end_date = date.today()
        else:
            date_parts_end = date_finish.split(".")
            if len(date_parts_end) >= 3:
                end_date = date(
                    int(date_parts_end[2]),
                    int(date_parts_end[1]),
                    int(date_parts_end[0]),
                )
            else:
                end_date = date.today()

        return max(0, (end_date - start_date).days / 365)
    except (ValueError, IndexError):
        return 0


def _get_seniority_level(occupation_text: str) -> int:
    """Get seniority level from occupation text."""
    occupation_lower = occupation_text.lower()
    max_level = 0

    for level, keywords in Functions.items():
        for keyword in keywords:
            if keyword.lower() in occupation_lower:
                max_level = max(max_level, level)

    return max_level


def _calculate_language_score(person: dict) -> float:
    """Calculate language proficiency score."""
    score = 0

    # Mother language
    mother_language = person.get("MotherLanguage", "").lower()
    mother_value = _get_language_value(mother_language)
    score += mother_value * 3  # Native language is more valuable

    # Additional languages
    for i in range(1, 3):
        language = person.get(f"ModernLanguage{i}", "").lower()
        level = person.get(f"Level{i}", "").lower().strip()

        if language:
            lang_value = _get_language_value(language)
            level_score = _get_level_score(level)
            score += lang_value * level_score * 0.5

    return score


def _get_language_value(language: str) -> int:
    """Get the business value of a language."""
    language_lower = language.lower()

    for tier, languages in Languages.items():
        if language_lower in [l.lower() for l in languages]:
            return tier * 2

    return 1  # Default for unknown languages


def _get_level_score(level: str) -> int:
    """Convert language level to numeric score."""
    level_lower = level.lower().strip()

    if level_lower in LanguageLevels:
        return LanguageLevels[level_lower]["score"]

    # Try to match partial strings
    for level_key, level_data in LanguageLevels.items():
        if level_key in level_lower or level_lower in level_key:
            return level_data["score"]

    return 1  # Default


def _calculate_skills_score(person: dict, sector: str) -> float:
    """Calculate skills matching score."""
    score = 0
    sector_data = JobSectors[sector]
    required_skills = sector_data.get("Skills", [])
    extra_skills = sector_data.get("ExtraSkills", [])

    # Gather all person's skills
    all_skills = []
    for field in [
        "CommunicationSkills",
        "OrganizationalManagerialSkills",
        "JobRelatedSkills",
        "ComputerSkills",
        "OtherSkills",
    ]:
        skills_text = person.get(field, "").lower()
        all_skills.extend([s.strip() for s in skills_text.split(",") if s.strip()])

    # Match required skills
    for skill in required_skills:
        skill_lower = skill.lower()
        for person_skill in all_skills:
            if skill_lower in person_skill or person_skill in skill_lower:
                score += 5
                break

    # Match extra skills (lower weight)
    for skill in extra_skills:
        skill_lower = skill.lower()
        for person_skill in all_skills:
            if skill_lower in person_skill or person_skill in skill_lower:
                score += 2.5
                break

    # Driving license bonus
    driving = person.get("DrivingLicense", "").lower()
    if driving and driving not in ["no", "none", ""]:
        score += 5

    return score


def _calculate_soft_skills_score(person: dict) -> float:
    """Calculate soft skills score based on descriptions and skills."""
    score = 0

    # Gather text to analyze
    description = person.get("ShortDescription", "").lower()
    comm_skills = person.get("CommunicationSkills", "").lower()
    org_skills = person.get("OrganizationalManagerialSkills", "").lower()

    all_text = f"{description} {comm_skills} {org_skills}"

    # Check for soft skills categories
    for category, keywords in SoftSkills.items():
        matches = sum(1 for kw in keywords if kw.lower() in all_text)
        score += matches * 2

    return score


def _calculate_information_score(person: dict) -> float:
    """Calculate additional information score."""
    score = 0

    # Publications (highly valued)
    publications = person.get("Publications", "")
    if publications and publications.strip():
        pub_count = publications.count(",") + 1
        score += pub_count * 5

    # Presentations
    presentations = person.get("Presentations", "")
    if presentations and presentations.strip():
        pres_count = presentations.count(",") + 1
        score += pres_count * 3

    # Projects
    projects = person.get("Projects", "")
    if projects and projects.strip():
        proj_count = projects.count(",") + 1
        score += proj_count * 3

    # Conferences
    conferences = person.get("Conferences", "")
    if conferences and conferences.strip():
        conf_count = conferences.count(",") + 1
        score += conf_count * 2

    # Honours and Awards (highly valued)
    awards = person.get("HonoursAndAwards", "")
    if awards and awards.strip():
        award_count = awards.count(",") + 1
        score += award_count * 6

    # Memberships
    memberships = person.get("Memberships", "")
    if memberships and memberships.strip():
        member_count = memberships.count(",") + 1
        score += member_count * 2

    return score
