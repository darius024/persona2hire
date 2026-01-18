"""Tests for Machine Learning module."""

import os
import pytest
from persona2hire.ml.feature_extractor import FeatureExtractor, extract_features
from persona2hire.ml.data_generator import generate_synthetic_cv, generate_training_data
from persona2hire.ml.model import ScoringModel, save_model, load_model
from persona2hire.ml.feedback import FeedbackCollector, save_feedback, load_feedback
from persona2hire.ml.pipeline import MLPipeline, PipelineConfig


class TestFeatureExtractor:
    """Tests for the feature extractor."""

    def test_extracts_correct_number_of_features(self, sample_cv_data):
        """Test that correct number of features are extracted."""
        features = extract_features(sample_cv_data, "Computers_ICT")
        assert len(features) == len(FeatureExtractor.FEATURE_NAMES)
        assert len(features) == 31

    def test_all_features_are_numeric(self, sample_cv_data):
        """Test that all features are numeric."""
        features = extract_features(sample_cv_data)
        for f in features:
            assert isinstance(f, (int, float))

    def test_features_in_reasonable_range(self, sample_cv_data):
        """Test that features are in reasonable ranges."""
        features = extract_features(sample_cv_data)
        for f in features:
            assert f >= 0  # No negative features
            assert f <= 100  # No extreme values

    def test_empty_cv_produces_valid_features(self, empty_cv_data):
        """Test that empty CV still produces valid features."""
        features = extract_features(empty_cv_data)
        assert len(features) == 31
        assert all(isinstance(f, (int, float)) for f in features)


class TestDataGenerator:
    """Tests for the synthetic data generator."""

    def test_generates_valid_cv(self):
        """Test that generated CV has all required fields."""
        cv = generate_synthetic_cv()

        assert cv.get("FirstName")
        assert cv.get("LastName")
        assert cv.get("EmailAddress")
        assert "@" in cv["EmailAddress"]

    def test_sector_specific_generation(self):
        """Test that sector affects CV content."""
        tech_cv = generate_synthetic_cv(target_sector="Computers_ICT", seed=42)
        finance_cv = generate_synthetic_cv(target_sector="Banking_Finance_Insurance", seed=42)

        # Tech CV should have tech skills
        tech_skills = tech_cv.get("ComputerSkills", "").lower()
        finance_skills = finance_cv.get("ComputerSkills", "").lower()

        # They should be different based on sector
        assert tech_cv["QualificationsAwarded"] != finance_cv["QualificationsAwarded"]

    def test_expected_score_affects_quality(self):
        """Test that expected score affects CV quality."""
        low_cv = generate_synthetic_cv(expected_score=20, seed=1)
        high_cv = generate_synthetic_cv(expected_score=90, seed=2)

        # High score CV should have more experience
        high_positions = sum(1 for i in [1, 2, 3] if high_cv.get(f"Workplace{i}"))
        low_positions = sum(1 for i in [1, 2, 3] if low_cv.get(f"Workplace{i}"))

        assert high_positions >= low_positions

    def test_seed_reproducibility(self):
        """Test that same seed produces same CV."""
        cv1 = generate_synthetic_cv(seed=123)
        cv2 = generate_synthetic_cv(seed=123)

        assert cv1["FirstName"] == cv2["FirstName"]
        assert cv1["LastName"] == cv2["LastName"]

    def test_generate_training_data_creates_list(self):
        """Test that training data generation works."""
        data = generate_training_data(num_samples=10)

        assert len(data) == 10
        assert all("cv" in item for item in data)
        assert all("sector" in item for item in data)
        assert all("expected_score" in item for item in data)


class TestScoringModel:
    """Tests for the scoring model."""

    @pytest.fixture
    def training_data(self):
        """Generate training data for model tests."""
        data = generate_training_data(num_samples=50)

        X = []
        y = []
        for item in data:
            features = extract_features(item["cv"], item["sector"])
            X.append(features)
            y.append(item["expected_score"])

        return X, y

    def test_model_trains_successfully(self, training_data):
        """Test that model trains without error."""
        X, y = training_data
        model = ScoringModel(use_sklearn=False)  # Use simple model for speed
        metrics = model.train(X, y)

        assert model.is_trained
        assert metrics.training_samples == len(X)
        assert metrics.mae >= 0

    def test_trained_model_predicts(self, training_data):
        """Test that trained model can predict."""
        X, y = training_data
        model = ScoringModel(use_sklearn=False)
        model.train(X, y)

        predictions = model.predict(X[:5])
        assert len(predictions) == 5
        assert all(0 <= p <= 100 for p in predictions)

    def test_untrained_model_raises_error(self):
        """Test that untrained model raises error on predict."""
        model = ScoringModel()

        with pytest.raises(ValueError):
            model.predict([[0.5] * 31])

    def test_model_save_load(self, training_data, temp_dir):
        """Test that model can be saved and loaded."""
        X, y = training_data
        model = ScoringModel(use_sklearn=False)
        model.train(X, y)

        # Save
        model_path = os.path.join(temp_dir, "test_model.json")
        save_model(model, model_path)

        # Load
        loaded = load_model(model_path)

        assert loaded.is_trained
        assert loaded.metrics.mae == model.metrics.mae

    def test_adjustment_factor_reasonable(self, training_data):
        """Test that adjustment factor is reasonable."""
        X, y = training_data
        model = ScoringModel(use_sklearn=False)
        model.train(X, y)

        factor = model.get_adjustment_factor(X[0], 50.0)
        # Factor should be between 0.7 and 1.3 (±30%)
        assert 0.7 <= factor <= 1.3


class TestFeedbackCollector:
    """Tests for the feedback collector."""

    def test_add_feedback(self, sample_cv_data, temp_dir):
        """Test adding feedback entries."""
        collector = FeedbackCollector(temp_dir)

        entry = collector.add_feedback(
            cv_data=sample_cv_data,
            sector="Computers_ICT",
            predicted_score=75.0,
            features=[0.5] * 31,
            actual_score=80.0,
        )

        assert len(collector.entries) == 1
        assert entry.predicted_score == 75.0
        assert entry.actual_score == 80.0

    def test_get_training_data(self, sample_cv_data, temp_dir):
        """Test extracting training data from feedback."""
        collector = FeedbackCollector(temp_dir)

        # Add feedback with actual score
        collector.add_feedback(
            cv_data=sample_cv_data,
            sector="Computers_ICT",
            predicted_score=75.0,
            features=[0.5] * 31,
            actual_score=80.0,
        )

        X, y = collector.get_training_data()
        assert len(X) == 1
        assert len(y) == 1
        assert y[0] == 80.0

    def test_save_load_feedback(self, sample_cv_data, temp_dir):
        """Test saving and loading feedback."""
        collector = FeedbackCollector(temp_dir)
        collector.add_feedback(
            cv_data=sample_cv_data,
            sector="Computers_ICT",
            predicted_score=75.0,
            features=[0.5] * 31,
        )

        # Save
        filepath = os.path.join(temp_dir, "test_feedback.json")
        save_feedback(collector, filepath)

        # Load
        loaded = load_feedback(filepath)
        assert len(loaded.entries) == 1

    def test_statistics(self, sample_cv_data, temp_dir):
        """Test feedback statistics."""
        collector = FeedbackCollector(temp_dir)

        collector.add_feedback(
            cv_data=sample_cv_data,
            sector="Computers_ICT",
            predicted_score=75.0,
            features=[0.5] * 31,
            was_hired=True,
        )

        stats = collector.get_statistics()
        assert stats["total_entries"] == 1
        assert stats["candidates_hired"] == 1


class TestMLPipeline:
    """Tests for the ML pipeline."""

    def test_pipeline_initializes(self, temp_dir):
        """Test that pipeline initializes correctly."""
        config = PipelineConfig(
            model_dir=os.path.join(temp_dir, "models"),
            feedback_dir=os.path.join(temp_dir, "feedback"),
            training_dir=os.path.join(temp_dir, "training"),
        )
        pipeline = MLPipeline(config=config)

        assert pipeline is not None
        assert pipeline.model is None  # No model trained yet

    def test_train_initial_model(self, temp_dir):
        """Test training initial model."""
        config = PipelineConfig(
            model_dir=os.path.join(temp_dir, "models"),
            feedback_dir=os.path.join(temp_dir, "feedback"),
            training_dir=os.path.join(temp_dir, "training"),
            use_sklearn=False,  # Faster for tests
        )
        pipeline = MLPipeline(config=config)

        metrics = pipeline.train_initial_model(num_synthetic_samples=50)

        assert pipeline.model is not None
        assert pipeline.model.is_trained
        assert metrics.mae >= 0

    def test_predict_score(self, sample_cv_data, temp_dir):
        """Test predicting score after training."""
        config = PipelineConfig(
            model_dir=os.path.join(temp_dir, "models"),
            feedback_dir=os.path.join(temp_dir, "feedback"),
            training_dir=os.path.join(temp_dir, "training"),
            use_sklearn=False,
        )
        pipeline = MLPipeline(config=config)
        pipeline.train_initial_model(num_synthetic_samples=50)

        score = pipeline.predict_score(sample_cv_data, "Computers_ICT")

        assert 0 <= score <= 100

    def test_get_adjusted_score(self, sample_cv_data, temp_dir):
        """Test getting adjusted score."""
        config = PipelineConfig(
            model_dir=os.path.join(temp_dir, "models"),
            feedback_dir=os.path.join(temp_dir, "feedback"),
            training_dir=os.path.join(temp_dir, "training"),
            use_sklearn=False,
        )
        pipeline = MLPipeline(config=config)
        pipeline.train_initial_model(num_synthetic_samples=50)

        adjusted = pipeline.get_adjusted_score(sample_cv_data, "Computers_ICT", 70.0)

        # Should be within ±30% of base score
        assert 49 <= adjusted <= 91

    def test_model_status(self, temp_dir):
        """Test getting model status."""
        config = PipelineConfig(
            model_dir=os.path.join(temp_dir, "models"),
            feedback_dir=os.path.join(temp_dir, "feedback"),
            training_dir=os.path.join(temp_dir, "training"),
            use_sklearn=False,
        )
        pipeline = MLPipeline(config=config)

        status = pipeline.get_model_status()

        assert "model_trained" in status
        assert "feedback_count" in status
        assert status["model_trained"] is False

        # Train and check again
        pipeline.train_initial_model(num_synthetic_samples=30)
        status = pipeline.get_model_status()

        assert status["model_trained"] is True
        assert "model_mae" in status
