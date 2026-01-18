"""Tests for CV parser functionality."""

import os
import pytest
from persona2hire.cv.parser import (
    read_cv_file,
    validate_cv_data,
    get_cv_summary,
    _extract_value,
    _is_valid_email,
    _is_valid_date_format,
)


class TestReadCvFile:
    """Tests for the read_cv_file function."""

    def test_parses_sample_cv_correctly(self, sample_cv_file):
        """Test that a well-formed CV file is parsed correctly."""
        result = read_cv_file(sample_cv_file)

        assert result["FirstName"] == "Sarah"
        assert result["LastName"] == "Mitchell"
        assert result["City"] == "Munich"
        assert result["EmailAddress"] == "sarah.mitchell@email.com"
        assert result["Nationality"] == "German"

    def test_parses_work_experience(self, sample_cv_file):
        """Test that work experience sections are parsed correctly."""
        result = read_cv_file(sample_cv_file)

        assert result["Workplace1"] == "TechStart GmbH"
        assert "current" in result["Dates1"].lower()
        assert result["Occupation1"] == "Lead Developer"

        assert result["Workplace2"] == "WebAgency"
        assert result["Occupation2"] == "Web Developer"

    def test_parses_education(self, sample_cv_file):
        """Test that education fields are parsed correctly."""
        result = read_cv_file(sample_cv_file)

        assert "Ludwig" in result["College/University"]
        assert "Computer Science" in result["SubjectsStudied"]
        assert "Artificial Intelligence" in result["Master1"]

    def test_parses_skills(self, sample_cv_file):
        """Test that skills are parsed correctly."""
        result = read_cv_file(sample_cv_file)

        assert "Python" in result["ComputerSkills"]
        assert "TensorFlow" in result["ComputerSkills"]
        assert "Machine learning" in result["JobRelatedSkills"]

    def test_parses_languages(self, sample_cv_file):
        """Test that language fields are parsed correctly."""
        result = read_cv_file(sample_cv_file)

        assert result["MotherLanguage"] == "German"
        assert result["ModernLanguage1"] == "English"
        assert result["Level1"] == "C2"

    def test_parses_personality_fields(self, sample_cv_file):
        """Test that personality-related fields are parsed."""
        result = read_cv_file(sample_cv_file)

        assert "Creative" in result["ShortDescription"]
        assert "machine learning" in result["Hobbies"]

    def test_file_not_found_raises_error(self, temp_dir):
        """Test that missing file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            read_cv_file(os.path.join(temp_dir, "nonexistent.txt"))

    def test_handles_empty_fields(self, temp_dir):
        """Test parsing file with empty fields."""
        content = """Curriculum Vitae
First-Name : John
Last-Name :
City :
"""
        filepath = os.path.join(temp_dir, "empty_fields.txt")
        with open(filepath, "w") as f:
            f.write(content)

        result = read_cv_file(filepath)
        assert result["FirstName"] == "John"
        assert result["LastName"] == ""

    def test_handles_colons_in_values(self, temp_dir):
        """Test that colons within values are preserved."""
        content = """Curriculum Vitae
First-Name : John
E-mail Address : user@domain.com
Projects : Time: 2020-2021, Budget: $50k
"""
        filepath = os.path.join(temp_dir, "colon_test.txt")
        with open(filepath, "w") as f:
            f.write(content)

        result = read_cv_file(filepath)
        assert ":" in result["Projects"]
        assert "Time" in result["Projects"]


class TestValidateCvData:
    """Tests for the validate_cv_data function."""

    def test_valid_cv_passes(self, sample_cv_data):
        """Test that a valid CV passes validation."""
        is_valid, errors = validate_cv_data(sample_cv_data)
        assert is_valid is True
        assert len(errors) == 0

    def test_missing_first_name_fails(self):
        """Test that missing first name fails validation."""
        cv_data = {"FirstName": "", "LastName": "Doe"}
        is_valid, errors = validate_cv_data(cv_data)
        assert is_valid is False
        assert any("FirstName" in e for e in errors)

    def test_missing_last_name_fails(self):
        """Test that missing last name fails validation."""
        cv_data = {"FirstName": "John", "LastName": ""}
        is_valid, errors = validate_cv_data(cv_data)
        assert is_valid is False
        assert any("LastName" in e for e in errors)

    def test_invalid_email_fails(self):
        """Test that invalid email format fails validation."""
        cv_data = {
            "FirstName": "John",
            "LastName": "Doe",
            "EmailAddress": "invalid-email",
        }
        is_valid, errors = validate_cv_data(cv_data)
        assert is_valid is False
        assert any("email" in e.lower() for e in errors)

    def test_valid_email_passes(self):
        """Test various valid email formats."""
        valid_emails = [
            "user@domain.com",
            "user.name@domain.co.uk",
            "user+tag@domain.org",
            "user123@sub.domain.com",
        ]
        for email in valid_emails:
            cv_data = {"FirstName": "John", "LastName": "Doe", "EmailAddress": email}
            is_valid, errors = validate_cv_data(cv_data)
            assert is_valid is True, f"Email {email} should be valid"

    def test_invalid_date_format_fails(self):
        """Test that invalid date format fails validation."""
        cv_data = {
            "FirstName": "John",
            "LastName": "Doe",
            "DateOfBirth": "1990-03-15",  # Wrong format (ISO instead of DD.MM.YYYY)
        }
        is_valid, errors = validate_cv_data(cv_data)
        assert is_valid is False
        assert any("date" in e.lower() for e in errors)

    def test_valid_date_format_passes(self):
        """Test that valid date format passes validation."""
        cv_data = {
            "FirstName": "John",
            "LastName": "Doe",
            "DateOfBirth": "15.03.1990",
        }
        is_valid, errors = validate_cv_data(cv_data)
        assert is_valid is True


class TestGetCvSummary:
    """Tests for the get_cv_summary function."""

    def test_summary_contains_name(self, sample_cv_data):
        """Test that summary contains the person's name."""
        summary = get_cv_summary(sample_cv_data)
        assert "John" in summary
        assert "Doe" in summary

    def test_summary_shows_work_experience_count(self, sample_cv_data):
        """Test that summary shows correct work experience count."""
        summary = get_cv_summary(sample_cv_data)
        assert "2 work experience" in summary

    def test_summary_shows_language_count(self, sample_cv_data):
        """Test that summary shows correct language count."""
        summary = get_cv_summary(sample_cv_data)
        assert "3 language" in summary

    def test_minimal_cv_summary(self, minimal_cv_data):
        """Test summary for minimal CV data."""
        summary = get_cv_summary(minimal_cv_data)
        assert "Jane" in summary
        assert "Smith" in summary


class TestHelperFunctions:
    """Tests for parser helper functions."""

    def test_extract_value_basic(self):
        """Test basic value extraction."""
        assert _extract_value("First-Name : John") == "John"
        assert _extract_value("City: Berlin") == "Berlin"

    def test_extract_value_with_spaces(self):
        """Test value extraction with various spacing."""
        assert _extract_value("Name :   Value   ") == "Value"
        assert _extract_value("Name:Value") == "Value"

    def test_extract_value_preserves_colons(self):
        """Test that colons in value are preserved."""
        result = _extract_value("URL : http://example.com")
        assert "http://example.com" == result

    def test_is_valid_email_patterns(self):
        """Test email validation patterns."""
        assert _is_valid_email("user@domain.com") is True
        assert _is_valid_email("invalid") is False
        assert _is_valid_email("@domain.com") is False
        assert _is_valid_email("user@") is False
        assert _is_valid_email("") is False

    def test_is_valid_date_format(self):
        """Test date format validation."""
        assert _is_valid_date_format("15.03.1990") is True
        assert _is_valid_date_format("1.1.2000") is True
        assert _is_valid_date_format("1990-03-15") is False
        assert _is_valid_date_format("March 15, 1990") is False
        assert _is_valid_date_format("") is False
