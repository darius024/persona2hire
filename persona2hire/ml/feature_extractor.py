"""Feature extraction from CV data for ML models."""

import re
from typing import Optional
from datetime import date


class FeatureExtractor:
    """Extract numerical features from CV data for ML processing."""

    # Feature names for model training
    FEATURE_NAMES = [
        # Education features (5)
        "education_level",  # 0-6 scale
        "education_field_match",  # 0-1 ratio
        "university_prestige",  # 0-3 scale
        "years_studied",  # Numeric
        "has_masters",  # Binary
        # Work experience features (6)
        "total_work_years",  # Numeric
        "num_positions",  # 0-3
        "max_seniority",  # 0-6 scale
        "work_field_match",  # 0-1 ratio
        "current_employment",  # Binary
        "avg_tenure",  # Years per position
        # Skills features (5)
        "required_skills_match",  # 0-1 ratio
        "extra_skills_match",  # 0-1 ratio
        "has_driving_license",  # Binary
        "computer_skills_count",  # Numeric
        "total_skills_words",  # Numeric
        # Language features (4)
        "num_languages",  # 1-5
        "has_english",  # Binary
        "max_language_level",  # 0-6 (CEFR)
        "mother_tongue_tier",  # 1-3 business value
        # Soft skills features (3)
        "soft_skills_categories",  # Numeric
        "has_leadership",  # Binary
        "has_communication",  # Binary
        # Additional features (4)
        "publications_count",  # Numeric
        "awards_count",  # Numeric
        "projects_count",  # Numeric
        "professional_memberships",  # Binary
        # Personality features (4)
        "personality_match",  # Binary
        "personality_partial_match",  # Binary
        "introversion_score",  # 0-1
        "thinking_score",  # 0-1
    ]

    def __init__(self, sector_data: Optional[dict] = None):
        """
        Initialize feature extractor.

        Args:
            sector_data: Job sector data for field matching (optional)
        """
        self.sector_data = sector_data or {}

    def extract(self, cv_data: dict, sector: str = "") -> list[float]:
        """
        Extract all features from CV data.

        Args:
            cv_data: Dictionary containing CV data
            sector: Target job sector for field matching

        Returns:
            List of numerical features
        """
        features = []

        # Education features
        features.extend(self._extract_education_features(cv_data, sector))

        # Work experience features
        features.extend(self._extract_work_features(cv_data, sector))

        # Skills features
        features.extend(self._extract_skills_features(cv_data, sector))

        # Language features
        features.extend(self._extract_language_features(cv_data))

        # Soft skills features
        features.extend(self._extract_soft_skills_features(cv_data))

        # Additional features
        features.extend(self._extract_additional_features(cv_data))

        # Personality features
        features.extend(self._extract_personality_features(cv_data, sector))

        return features

    def _extract_education_features(self, cv_data: dict, sector: str) -> list[float]:
        """Extract education-related features."""
        features = []

        # Education level (0-6)
        qual_text = self._safe_lower(cv_data.get("QualificationsAwarded", ""))
        education_level = self._get_education_level(qual_text)

        # Boost for master's
        master1 = cv_data.get("Master1", "")
        master2 = cv_data.get("Master2", "")
        has_masters = 1.0 if (master1 or master2) else 0.0
        if has_masters:
            education_level = max(education_level, 5)

        features.append(float(education_level))

        # Field match ratio
        subjects = self._safe_lower(cv_data.get("SubjectsStudied", ""))
        field_keywords = self._get_sector_keywords(sector, "School/College")
        field_match = self._calculate_match_ratio(subjects, field_keywords)
        features.append(field_match)

        # University prestige
        college = self._safe_lower(cv_data.get("College/University", ""))
        prestige = self._get_university_prestige(college)
        features.append(float(prestige))

        # Years studied
        years = cv_data.get("YearsStudied", "0")
        try:
            years_float = float(years)
        except ValueError:
            years_float = 0.0
        features.append(min(years_float, 10.0))  # Cap at 10

        # Has masters
        features.append(has_masters)

        return features

    def _extract_work_features(self, cv_data: dict, sector: str) -> list[float]:
        """Extract work experience features."""
        features = []

        total_years = 0.0
        num_positions = 0
        max_seniority = 0
        is_current = False
        tenures = []

        work_keywords = self._get_sector_keywords(sector, "WorkExperience")
        work_text = ""

        for i in range(1, 4):
            workplace = cv_data.get(f"Workplace{i}", "")
            if not workplace:
                continue

            num_positions += 1
            dates = cv_data.get(f"Dates{i}", "")
            occupation = cv_data.get(f"Occupation{i}", "")
            activities = cv_data.get(f"MainActivities{i}", "")

            # Work text for matching
            work_text += f" {workplace} {occupation} {activities}"

            # Calculate tenure
            tenure = self._calculate_tenure(dates)
            if tenure > 0:
                tenures.append(tenure)
                total_years += tenure

            # Check if current
            if "current" in dates.lower() or "present" in dates.lower():
                is_current = True

            # Seniority
            seniority = self._get_seniority(occupation)
            max_seniority = max(max_seniority, seniority)

        features.append(min(total_years, 20.0))  # Cap at 20 years
        features.append(float(num_positions))
        features.append(float(max_seniority))

        # Work field match
        field_match = self._calculate_match_ratio(work_text.lower(), work_keywords)
        features.append(field_match)

        features.append(1.0 if is_current else 0.0)

        # Average tenure
        avg_tenure = sum(tenures) / len(tenures) if tenures else 0.0
        features.append(min(avg_tenure, 10.0))

        return features

    def _extract_skills_features(self, cv_data: dict, sector: str) -> list[float]:
        """Extract skills-related features."""
        features = []

        # Gather all skills text
        skills_text = ""
        for field in [
            "ComputerSkills",
            "JobRelatedSkills",
            "OtherSkills",
            "CommunicationSkills",
            "OrganizationalManagerialSkills",
        ]:
            skills_text += " " + self._safe_lower(cv_data.get(field, ""))

        # Required skills match
        required_skills = self._get_sector_keywords(sector, "Skills")
        required_match = self._calculate_match_ratio(skills_text, required_skills)
        features.append(required_match)

        # Extra skills match
        extra_skills = self._get_sector_keywords(sector, "ExtraSkills")
        extra_match = self._calculate_match_ratio(skills_text, extra_skills)
        features.append(extra_match)

        # Driving license
        driving = cv_data.get("DrivingLicense", "").lower()
        has_license = 1.0 if driving and driving not in ["no", "none", "n/a", ""] else 0.0
        features.append(has_license)

        # Computer skills count
        computer_skills = cv_data.get("ComputerSkills", "")
        skills_count = len([s for s in computer_skills.split(",") if s.strip()])
        features.append(min(float(skills_count), 15.0))

        # Total skills words
        total_words = len(skills_text.split())
        features.append(min(float(total_words), 100.0))

        return features

    def _extract_language_features(self, cv_data: dict) -> list[float]:
        """Extract language-related features."""
        features = []

        # Count languages
        num_languages = 1  # Mother language
        mother = cv_data.get("MotherLanguage", "")
        lang1 = cv_data.get("ModernLanguage1", "")
        lang2 = cv_data.get("ModernLanguage2", "")

        if lang1:
            num_languages += 1
        if lang2:
            num_languages += 1

        features.append(float(num_languages))

        # Has English
        all_langs = f"{mother} {lang1} {lang2}".lower()
        has_english = 1.0 if "english" in all_langs else 0.0
        features.append(has_english)

        # Max language level (CEFR)
        level1 = cv_data.get("Level1", "")
        level2 = cv_data.get("Level2", "")
        max_level = max(
            self._parse_language_level(level1), self._parse_language_level(level2)
        )
        features.append(float(max_level))

        # Mother tongue tier
        tier = self._get_language_tier(mother)
        features.append(float(tier))

        return features

    def _extract_soft_skills_features(self, cv_data: dict) -> list[float]:
        """Extract soft skills features."""
        features = []

        text = ""
        for field in [
            "ShortDescription",
            "CommunicationSkills",
            "OrganizationalManagerialSkills",
        ]:
            text += " " + self._safe_lower(cv_data.get(field, ""))

        # Soft skills categories matched
        categories = {
            "leadership": ["lead", "manage", "direct", "supervise", "mentor"],
            "communication": ["communicate", "present", "speak", "write", "listen"],
            "teamwork": ["team", "collaborate", "cooperate", "coordinate"],
            "problem_solving": ["solve", "analyze", "think", "innovate", "creative"],
            "organization": ["organize", "plan", "schedule", "prioritize"],
        }

        matched_categories = 0
        has_leadership = 0.0
        has_communication = 0.0

        for cat, keywords in categories.items():
            if any(kw in text for kw in keywords):
                matched_categories += 1
                if cat == "leadership":
                    has_leadership = 1.0
                if cat == "communication":
                    has_communication = 1.0

        features.append(float(matched_categories))
        features.append(has_leadership)
        features.append(has_communication)

        return features

    def _extract_additional_features(self, cv_data: dict) -> list[float]:
        """Extract additional information features."""
        features = []

        # Publications count
        pubs = cv_data.get("Publications", "")
        pub_count = len([p for p in pubs.split(",") if p.strip()]) if pubs else 0
        features.append(min(float(pub_count), 10.0))

        # Awards count
        awards = cv_data.get("HonoursAndAwards", "")
        award_count = len([a for a in awards.split(",") if a.strip()]) if awards else 0
        features.append(min(float(award_count), 10.0))

        # Projects count
        projects = cv_data.get("Projects", "")
        proj_count = len([p for p in projects.split(",") if p.strip()]) if projects else 0
        features.append(min(float(proj_count), 10.0))

        # Professional memberships
        memberships = cv_data.get("Memberships", "")
        has_memberships = 1.0 if memberships.strip() else 0.0
        features.append(has_memberships)

        return features

    def _extract_personality_features(self, cv_data: dict, sector: str) -> list[float]:
        """Extract personality-related features."""
        features = []

        personality = cv_data.get("PersonalityTypeMB", "")
        preferred = self._get_sector_keywords(sector, "Personality")

        # Exact match
        exact_match = 1.0 if personality in preferred else 0.0
        features.append(exact_match)

        # Partial match (first 2 letters)
        partial_match = 0.0
        if len(personality) >= 2:
            for pref in preferred:
                if len(pref) >= 2 and personality[:2] == pref[:2]:
                    partial_match = 1.0
                    break
        features.append(partial_match)

        # I/E score (introversion)
        introversion = 0.5  # Default neutral
        if personality and len(personality) >= 1:
            introversion = 1.0 if personality[0] == "I" else 0.0
        features.append(introversion)

        # T/F score (thinking)
        thinking = 0.5  # Default neutral
        if personality and len(personality) >= 3:
            thinking = 1.0 if personality[2] == "T" else 0.0
        features.append(thinking)

        return features

    # Helper methods

    def _safe_lower(self, value) -> str:
        """Safely convert to lowercase string."""
        if value is None:
            return ""
        return str(value).lower().strip()

    def _get_sector_keywords(self, sector: str, field: str) -> list[str]:
        """Get keywords for a sector field."""
        if not sector or not self.sector_data:
            return []
        sector_info = self.sector_data.get(sector, {})
        return sector_info.get(field, [])

    def _calculate_match_ratio(self, text: str, keywords: list[str]) -> float:
        """Calculate match ratio between text and keywords."""
        if not keywords:
            return 0.0

        text_lower = text.lower()
        matched = sum(1 for kw in keywords if kw.lower() in text_lower)
        return matched / len(keywords)

    def _get_education_level(self, qual_text: str) -> int:
        """Get education level from qualification text (0-6)."""
        levels = {
            6: ["phd", "doctorate", "doctoral"],
            5: ["master", "msc", "ma", "mba"],
            4: ["bachelor", "bsc", "ba", "degree"],
            3: ["diploma", "associate"],
            2: ["certificate", "vocational"],
            1: ["high school", "secondary", "a-level"],
        }

        for level, keywords in levels.items():
            if any(kw in qual_text for kw in keywords):
                return level
        return 0

    def _get_university_prestige(self, college: str) -> int:
        """Get university prestige level (0-3)."""
        # Top tier keywords
        top_tier = ["harvard", "mit", "stanford", "oxford", "cambridge", "eth"]
        if any(t in college for t in top_tier):
            return 3

        # Good tier
        good_tier = ["university", "institute of technology", "polytechnic"]
        if any(t in college for t in good_tier):
            return 2

        if college:
            return 1

        return 0

    def _calculate_tenure(self, dates: str) -> float:
        """Calculate tenure in years from date string."""
        if not dates or "-" not in dates:
            return 0.0

        try:
            parts = dates.split("-")
            if len(parts) != 2:
                return 0.0

            start_str = parts[0].strip()
            end_str = parts[1].strip()

            start = self._parse_date(start_str)
            if not start:
                return 0.0

            if end_str.lower() in ["current", "present", "now", ""]:
                end = date.today()
            else:
                end = self._parse_date(end_str)
                if not end:
                    end = date.today()

            years = (end - start).days / 365.25
            return max(0.0, years)
        except Exception:
            return 0.0

    def _parse_date(self, date_str: str) -> Optional[date]:
        """Parse date from string."""
        if not date_str:
            return None

        # Try DD.MM.YYYY
        try:
            parts = date_str.strip().split(".")
            if len(parts) >= 3:
                return date(int(parts[2]), int(parts[1]), int(parts[0]))
        except Exception:
            pass

        # Try year only
        try:
            year = int(date_str.strip())
            if 1900 <= year <= 2100:
                return date(year, 1, 1)
        except Exception:
            pass

        return None

    def _get_seniority(self, occupation: str) -> int:
        """Get seniority level from occupation (0-6)."""
        occ_lower = occupation.lower()

        levels = {
            6: ["ceo", "cto", "cfo", "director", "vp", "president"],
            5: ["head", "chief", "principal", "partner"],
            4: ["senior manager", "senior director"],
            3: ["manager", "lead", "supervisor"],
            2: ["senior", "specialist", "analyst"],
            1: ["junior", "associate", "assistant", "intern"],
        }

        for level, keywords in levels.items():
            if any(kw in occ_lower for kw in keywords):
                return level
        return 0

    def _parse_language_level(self, level: str) -> int:
        """Parse language level to CEFR scale (0-6)."""
        level_lower = level.lower().strip()

        cefr = {"c2": 6, "c1": 5, "b2": 4, "b1": 3, "a2": 2, "a1": 1}
        for code, value in cefr.items():
            if code in level_lower:
                return value

        descriptive = {
            "native": 6,
            "fluent": 5,
            "advanced": 4,
            "intermediate": 3,
            "basic": 2,
            "beginner": 1,
        }
        for desc, value in descriptive.items():
            if desc in level_lower:
                return value

        return 0

    def _get_language_tier(self, language: str) -> int:
        """Get business value tier of language (1-3)."""
        lang_lower = language.lower()

        tier3 = ["english", "mandarin", "spanish", "arabic"]
        tier2 = ["french", "german", "japanese", "portuguese", "russian"]

        if any(t in lang_lower for t in tier3):
            return 3
        if any(t in lang_lower for t in tier2):
            return 2
        return 1


def extract_features(cv_data: dict, sector: str = "", sector_data: dict = None) -> list[float]:
    """
    Convenience function to extract features from CV data.

    Args:
        cv_data: Dictionary containing CV data
        sector: Target job sector
        sector_data: Job sectors dictionary

    Returns:
        List of numerical features
    """
    extractor = FeatureExtractor(sector_data)
    return extractor.extract(cv_data, sector)
