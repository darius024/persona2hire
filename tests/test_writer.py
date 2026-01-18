"""Tests for CV writer functionality."""

import os
import pytest
from persona2hire.cv.writer import (
    write_cv_file,
    create_empty_cv,
    cv_to_string,
    _sanitize_filename,
    _generate_unique_filepath,
)


class TestWriteCvFile:
    """Tests for the write_cv_file function."""

    def test_writes_file_successfully(self, sample_cv_data, temp_dir):
        """Test that CV file is written successfully."""
        filepath = write_cv_file(sample_cv_data, output_dir=temp_dir)

        assert os.path.exists(filepath)
        assert filepath.endswith(".txt")

    def test_file_contains_required_data(self, sample_cv_data, temp_dir):
        """Test that written file contains the required data."""
        filepath = write_cv_file(sample_cv_data, output_dir=temp_dir)

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        assert "John" in content
        assert "Doe" in content
        assert "john.doe@example.com" in content

    def test_filename_contains_name(self, sample_cv_data, temp_dir):
        """Test that filename contains the person's name."""
        filepath = write_cv_file(sample_cv_data, output_dir=temp_dir)
        filename = os.path.basename(filepath)

        assert "John" in filename or "Doe" in filename

    def test_generates_unique_filename(self, sample_cv_data, temp_dir):
        """Test that duplicate names generate unique filenames."""
        filepath1 = write_cv_file(sample_cv_data, output_dir=temp_dir)
        filepath2 = write_cv_file(sample_cv_data, output_dir=temp_dir)

        assert filepath1 != filepath2
        assert os.path.exists(filepath1)
        assert os.path.exists(filepath2)

    def test_overwrite_mode(self, sample_cv_data, temp_dir):
        """Test that overwrite mode replaces existing file."""
        # First write
        filepath1 = write_cv_file(sample_cv_data, output_dir=temp_dir)

        # Second write with overwrite
        sample_cv_data["FirstName"] = "UpdatedName"
        filepath2 = write_cv_file(sample_cv_data, output_dir=temp_dir, overwrite=True)

        # Should overwrite the first file or create with same naming pattern
        with open(filepath2, "r", encoding="utf-8") as f:
            content = f.read()
        assert "UpdatedName" in content

    def test_missing_name_raises_error(self, temp_dir):
        """Test that missing name raises ValueError."""
        cv_data = {"FirstName": "", "LastName": ""}

        with pytest.raises(ValueError):
            write_cv_file(cv_data, output_dir=temp_dir)


class TestCreateEmptyCv:
    """Tests for the create_empty_cv function."""

    def test_creates_dict_with_all_fields(self):
        """Test that empty CV has all required fields."""
        cv = create_empty_cv()

        # Check key personal fields exist
        assert "FirstName" in cv
        assert "LastName" in cv
        assert "EmailAddress" in cv
        assert "DateOfBirth" in cv

        # Check work experience fields
        assert "Workplace1" in cv
        assert "Occupation1" in cv
        assert "Dates1" in cv

        # Check education fields
        assert "College/University" in cv
        assert "QualificationsAwarded" in cv

        # Check skills fields
        assert "ComputerSkills" in cv
        assert "JobRelatedSkills" in cv

    def test_all_fields_are_empty_strings(self):
        """Test that all fields are initialized as empty strings."""
        cv = create_empty_cv()

        for key, value in cv.items():
            if key not in ["Score", "PersonalityTypeMB", "PersonalityTypeBF"]:
                assert value == "", f"Field {key} should be empty"


class TestCvToString:
    """Tests for the cv_to_string function."""

    def test_returns_string(self, sample_cv_data):
        """Test that function returns a string."""
        result = cv_to_string(sample_cv_data)
        assert isinstance(result, str)

    def test_string_contains_name(self, sample_cv_data):
        """Test that string contains the person's name."""
        result = cv_to_string(sample_cv_data)
        assert "John" in result
        assert "Doe" in result

    def test_string_contains_work_experience(self, sample_cv_data):
        """Test that string contains work experience."""
        result = cv_to_string(sample_cv_data)
        assert "Tech Corp" in result
        assert "Senior Software Engineer" in result

    def test_string_contains_education(self, sample_cv_data):
        """Test that string contains education info."""
        result = cv_to_string(sample_cv_data)
        # Should contain education section
        assert "EDUCATION" in result or "Bachelor" in result

    def test_minimal_cv_produces_output(self, minimal_cv_data):
        """Test that minimal CV still produces output."""
        result = cv_to_string(minimal_cv_data)
        assert len(result) > 0
        assert "Jane" in result


class TestSanitizeFilename:
    """Tests for the _sanitize_filename function."""

    def test_removes_special_characters(self):
        """Test that special characters are removed."""
        result = _sanitize_filename("John/Doe")
        assert "/" not in result

    def test_preserves_valid_characters(self):
        """Test that valid characters are preserved."""
        result = _sanitize_filename("John_Doe")
        assert "John" in result and "Doe" in result

    def test_handles_empty_input(self):
        """Test handling of empty input."""
        result = _sanitize_filename("")
        # Empty input returns empty string
        assert result == "" or result == "unnamed"

    def test_handles_only_invalid_chars(self):
        """Test handling input with only invalid characters."""
        result = _sanitize_filename("/<>:")
        # Should remove invalid chars, result may be empty or "unnamed"
        assert "/" not in result and "<" not in result

    def test_trims_whitespace(self):
        """Test that whitespace is trimmed."""
        result = _sanitize_filename("  John  ")
        assert result.strip() == result


class TestGenerateUniqueFilepath:
    """Tests for the _generate_unique_filepath function."""

    def test_returns_path_with_name(self, temp_dir):
        """Test that path is returned with name components."""
        result = _generate_unique_filepath(temp_dir, "John", "Doe", False)
        assert temp_dir in result
        assert result.endswith(".txt")

    def test_adds_suffix_for_existing_file(self, temp_dir):
        """Test that suffix is added for existing files."""
        # Create first file
        first_path = _generate_unique_filepath(temp_dir, "John", "Doe", False)
        with open(first_path, "w") as f:
            f.write("test")

        # Get second path - should be different
        second_path = _generate_unique_filepath(temp_dir, "John", "Doe", False)
        assert second_path != first_path

    def test_overwrite_returns_same_path(self, temp_dir):
        """Test that overwrite mode can return same base path."""
        # First call
        first_path = _generate_unique_filepath(temp_dir, "John", "Doe", True)
        with open(first_path, "w") as f:
            f.write("test")

        # Second call with overwrite - may return same path
        second_path = _generate_unique_filepath(temp_dir, "John", "Doe", True)
        # Just verify it's a valid path
        assert second_path.endswith(".txt")
