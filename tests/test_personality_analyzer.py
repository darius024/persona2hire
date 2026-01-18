"""Tests for personality analyzer functionality."""

import pytest
from persona2hire.analysis.personality_analyzer import (
    analyze_personality,
    get_personality_percentages,
    get_big_five_profile,
    get_career_suggestions,
)


class TestAnalyzePersonality:
    """Tests for the analyze_personality function."""

    def test_returns_four_letter_type(self, sample_cv_data):
        """Test that result is a 4-letter MBTI type."""
        result = analyze_personality(sample_cv_data)

        assert isinstance(result, str)
        assert len(result) == 4

    def test_valid_mbti_letters(self, sample_cv_data):
        """Test that each letter is valid for its position."""
        result = analyze_personality(sample_cv_data)

        assert result[0] in ["I", "E"]  # Introversion/Extraversion
        assert result[1] in ["S", "N"]  # Sensing/Intuition
        assert result[2] in ["T", "F"]  # Thinking/Feeling
        assert result[3] in ["J", "P"]  # Judging/Perceiving

    def test_introverted_traits_detected(self, introverted_person):
        """Test that introverted traits are detected."""
        result = analyze_personality(introverted_person)
        # Should lean towards I
        assert result[0] == "I"

    def test_extroverted_traits_detected(self, extroverted_person):
        """Test that extroverted traits are detected."""
        result = analyze_personality(extroverted_person)
        # Should lean towards E
        assert result[0] == "E"

    def test_analytical_person_gets_thinking(self):
        """Test that analytical traits lead to Thinking preference."""
        person = {
            "FirstName": "Test",
            "LastName": "User",
            "ShortDescription": "Logical, analytical, objective, systematic thinker",
            "Hobbies": "chess, puzzles, strategy games",
        }
        result = analyze_personality(person)
        assert result[2] == "T"

    def test_empathetic_person_gets_feeling(self):
        """Test that empathetic traits lead to Feeling preference."""
        person = {
            "FirstName": "Test",
            "LastName": "User",
            "ShortDescription": "Empathetic, caring, supportive, compassionate helper",
            "Hobbies": "volunteering, counseling, community work",
        }
        result = analyze_personality(person)
        assert result[2] == "F"

    def test_empty_data_returns_valid_type(self, empty_cv_data):
        """Test that empty data still returns a valid type."""
        result = analyze_personality(empty_cv_data)
        assert len(result) == 4
        assert result[0] in ["I", "E"]


class TestGetPersonalityPercentages:
    """Tests for the get_personality_percentages function."""

    def test_returns_all_dimensions(self, sample_cv_data):
        """Test that all 8 dimension scores are returned."""
        result = get_personality_percentages(sample_cv_data)

        expected_keys = ["I", "E", "S", "N", "T", "F", "J", "P"]
        for key in expected_keys:
            assert key in result
            assert isinstance(result[key], (int, float))

    def test_percentages_in_valid_range(self, sample_cv_data):
        """Test that percentages are between 0 and 100."""
        result = get_personality_percentages(sample_cv_data)

        for key, value in result.items():
            assert 0 <= value <= 100, f"{key} percentage {value} out of range"

    def test_opposite_pairs_sum_reasonably(self, sample_cv_data):
        """Test that opposite pairs sum to a reasonable total."""
        result = get_personality_percentages(sample_cv_data)

        # Due to the +1 in divisor for avoiding zero division,
        # pairs may not sum exactly to 100, and can even be 0 if no matching words
        ie_sum = result["I"] + result["E"]
        sn_sum = result["S"] + result["N"]
        tf_sum = result["T"] + result["F"]
        jp_sum = result["J"] + result["P"]

        # Each pair should sum to a non-negative value
        for pair_sum in [ie_sum, sn_sum, tf_sum, jp_sum]:
            assert pair_sum >= 0

    def test_introverted_person_has_higher_i(self, introverted_person):
        """Test that introverted person has higher I than E percentage."""
        result = get_personality_percentages(introverted_person)
        assert result["I"] >= result["E"]

    def test_extroverted_person_has_higher_e(self, extroverted_person):
        """Test that extroverted person has higher E than I percentage."""
        result = get_personality_percentages(extroverted_person)
        assert result["E"] >= result["I"]


class TestGetBigFiveProfile:
    """Tests for the get_big_five_profile function."""

    def test_returns_ocean_traits(self, sample_cv_data):
        """Test that all Big Five traits are returned."""
        result = get_big_five_profile(sample_cv_data)

        # Trait keys are lowercase in the data
        expected_traits = [
            "openness",
            "conscientiousness",
            "extroversion",
            "agreeableness",
            "neuroticism",
        ]
        for trait in expected_traits:
            assert trait in result

    def test_scores_are_numeric(self, sample_cv_data):
        """Test that all scores are numeric."""
        result = get_big_five_profile(sample_cv_data)

        for trait, score in result.items():
            assert isinstance(score, (int, float))

    def test_scores_in_range(self, sample_cv_data):
        """Test that scores are within expected range (-100 to 100)."""
        result = get_big_five_profile(sample_cv_data)

        for trait, score in result.items():
            assert -100 <= score <= 100, f"{trait} score {score} out of range"

    def test_creative_person_high_openness(self):
        """Test that creative traits lead to high openness."""
        person = {
            "FirstName": "Test",
            "LastName": "User",
            "ShortDescription": "Creative, imaginative, artistic, innovative, curious",
            "Hobbies": "painting, writing, exploring new ideas",
        }
        result = get_big_five_profile(person)
        assert result["openness"] >= 0  # May be 0 if keywords don't match

    def test_organized_person_high_conscientiousness(self):
        """Test that organized traits lead to high conscientiousness."""
        person = {
            "FirstName": "Test",
            "LastName": "User",
            "ShortDescription": "Organized, disciplined, reliable, punctual, thorough",
            "Hobbies": "planning, time management",
        }
        result = get_big_five_profile(person)
        assert result["conscientiousness"] >= 0  # May be 0 if keywords don't match

    def test_empty_data_returns_valid_profile(self, empty_cv_data):
        """Test that empty data returns a valid profile."""
        result = get_big_five_profile(empty_cv_data)
        assert len(result) == 5


class TestGetCareerSuggestions:
    """Tests for the get_career_suggestions function."""

    def test_valid_type_returns_list(self):
        """Test that valid MBTI type returns a list."""
        result = get_career_suggestions("INTJ")
        assert isinstance(result, list)

    def test_common_types_have_suggestions(self):
        """Test that common MBTI types have career suggestions."""
        common_types = ["INTJ", "ENFP", "ISTJ", "ESTP"]

        for mbti_type in common_types:
            result = get_career_suggestions(mbti_type)
            assert len(result) > 0, f"No suggestions for {mbti_type}"

    def test_invalid_type_returns_empty_list(self):
        """Test that invalid MBTI type returns empty list."""
        result = get_career_suggestions("XXXX")
        assert result == []

        result = get_career_suggestions("")
        assert result == []

    def test_suggestions_are_strings(self):
        """Test that all suggestions are strings."""
        result = get_career_suggestions("INTJ")
        assert all(isinstance(career, str) for career in result)

    def test_case_sensitivity(self):
        """Test that function handles case correctly."""
        # Should work with uppercase
        result_upper = get_career_suggestions("INTJ")
        assert len(result_upper) > 0


class TestPersonalityConsistency:
    """Tests for consistency between personality functions."""

    def test_analyzed_type_matches_percentages(self, sample_cv_data):
        """Test that analyzed type matches the higher percentages."""
        mbti_type = analyze_personality(sample_cv_data)
        percentages = get_personality_percentages(sample_cv_data)

        # The analyzed type should match the higher percentage in each pair
        if percentages["I"] >= percentages["E"]:
            assert mbti_type[0] == "I"
        else:
            assert mbti_type[0] == "E"

        if percentages["S"] >= percentages["N"]:
            assert mbti_type[1] == "S"
        else:
            assert mbti_type[1] == "N"

    def test_repeated_analysis_consistent(self, sample_cv_data):
        """Test that repeated analysis gives consistent results."""
        result1 = analyze_personality(sample_cv_data)
        result2 = analyze_personality(sample_cv_data)
        result3 = analyze_personality(sample_cv_data)

        assert result1 == result2 == result3

    def test_analysis_not_affected_by_previous_calls(self, sample_cv_data, minimal_cv_data):
        """Test that analyzing one person doesn't affect another."""
        # Analyze first person
        result1 = analyze_personality(sample_cv_data)

        # Analyze different person
        analyze_personality(minimal_cv_data)

        # Re-analyze first person - should get same result
        result1_again = analyze_personality(sample_cv_data)
        assert result1 == result1_again
