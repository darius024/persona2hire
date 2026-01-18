"""Job analysis and matching algorithms."""

from datetime import date
from typing import Optional

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


# Scoring weights - these determine how much each category contributes to total score
# All weights should sum to approximately 100 for a perfect candidate
WEIGHTS = {
    "education": 25,  # Max 25 points for education
    "work_experience": 30,  # Max 30 points for work experience
    "skills": 20,  # Max 20 points for skills match
    "languages": 10,  # Max 10 points for languages
    "soft_skills": 10,  # Max 10 points for soft skills
    "additional": 5,  # Max 5 points for publications, awards, etc.
}


def analyze_job(person: dict, sector: str) -> float:
    """
    Analyze a person's fit for a specific job sector.

    Args:
        person: Dictionary containing CV data
        sector: Job sector key from JobSectors

    Returns:
        Total score for the person-sector match (0-100 scale)
    """
    if sector not in JobSectors:
        return 0.0

    # Calculate normalized scores for each category
    education_score = _calculate_education_score(person, sector)
    work_score = _calculate_work_score(person, sector)
    skills_score = _calculate_skills_score(person, sector)
    language_score = _calculate_language_score(person)
    soft_skills_score = _calculate_soft_skills_score(person)
    additional_score = _calculate_additional_score(person)

    # Sum all scores (each is already weighted)
    total_score = (
        education_score
        + work_score
        + skills_score
        + language_score
        + soft_skills_score
        + additional_score
    )

    return round(total_score, 1)


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


def get_score_breakdown(person: dict, sector: str) -> dict:
    """
    Get a detailed breakdown of the scoring for a person-sector match.

    Args:
        person: Dictionary containing CV data
        sector: Job sector key from JobSectors

    Returns:
        Dictionary with scores for each category
    """
    if sector not in JobSectors:
        return {}

    return {
        "education": _calculate_education_score(person, sector),
        "work_experience": _calculate_work_score(person, sector),
        "skills": _calculate_skills_score(person, sector),
        "languages": _calculate_language_score(person),
        "soft_skills": _calculate_soft_skills_score(person),
        "additional": _calculate_additional_score(person),
        "max_education": WEIGHTS["education"],
        "max_work_experience": WEIGHTS["work_experience"],
        "max_skills": WEIGHTS["skills"],
        "max_languages": WEIGHTS["languages"],
        "max_soft_skills": WEIGHTS["soft_skills"],
        "max_additional": WEIGHTS["additional"],
    }


def _calculate_education_score(person: dict, sector: str) -> float:
    """
    Calculate education-related score (0 to WEIGHTS['education']).

    Scoring breakdown:
    - Qualification level: 0-10 points (scaled by level 0-6)
    - Subject/field match: 0-10 points
    - University prestige: 0-5 points
    """
    max_score = WEIGHTS["education"]
    raw_score = 0.0

    sector_data = JobSectors[sector]
    education_keywords = sector_data.get("School/College", [])
    education_keywords_lower = [kw.lower() for kw in education_keywords]

    # Qualification level (0-10 points, scaled from 0-6 levels)
    qualifications = _safe_lower(person.get("QualificationsAwarded", ""))
    qual_level = _get_qualification_level(qualifications)

    # Also check for Master's degrees
    master1 = _safe_lower(person.get("Master1", ""))
    master2 = _safe_lower(person.get("Master2", ""))
    if master1 or master2:
        qual_level = max(qual_level, 5)  # At least Master's level

    raw_score += (qual_level / 6.0) * 10

    # Subject/field match (0-10 points)
    field_match_score = 0.0

    # Check subjects studied
    subjects = _safe_lower(person.get("SubjectsStudied", ""))
    matched_subjects = set()
    for kw in education_keywords_lower:
        if kw in subjects and kw not in matched_subjects:
            field_match_score += 2
            matched_subjects.add(kw)

    # Check qualifications text for field keywords
    for kw in education_keywords_lower:
        if kw in qualifications and kw not in matched_subjects:
            field_match_score += 1.5
            matched_subjects.add(kw)

    # Check master's degrees for field keywords
    masters_text = f"{master1} {master2}"
    for kw in education_keywords_lower:
        if kw in masters_text and kw not in matched_subjects:
            field_match_score += 2
            matched_subjects.add(kw)

    raw_score += min(10.0, field_match_score)

    # University prestige (0-5 points)
    college = _safe_lower(person.get("College/University", ""))
    university_bonus = _get_university_bonus(college)
    raw_score += university_bonus

    # Normalize to max weight
    return min(max_score, (raw_score / 25.0) * max_score)


def _get_university_bonus(college_text: str) -> float:
    """Get bonus points based on university ranking (0-5 points)."""
    if not college_text:
        return 0.0

    # Check Top 50
    for uni_name in Top50Universities:
        if uni_name.lower() in college_text:
            return 5.0

    # Check Top 100
    for uni_name in Top100Universities:
        if uni_name.lower() in college_text:
            return 3.5

    # Any university mentioned
    if "university" in college_text or "college" in college_text:
        return 2.0

    return 0.0


def _get_qualification_level(qualifications_text: str) -> int:
    """Get the highest qualification level from text (0-6)."""
    max_level = 0

    if not qualifications_text:
        return max_level

    for level, keywords in Qualifications.items():
        for keyword in keywords:
            if keyword.lower() in qualifications_text:
                max_level = max(max_level, level)

    return max_level


def _calculate_work_score(person: dict, sector: str) -> float:
    """
    Calculate work experience score (0 to WEIGHTS['work_experience']).

    Scoring breakdown:
    - Total years of experience: 0-12 points
    - Seniority level: 0-8 points
    - Sector relevance: 0-10 points
    """
    max_score = WEIGHTS["work_experience"]
    raw_score = 0.0

    sector_data = JobSectors[sector]
    work_keywords = sector_data.get("WorkExperience", [])
    work_keywords_lower = [kw.lower() for kw in work_keywords]

    total_years = 0.0
    max_seniority = 0
    relevance_score = 0.0
    matched_keywords = set()

    # Process each workplace (1-3)
    for i in range(1, 4):
        workplace = _safe_str(person.get(f"Workplace{i}", ""))
        dates = _safe_str(person.get(f"Dates{i}", ""))
        occupation = _safe_str(person.get(f"Occupation{i}", ""))
        activities = _safe_str(person.get(f"MainActivities{i}", ""))

        if not workplace:
            continue

        # Calculate time worked
        years_worked = _calculate_time_worked(dates)
        total_years += years_worked

        # Get seniority level
        seniority = _get_seniority_level(occupation)
        max_seniority = max(max_seniority, seniority)

        # Check for keyword matches (relevance)
        all_text = f"{workplace} {occupation} {activities}".lower()
        for kw in work_keywords_lower:
            if kw in all_text and kw not in matched_keywords:
                relevance_score += 2.5
                matched_keywords.add(kw)

    # Years of experience (cap at 10+ years = max points)
    years_points = min(12.0, total_years * 1.2)
    raw_score += years_points

    # Seniority level (0-6 scale mapped to 0-8 points)
    raw_score += (max_seniority / 6.0) * 8

    # Sector relevance (capped at 10)
    raw_score += min(10.0, relevance_score)

    # Normalize to max weight
    return min(max_score, (raw_score / 30.0) * max_score)


def _calculate_time_worked(dates_str: str) -> float:
    """Calculate years worked from date range string."""
    if not dates_str or "-" not in dates_str:
        return 0.0

    try:
        parts = dates_str.split("-")
        if len(parts) != 2:
            return 0.0

        date_start = parts[0].strip()
        date_finish = parts[1].strip()

        # Parse start date
        start_date = _parse_date(date_start)
        if not start_date:
            return 0.0

        # Parse end date
        if date_finish.lower() in ["current", "present", "now", "ongoing", ""]:
            end_date = date.today()
        else:
            end_date = _parse_date(date_finish)
            if not end_date:
                end_date = date.today()

        years = (end_date - start_date).days / 365.25
        return max(0.0, years)
    except (ValueError, IndexError, AttributeError):
        return 0.0


def _parse_date(date_str: str) -> Optional[date]:
    """Parse a date string in DD.MM.YYYY format."""
    if not date_str:
        return None

    try:
        parts = date_str.strip().split(".")
        if len(parts) >= 3:
            day = int(parts[0])
            month = int(parts[1])
            year = int(parts[2])
            return date(year, month, day)
    except (ValueError, IndexError):
        pass

    return None


def _get_seniority_level(occupation_text: str) -> int:
    """Get seniority level from occupation text (0-6)."""
    if not occupation_text:
        return 0

    occupation_lower = occupation_text.lower()
    max_level = 0

    for level, keywords in Functions.items():
        for keyword in keywords:
            if keyword.lower() in occupation_lower:
                max_level = max(max_level, level)

    return max_level


def _calculate_language_score(person: dict) -> float:
    """
    Calculate language proficiency score (0 to WEIGHTS['languages']).
    """
    max_score = WEIGHTS["languages"]
    raw_score = 0.0

    # Mother language (3 points if it's a global language)
    mother_language = _safe_lower(person.get("MotherLanguage", ""))
    mother_tier = _get_language_tier(mother_language)
    raw_score += mother_tier * 1.0

    # Additional languages
    for i in range(1, 3):
        language = _safe_lower(person.get(f"ModernLanguage{i}", ""))
        level = _safe_lower(person.get(f"Level{i}", ""))

        if language:
            lang_tier = _get_language_tier(language)
            level_multiplier = _get_level_multiplier(level)
            raw_score += lang_tier * level_multiplier * 0.5

    # Normalize to max weight (max raw = ~12 if trilingual with top languages)
    return min(max_score, (raw_score / 12.0) * max_score)


def _get_language_tier(language: str) -> int:
    """Get the business value tier of a language (1-3)."""
    if not language:
        return 0

    for tier, languages in Languages.items():
        if language in [lang.lower() for lang in languages]:
            return tier

    return 1  # Default for unknown languages


def _get_level_multiplier(level: str) -> float:
    """Convert language level to a multiplier (0-1)."""
    if not level:
        return 0.3

    level_clean = level.strip().lower()

    # Check exact match first
    if level_clean in LanguageLevels:
        return LanguageLevels[level_clean]["score"] / 10.0

    # Check partial matches
    for level_key, level_data in LanguageLevels.items():
        if level_key in level_clean or level_clean in level_key:
            return level_data["score"] / 10.0

    # Check for CEFR levels
    cefr_scores = {
        "a1": 0.2,
        "a2": 0.3,
        "b1": 0.5,
        "b2": 0.7,
        "c1": 0.9,
        "c2": 1.0,
    }
    for cefr, score in cefr_scores.items():
        if cefr in level_clean:
            return score

    return 0.3  # Default


def _calculate_skills_score(person: dict, sector: str) -> float:
    """
    Calculate skills matching score (0 to WEIGHTS['skills']).
    """
    max_score = WEIGHTS["skills"]

    sector_data = JobSectors[sector]
    required_skills = sector_data.get("Skills", [])
    extra_skills = sector_data.get("ExtraSkills", [])

    # Gather all person's skills
    person_skills_text = ""
    for field in [
        "CommunicationSkills",
        "OrganizationalManagerialSkills",
        "JobRelatedSkills",
        "ComputerSkills",
        "OtherSkills",
    ]:
        person_skills_text += " " + _safe_lower(person.get(field, ""))

    # Count unique matched skills
    matched_required = 0
    matched_extra = 0

    for skill in required_skills:
        if skill.lower() in person_skills_text:
            matched_required += 1

    for skill in extra_skills:
        if skill.lower() in person_skills_text:
            matched_extra += 1

    # Score calculation
    # Required skills are worth more
    total_required = max(1, len(required_skills))
    total_extra = max(1, len(extra_skills))

    required_ratio = matched_required / total_required
    extra_ratio = matched_extra / total_extra

    # 70% weight to required, 30% to extra skills
    raw_score = (required_ratio * 0.7 + extra_ratio * 0.3) * max_score

    # Driving license bonus (if sector seems to need it)
    driving = _safe_lower(person.get("DrivingLicense", ""))
    if driving and driving not in ["no", "none", "n/a"]:
        raw_score += 1.0

    return min(max_score, raw_score)


def _calculate_soft_skills_score(person: dict) -> float:
    """
    Calculate soft skills score (0 to WEIGHTS['soft_skills']).
    """
    max_score = WEIGHTS["soft_skills"]

    # Gather text to analyze
    all_text = ""
    for field in [
        "ShortDescription",
        "CommunicationSkills",
        "OrganizationalManagerialSkills",
        "MainActivities1",
        "MainActivities2",
        "MainActivities3",
    ]:
        all_text += " " + _safe_lower(person.get(field, ""))

    # Count soft skill category matches
    categories_matched = 0
    for category, keywords in SoftSkills.items():
        for kw in keywords:
            if kw.lower() in all_text:
                categories_matched += 1
                break  # Only count category once

    # Each category matched is worth some points
    total_categories = len(SoftSkills)
    ratio = categories_matched / max(1, total_categories)

    return ratio * max_score


def _calculate_additional_score(person: dict) -> float:
    """
    Calculate additional information score (0 to WEIGHTS['additional']).

    Awards, publications, projects, etc.
    """
    max_score = WEIGHTS["additional"]
    raw_score = 0.0

    # Publications (high value)
    publications = _safe_str(person.get("Publications", ""))
    if publications:
        pub_count = min(3, publications.count(",") + 1)
        raw_score += pub_count * 0.5

    # Honours and Awards (high value)
    awards = _safe_str(person.get("HonoursAndAwards", ""))
    if awards:
        award_count = min(3, awards.count(",") + 1)
        raw_score += award_count * 0.6

    # Projects
    projects = _safe_str(person.get("Projects", ""))
    if projects:
        proj_count = min(3, projects.count(",") + 1)
        raw_score += proj_count * 0.3

    # Presentations
    presentations = _safe_str(person.get("Presentations", ""))
    if presentations:
        raw_score += 0.4

    # Conferences
    conferences = _safe_str(person.get("Conferences", ""))
    if conferences:
        raw_score += 0.3

    # Memberships
    memberships = _safe_str(person.get("Memberships", ""))
    if memberships:
        raw_score += 0.4

    return min(max_score, raw_score)


# Utility functions


def _safe_str(value) -> str:
    """Safely convert value to string."""
    if value is None:
        return ""
    return str(value).strip()


def _safe_lower(value) -> str:
    """Safely convert value to lowercase string."""
    return _safe_str(value).lower()
