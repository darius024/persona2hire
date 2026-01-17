"""Personality analysis using Myers-Briggs Type Indicator (MBTI)."""

from ..data.personality import Domains, Hobbies


def analyze_personality(person: dict) -> str:
    """
    Analyze a person's personality type based on their CV data.
    
    Args:
        person: Dictionary containing CV data
        
    Returns:
        4-letter MBTI personality type (e.g., "INTJ", "ENFP")
    """
    # Reset domain scores
    _reset_domain_scores()
    
    # Analyze hobbies
    hobbies = [h.strip() for h in person.get("Hobbies", "").lower().split(",")]
    description = [d.strip() for d in person.get("ShortDescription", "").lower().split(",")]
    
    # Score based on description words
    _score_from_words(description)
    
    # Score based on hobbies (if mapping exists)
    for word in hobbies:
        if word in Hobbies["words"]:
            index = Hobbies["words"].index(word)
            if index < len(Hobbies["domain"]) and index < len(Hobbies["trait"]):
                domain = Hobbies["domain"][index]
                trait = Hobbies["trait"][index]
                if domain in Domains and trait in Domains[domain]:
                    Domains[domain][trait]["score"] += 1
    
    # Calculate domain scores
    domain_ie_i = _sum_domain_scores("I")
    domain_ie_e = _sum_domain_scores("E")
    domain_sn_s = _sum_domain_scores("S")
    domain_sn_n = _sum_domain_scores("N")
    domain_tf_t = _sum_domain_scores("T")
    domain_tf_f = _sum_domain_scores("F")
    domain_jp_j = _sum_domain_scores("J")
    domain_jp_p = _sum_domain_scores("P")
    
    # Determine personality type
    personality_type = ""
    personality_type += "I" if domain_ie_i >= domain_ie_e else "E"
    personality_type += "S" if domain_sn_s >= domain_sn_n else "N"
    personality_type += "T" if domain_tf_t >= domain_tf_f else "F"
    personality_type += "J" if domain_jp_j >= domain_jp_p else "P"
    
    return personality_type


def get_personality_percentages(person: dict) -> dict:
    """
    Get detailed percentage breakdown of personality dimensions.
    
    Args:
        person: Dictionary containing CV data
        
    Returns:
        Dictionary with percentages for each MBTI dimension
    """
    # Analyze first to populate scores
    analyze_personality(person)
    
    domain_ie_i = _sum_domain_scores("I")
    domain_ie_e = _sum_domain_scores("E")
    domain_sn_s = _sum_domain_scores("S")
    domain_sn_n = _sum_domain_scores("N")
    domain_tf_t = _sum_domain_scores("T")
    domain_tf_f = _sum_domain_scores("F")
    domain_jp_j = _sum_domain_scores("J")
    domain_jp_p = _sum_domain_scores("P")
    
    # Calculate percentages (add 1 to avoid division by zero)
    domain_ie = domain_ie_i + domain_ie_e + 1
    domain_sn = domain_sn_s + domain_sn_n + 1
    domain_tf = domain_tf_t + domain_tf_f + 1
    domain_jp = domain_jp_j + domain_jp_p + 1
    
    return {
        "I": domain_ie_i / domain_ie * 100,
        "E": domain_ie_e / domain_ie * 100,
        "S": domain_sn_s / domain_sn * 100,
        "N": domain_sn_n / domain_sn * 100,
        "T": domain_tf_t / domain_tf * 100,
        "F": domain_tf_f / domain_tf * 100,
        "J": domain_jp_j / domain_jp * 100,
        "P": domain_jp_p / domain_jp * 100
    }


def _reset_domain_scores():
    """Reset all domain scores to zero."""
    for domain in Domains:
        for trait in Domains[domain]:
            if trait != "SCORE" and isinstance(Domains[domain][trait], dict):
                Domains[domain][trait]["score"] = 0
        Domains[domain]["SCORE"] = 0


def _score_from_words(words: list):
    """Score personality based on word matches."""
    for word in words:
        word = word.strip()
        for domain in Domains:
            for trait in Domains[domain]:
                if trait != "SCORE" and isinstance(Domains[domain][trait], dict):
                    if word in Domains[domain][trait]["words"]:
                        Domains[domain][trait]["score"] += 1


def _sum_domain_scores(domain_key: str) -> int:
    """Sum all trait scores for a domain."""
    total = 0
    if domain_key in Domains:
        for trait in Domains[domain_key]:
            if trait != "SCORE" and isinstance(Domains[domain_key][trait], dict):
                total += Domains[domain_key][trait].get("score", 0)
    return total
