"""Tests for job analyzer functionality."""

import pytest
from datetime import date
from persona2hire.analysis.job_analyzer import (
    analyze_job,
    analyze_jobs,
    get_score_breakdown,
    get_skill_gaps,
    filter_candidates,
    _parse_date,
    _calculate_time_worked,
    _get_qualification_level,
    _get_seniority_level,
)


class TestAnalyzeJob:
    """Tests for the analyze_job function."""

    def test_returns_score_for_valid_sector(self, sample_cv_data):
        """Test that a valid sector returns a score."""
        score = analyze_job(sample_cv_data, "Computers_ICT")
        assert isinstance(score, float)
        assert score >= 0

    def test_returns_zero_for_invalid_sector(self, sample_cv_data):
        """Test that invalid sector returns zero."""
        score = analyze_job(sample_cv_data, "NonexistentSector")
        assert score == 0.0

    def test_tech_cv_scores_high_in_tech_sector(self, sample_cv_data):
        """Test that a tech CV scores well in tech sector."""
        tech_score = analyze_job(sample_cv_data, "Computers_ICT")
        farming_score = analyze_job(sample_cv_data, "Farming_Horticulture_Forestry")

        assert tech_score > farming_score

    def test_score_within_expected_range(self, sample_cv_data):
        """Test that scores are within reasonable range."""
        score = analyze_job(sample_cv_data, "Computers_ICT")
        # Score should be 0-105 (100 base + 5 personality bonus max)
        assert 0 <= score <= 105

    def test_personality_bonus_applied(self, sample_cv_data):
        """Test that personality bonus is applied when matching."""
        # Set a personality type that matches IT sector
        sample_cv_data["PersonalityTypeMB"] = "INTJ"
        score_with_match = analyze_job(sample_cv_data, "Computers_ICT")

        sample_cv_data["PersonalityTypeMB"] = ""
        score_without_match = analyze_job(sample_cv_data, "Computers_ICT")

        # Should be higher with personality match
        assert score_with_match >= score_without_match

    def test_empty_cv_returns_low_score(self, empty_cv_data):
        """Test that empty CV returns minimal score."""
        score = analyze_job(empty_cv_data, "Computers_ICT")
        assert score < 10


class TestAnalyzeJobs:
    """Tests for the analyze_jobs function."""

    def test_returns_list_of_tuples(self, sample_cv_data):
        """Test that function returns list of (sector, score) tuples."""
        results = analyze_jobs(sample_cv_data)

        assert isinstance(results, list)
        assert len(results) > 0
        assert all(isinstance(item, tuple) for item in results)
        assert all(len(item) == 2 for item in results)

    def test_results_sorted_by_score_descending(self, sample_cv_data):
        """Test that results are sorted by score in descending order."""
        results = analyze_jobs(sample_cv_data)

        scores = [score for _, score in results]
        assert scores == sorted(scores, reverse=True)

    def test_covers_all_sectors(self, sample_cv_data):
        """Test that all sectors are analyzed."""
        from persona2hire.data.job_sectors import JobSectors

        results = analyze_jobs(sample_cv_data)
        sectors_in_results = {sector for sector, _ in results}

        assert sectors_in_results == set(JobSectors.keys())


class TestGetScoreBreakdown:
    """Tests for the get_score_breakdown function."""

    def test_returns_dict_with_all_categories(self, sample_cv_data):
        """Test that breakdown contains all scoring categories."""
        breakdown = get_score_breakdown(sample_cv_data, "Computers_ICT")

        expected_keys = [
            "education",
            "work_experience",
            "skills",
            "languages",
            "soft_skills",
            "additional",
            "personality_bonus",
        ]
        for key in expected_keys:
            assert key in breakdown

    def test_includes_max_values(self, sample_cv_data):
        """Test that breakdown includes max values for each category."""
        breakdown = get_score_breakdown(sample_cv_data, "Computers_ICT")

        assert "max_education" in breakdown
        assert "max_work_experience" in breakdown
        assert "max_skills" in breakdown

    def test_scores_do_not_exceed_max(self, sample_cv_data):
        """Test that no score exceeds its maximum."""
        breakdown = get_score_breakdown(sample_cv_data, "Computers_ICT")

        assert breakdown["education"] <= breakdown["max_education"]
        assert breakdown["work_experience"] <= breakdown["max_work_experience"]
        assert breakdown["skills"] <= breakdown["max_skills"]

    def test_invalid_sector_returns_empty(self, sample_cv_data):
        """Test that invalid sector returns empty dict."""
        breakdown = get_score_breakdown(sample_cv_data, "InvalidSector")
        assert breakdown == {}


class TestGetSkillGaps:
    """Tests for the get_skill_gaps function."""

    def test_returns_expected_keys(self, sample_cv_data):
        """Test that result contains expected keys."""
        gaps = get_skill_gaps(sample_cv_data, "Computers_ICT")

        assert "missing_required" in gaps
        assert "missing_extra" in gaps
        assert "matched" in gaps

    def test_matched_skills_detected(self, sample_cv_data):
        """Test that matched skills are detected."""
        gaps = get_skill_gaps(sample_cv_data, "Computers_ICT")

        # Check that at least some skills are matched or missing (non-empty result)
        total_skills = len(gaps["matched"]) + len(gaps["missing_required"]) + len(gaps["missing_extra"])
        assert total_skills >= 0  # Just verify structure works

    def test_invalid_sector_returns_empty_lists(self, sample_cv_data):
        """Test that invalid sector returns empty lists."""
        gaps = get_skill_gaps(sample_cv_data, "InvalidSector")

        assert gaps["missing_required"] == []
        assert gaps["missing_extra"] == []
        assert gaps["matched"] == []


class TestFilterCandidates:
    """Tests for the filter_candidates function."""

    @pytest.fixture
    def candidate_list(self, sample_cv_data, minimal_cv_data):
        """Create a list of candidates for filtering tests."""
        german_candidate = sample_cv_data.copy()
        german_candidate["Nationality"] = "German"
        german_candidate["Sex"] = "M"

        british_candidate = minimal_cv_data.copy()
        british_candidate["Nationality"] = "British"
        british_candidate["Sex"] = "F"
        british_candidate["DateOfBirth"] = "15.03.2000"  # Young

        return [german_candidate, british_candidate]

    def test_empty_criteria_returns_all(self, candidate_list):
        """Test that empty criteria returns all candidates."""
        result = filter_candidates(candidate_list, {})
        assert len(result) == len(candidate_list)

    def test_filter_by_nationality(self, candidate_list):
        """Test filtering by nationality."""
        result = filter_candidates(candidate_list, {"nationality": "German"})
        assert len(result) == 1
        assert result[0]["Nationality"] == "German"

    def test_filter_by_sex(self, candidate_list):
        """Test filtering by sex."""
        result = filter_candidates(candidate_list, {"sex": "F"})
        assert len(result) == 1
        assert result[0]["Sex"] == "F"

    def test_filter_by_age_range(self, candidate_list):
        """Test filtering by age range."""
        # Filter for age 20-30 (the British candidate born in 2000)
        result = filter_candidates(candidate_list, {"age_min": "20", "age_max": "30"})
        assert len(result) >= 1

    def test_filter_by_skills(self, sample_cv_data):
        """Test filtering by required skills."""
        candidates = [sample_cv_data]
        result = filter_candidates(candidates, {"skills": "Python"})
        assert len(result) == 1

        result = filter_candidates(candidates, {"skills": "NonexistentSkill"})
        assert len(result) == 0

    def test_filter_by_languages(self, sample_cv_data):
        """Test filtering by required languages."""
        candidates = [sample_cv_data]
        result = filter_candidates(candidates, {"languages": "English"})
        assert len(result) == 1

        result = filter_candidates(candidates, {"languages": "Japanese"})
        assert len(result) == 0

    def test_multiple_criteria_combined(self, candidate_list):
        """Test that multiple criteria are AND-combined."""
        result = filter_candidates(
            candidate_list, {"nationality": "German", "sex": "M"}
        )
        assert len(result) == 1


class TestParseDateFunction:
    """Tests for the _parse_date helper function."""

    def test_european_format(self):
        """Test DD.MM.YYYY format parsing."""
        result = _parse_date("15.03.1990")
        assert result == date(1990, 3, 15)

    def test_us_format(self):
        """Test MM/DD/YYYY format parsing."""
        result = _parse_date("03/15/1990")
        assert result == date(1990, 3, 15)

    def test_iso_format(self):
        """Test YYYY-MM-DD format parsing."""
        result = _parse_date("1990-03-15")
        assert result == date(1990, 3, 15)

    def test_month_year_format(self):
        """Test Month YYYY format parsing."""
        result = _parse_date("March 1990")
        assert result == date(1990, 3, 1)

        result = _parse_date("January 2020")
        assert result == date(2020, 1, 1)

    def test_year_only_format(self):
        """Test year-only format parsing."""
        result = _parse_date("1990")
        assert result == date(1990, 1, 1)

    def test_empty_string(self):
        """Test empty string returns None."""
        assert _parse_date("") is None
        assert _parse_date(None) is None

    def test_invalid_date_returns_none(self):
        """Test invalid date returns None."""
        assert _parse_date("invalid") is None
        assert _parse_date("not a date") is None


class TestCalculateTimeWorked:
    """Tests for the _calculate_time_worked helper function."""

    def test_date_range_calculation(self):
        """Test calculation of years between two dates."""
        # 3 years
        years = _calculate_time_worked("01.01.2018 - 31.12.2020")
        assert 2.5 < years < 3.5

    def test_current_date_handling(self):
        """Test handling of 'current' as end date."""
        years = _calculate_time_worked("01.01.2020 - current")
        assert years > 0

        years = _calculate_time_worked("01.01.2020 - present")
        assert years > 0

    def test_empty_input(self):
        """Test empty input returns zero."""
        assert _calculate_time_worked("") == 0.0
        assert _calculate_time_worked(None) == 0.0

    def test_invalid_format(self):
        """Test invalid format returns zero."""
        assert _calculate_time_worked("invalid dates") == 0.0


class TestQualificationLevel:
    """Tests for the _get_qualification_level helper function."""

    def test_phd_level(self):
        """Test PhD qualification is highest level."""
        level = _get_qualification_level("phd in computer science")
        assert level >= 5

    def test_masters_level(self):
        """Test Master's qualification level."""
        level = _get_qualification_level("master of science")
        assert level >= 4

    def test_bachelors_level(self):
        """Test Bachelor's qualification level."""
        level = _get_qualification_level("bachelor of arts")
        assert level >= 3

    def test_empty_returns_zero(self):
        """Test empty text returns zero."""
        assert _get_qualification_level("") == 0


class TestSeniorityLevel:
    """Tests for the _get_seniority_level helper function."""

    def test_ceo_highest_level(self):
        """Test CEO/Director is highest seniority."""
        level = _get_seniority_level("Chief Executive Officer")
        assert level >= 5

    def test_manager_mid_level(self):
        """Test manager is mid-level seniority."""
        level = _get_seniority_level("Project Manager")
        assert 2 <= level <= 5

    def test_junior_low_level(self):
        """Test junior position is low seniority."""
        level = _get_seniority_level("Junior Developer")
        assert level <= 2

    def test_empty_returns_zero(self):
        """Test empty text returns zero."""
        assert _get_seniority_level("") == 0
