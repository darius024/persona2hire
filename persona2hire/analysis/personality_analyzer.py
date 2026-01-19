"""
Personality analysis using Myers-Briggs Type Indicator (MBTI) and Big Five.

This module infers personality types from CV text content (descriptions, hobbies,
skills). It's used both for personality insights and for job-personality matching
bonuses in the scoring system.

MBTI Analysis
=============
The Myers-Briggs Type Indicator classifies personalities across four dimensions:

- I/E (Introversion/Extroversion): Energy direction (inward vs outward)
- S/N (Sensing/iNtuition): Information processing (concrete vs abstract)
- T/F (Thinking/Feeling): Decision making (logic vs values)
- J/P (Judging/Perceiving): Lifestyle (structured vs flexible)

These combine into 16 types (e.g., INTJ, ENFP).

How Analysis Works
==================
1. Text sources are gathered: ShortDescription, Hobbies, skills fields
2. Words are tokenized and normalized (lowercase, punctuation stripped)
3. Each word is matched against curated word lists for each MBTI dimension
4. Hobbies are mapped to personality indicators (e.g., "reading" → I, "sports" → E)
5. Scores accumulate for each letter in each dimension pair
6. The letter with higher score wins for each dimension

Example:
    Description: "analytical, organized, independent problem-solver"
    - "analytical" → T (Thinking)
    - "organized" → J (Judging)  
    - "independent" → I (Introversion)
    Result: I_TJ (with other dimensions determined by remaining text)

Big Five (OCEAN) Analysis
=========================
Also analyzes the five-factor personality model:
- Openness: Creativity, curiosity, unconventionality
- Conscientiousness: Organization, discipline, responsibility
- Extroversion: Sociability, energy, assertiveness
- Agreeableness: Cooperation, empathy, trust
- Neuroticism: Anxiety, emotional reactivity, stress

Scores range from -100 to +100 based on high/low indicator word matches.

Personality-Job Matching
========================
Each job sector in job_sectors.py defines preferred MBTI types. For example:
- Computers_ICT prefers: INTJ, INTP, ISTJ, ENTJ
- Healthcare prefers: ISFJ, ESFJ, ENFJ, INFJ

If a candidate's inferred type matches:
- Exact match: +5 bonus points
- Partial match (first 2 letters): +2.5 bonus points

Known Limitations
=================
1. Text-based inference is imprecise - not a valid psychological assessment
2. Limited signal from short descriptions and hobby lists
3. Word lists reflect Western/English personality associations
4. MBTI itself is scientifically debated as a personality model
5. Results should be treated as rough estimates, not definitive typing

Usage
=====
    from persona2hire.analysis.personality_analyzer import (
        analyze_personality,
        get_personality_percentages,
        get_big_five_profile,
        get_career_suggestions,
    )
    
    # Get 4-letter MBTI type
    mbti_type = analyze_personality(cv_data)  # e.g., "INTJ"
    
    # Get percentage breakdown
    percentages = get_personality_percentages(cv_data)
    # {'I': 65.0, 'E': 35.0, 'S': 40.0, 'N': 60.0, ...}
    
    # Get Big Five profile
    ocean = get_big_five_profile(cv_data)
    # {'openness': 45.0, 'conscientiousness': 60.0, ...}
    
    # Get career suggestions for a type
    careers = get_career_suggestions("INTJ")
    # ['scientist', 'engineer', 'programmer', ...]
"""

from ..data.personality import Domains, Hobbies, PersonalityTypes, BigFive


def analyze_personality(person: dict) -> str:
    """
    Analyze a person's personality type based on their CV data.

    Args:
        person: Dictionary containing CV data

    Returns:
        4-letter MBTI personality type (e.g., "INTJ", "ENFP")
    """
    # Create a fresh copy of domains to avoid state issues
    domains = _get_fresh_domains()

    # Analyze description words
    description = person.get("ShortDescription", "").lower()
    description_words = [
        w.strip() for w in description.replace(",", " ").split() if w.strip()
    ]
    _score_from_words(domains, description_words)

    # Analyze hobbies
    hobbies_text = person.get("Hobbies", "").lower()
    hobbies_list = [h.strip() for h in hobbies_text.split(",") if h.strip()]
    _score_from_hobbies(domains, hobbies_list)

    # Analyze skills for personality indicators
    skills_text = _gather_skills_text(person)
    skills_words = [
        w.strip() for w in skills_text.replace(",", " ").split() if w.strip()
    ]
    _score_from_words(domains, skills_words, weight=0.5)

    # Calculate domain scores
    scores = {
        "I": _sum_domain_scores(domains, "I"),
        "E": _sum_domain_scores(domains, "E"),
        "S": _sum_domain_scores(domains, "S"),
        "N": _sum_domain_scores(domains, "N"),
        "T": _sum_domain_scores(domains, "T"),
        "F": _sum_domain_scores(domains, "F"),
        "J": _sum_domain_scores(domains, "J"),
        "P": _sum_domain_scores(domains, "P"),
    }

    # Determine personality type
    personality_type = ""
    personality_type += "I" if scores["I"] >= scores["E"] else "E"
    personality_type += "S" if scores["S"] >= scores["N"] else "N"
    personality_type += "T" if scores["T"] >= scores["F"] else "F"
    personality_type += "J" if scores["J"] >= scores["P"] else "P"

    return personality_type


def get_personality_percentages(person: dict) -> dict:
    """
    Get detailed percentage breakdown of personality dimensions.

    Args:
        person: Dictionary containing CV data

    Returns:
        Dictionary with percentages for each MBTI dimension
    """
    # Create fresh domains
    domains = _get_fresh_domains()

    # Analyze all text
    description = person.get("ShortDescription", "").lower()
    description_words = [
        w.strip() for w in description.replace(",", " ").split() if w.strip()
    ]
    _score_from_words(domains, description_words)

    hobbies_text = person.get("Hobbies", "").lower()
    hobbies_list = [h.strip() for h in hobbies_text.split(",") if h.strip()]
    _score_from_hobbies(domains, hobbies_list)

    # Calculate scores
    scores = {
        "I": _sum_domain_scores(domains, "I"),
        "E": _sum_domain_scores(domains, "E"),
        "S": _sum_domain_scores(domains, "S"),
        "N": _sum_domain_scores(domains, "N"),
        "T": _sum_domain_scores(domains, "T"),
        "F": _sum_domain_scores(domains, "F"),
        "J": _sum_domain_scores(domains, "J"),
        "P": _sum_domain_scores(domains, "P"),
    }

    # Calculate percentages (add 1 to avoid division by zero)
    ie_total = scores["I"] + scores["E"] + 1
    sn_total = scores["S"] + scores["N"] + 1
    tf_total = scores["T"] + scores["F"] + 1
    jp_total = scores["J"] + scores["P"] + 1

    return {
        "I": round(scores["I"] / ie_total * 100, 1),
        "E": round(scores["E"] / ie_total * 100, 1),
        "S": round(scores["S"] / sn_total * 100, 1),
        "N": round(scores["N"] / sn_total * 100, 1),
        "T": round(scores["T"] / tf_total * 100, 1),
        "F": round(scores["F"] / tf_total * 100, 1),
        "J": round(scores["J"] / jp_total * 100, 1),
        "P": round(scores["P"] / jp_total * 100, 1),
    }


def get_big_five_profile(person: dict) -> dict:
    """
    Analyze Big Five (OCEAN) personality traits.

    Args:
        person: Dictionary containing CV data

    Returns:
        Dictionary with scores for each Big Five trait
    """
    description = person.get("ShortDescription", "").lower()
    hobbies = person.get("Hobbies", "").lower()
    skills = _gather_skills_text(person)

    all_text = f"{description} {hobbies} {skills}"

    profile = {}
    for trait, levels in BigFive.items():
        high_matches = sum(
            1 for word in levels.get("high", []) if word.lower() in all_text
        )
        low_matches = sum(
            1 for word in levels.get("low", []) if word.lower() in all_text
        )

        # Calculate score (-100 to +100 scale)
        total = high_matches + low_matches + 1  # Avoid division by zero
        score = ((high_matches - low_matches) / total) * 100
        profile[trait] = round(score, 1)

    return profile


def get_career_suggestions(personality_type: str) -> list:
    """
    Get career suggestions based on personality type.

    Args:
        personality_type: 4-letter MBTI type

    Returns:
        List of suggested careers
    """
    if personality_type in PersonalityTypes:
        return PersonalityTypes[personality_type].get("Careers", [])
    return []


def _get_fresh_domains() -> dict:
    """Create a fresh copy of domains with reset scores."""
    domains = {}
    for domain_key, domain_data in Domains.items():
        domains[domain_key] = {}
        for trait_key, trait_data in domain_data.items():
            if trait_key == "SCORE":
                domains[domain_key][trait_key] = 0
            elif isinstance(trait_data, dict):
                domains[domain_key][trait_key] = {
                    "words": trait_data.get("words", []).copy(),
                    "score": 0,
                }
    return domains


def _gather_skills_text(person: dict) -> str:
    """Gather all skills text from person data."""
    skills_fields = [
        "CommunicationSkills",
        "OrganizationalManagerialSkills",
        "JobRelatedSkills",
        "ComputerSkills",
        "OtherSkills",
    ]
    return " ".join(person.get(field, "") for field in skills_fields).lower()


def _score_from_words(domains: dict, words: list, weight: float = 1.0):
    """Score personality based on word matches."""
    for word in words:
        word_clean = word.strip().lower()
        if not word_clean:
            continue

        for domain_key in domains:
            for trait_key, trait_data in domains[domain_key].items():
                if trait_key != "SCORE" and isinstance(trait_data, dict):
                    trait_words = trait_data.get("words", [])
                    for trait_word in trait_words:
                        if (
                            word_clean == trait_word.lower()
                            or trait_word.lower() in word_clean
                        ):
                            domains[domain_key][trait_key]["score"] += weight
                            break


def _score_from_hobbies(domains: dict, hobbies_list: list):
    """Score personality based on hobby matches."""
    hobby_words = Hobbies.get("words", [])
    hobby_domains = Hobbies.get("domain", [])
    hobby_traits = Hobbies.get("trait", [])

    for hobby in hobbies_list:
        hobby_clean = hobby.strip().lower()
        if not hobby_clean:
            continue

        # Find matching hobby in the list
        for i, hobby_word in enumerate(hobby_words):
            if hobby_word.lower() in hobby_clean or hobby_clean in hobby_word.lower():
                # Get the domain and trait for this hobby
                if i < len(hobby_domains) and i < len(hobby_traits):
                    domain = hobby_domains[i]
                    trait = hobby_traits[i]

                    # Add score to the corresponding domain/trait
                    if domain in domains and trait in domains[domain]:
                        if isinstance(domains[domain][trait], dict):
                            domains[domain][trait]["score"] += 1
                break

    # Also check sports
    sports = Hobbies.get("sports", [])
    for hobby in hobbies_list:
        hobby_clean = hobby.strip().lower()
        for sport in sports:
            if sport.lower() in hobby_clean:
                # Sports tend to indicate E, S, and P traits
                if "E" in domains and "energetic" in domains["E"]:
                    domains["E"]["energetic"]["score"] += 0.5
                if "S" in domains and "practical" in domains["S"]:
                    domains["S"]["practical"]["score"] += 0.5
                break


def _sum_domain_scores(domains: dict, domain_key: str) -> float:
    """Sum all trait scores for a domain."""
    total = 0
    if domain_key in domains:
        for trait_key, trait_data in domains[domain_key].items():
            if trait_key != "SCORE" and isinstance(trait_data, dict):
                total += trait_data.get("score", 0)
    return total
