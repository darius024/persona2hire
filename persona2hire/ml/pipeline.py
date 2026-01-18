"""End-to-end ML pipeline for model training, inference, and retraining."""

import json
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .feature_extractor import FeatureExtractor, extract_features
from .model import ScoringModel, save_model, load_model, ModelMetrics
from .feedback import FeedbackCollector, save_feedback, load_feedback
from .data_generator import generate_training_data


@dataclass
class PipelineConfig:
    """Configuration for the ML pipeline."""

    model_dir: str = "data/models"
    feedback_dir: str = "data/feedback"
    training_dir: str = "data/training"
    min_samples_for_training: int = 50
    retrain_threshold: float = 15.0  # Retrain if MAE exceeds this
    use_sklearn: bool = True


class MLPipeline:
    """
    End-to-end machine learning pipeline for adaptive scoring.

    Features:
    - Automatic feature extraction from CV data
    - Model training on synthetic and real data
    - Score prediction and adjustment
    - Feedback collection for continuous learning
    - Periodic retraining based on feedback
    """

    def __init__(self, config: Optional[PipelineConfig] = None, sector_data: Optional[dict] = None):
        """
        Initialize the ML pipeline.

        Args:
            config: Pipeline configuration
            sector_data: Job sectors dictionary for feature extraction
        """
        self.config = config or PipelineConfig()
        self.sector_data = sector_data or {}

        # Initialize components
        self.feature_extractor = FeatureExtractor(sector_data)
        self.model: Optional[ScoringModel] = None
        self.feedback_collector = FeedbackCollector(self.config.feedback_dir)

        # Ensure directories exist
        os.makedirs(self.config.model_dir, exist_ok=True)
        os.makedirs(self.config.feedback_dir, exist_ok=True)
        os.makedirs(self.config.training_dir, exist_ok=True)

        # Try to load existing model
        self._load_latest_model()

        # Try to load existing feedback
        try:
            self.feedback_collector.load()
        except Exception:
            pass

    def _load_latest_model(self):
        """Load the most recent model if available."""
        model_path = os.path.join(self.config.model_dir, "scoring_model.json")
        if os.path.exists(model_path):
            try:
                self.model = load_model(model_path)
            except Exception:
                self.model = None

    def train_initial_model(self, num_synthetic_samples: int = 200) -> ModelMetrics:
        """
        Train the initial model on synthetic data.

        Args:
            num_synthetic_samples: Number of synthetic CVs to generate

        Returns:
            Training metrics
        """
        print(f"Generating {num_synthetic_samples} synthetic training samples...")

        # Generate synthetic training data
        training_data = generate_training_data(
            num_samples=num_synthetic_samples,
            output_dir=self.config.training_dir,
        )

        # Extract features and prepare training data
        X = []
        y = []

        for item in training_data:
            cv = item["cv"]
            sector = item["sector"]
            expected_score = item["expected_score"]

            features = extract_features(cv, sector, self.sector_data)
            X.append(features)
            y.append(expected_score)

        print(f"Training model on {len(X)} samples...")

        # Train model
        self.model = ScoringModel(use_sklearn=self.config.use_sklearn)
        metrics = self.model.train(X, y, feature_names=FeatureExtractor.FEATURE_NAMES)

        # Save model
        model_path = os.path.join(self.config.model_dir, "scoring_model.json")
        save_model(self.model, model_path)

        print(f"Model trained. MAE: {metrics.mae:.2f}, R²: {metrics.r2:.2f}")

        return metrics

    def predict_score(self, cv_data: dict, sector: str) -> float:
        """
        Predict score for a CV-sector match.

        Args:
            cv_data: CV data dictionary
            sector: Target job sector

        Returns:
            Predicted score
        """
        if self.model is None or not self.model.is_trained:
            raise ValueError("Model not trained. Call train_initial_model() first.")

        features = extract_features(cv_data, sector, self.sector_data)
        return self.model.predict_single(features)

    def get_adjusted_score(self, cv_data: dict, sector: str, base_score: float) -> float:
        """
        Get ML-adjusted score based on rule-based base score.

        The ML model adjusts the rule-based score rather than replacing it,
        providing a hybrid approach that combines domain knowledge with
        learned patterns.

        Args:
            cv_data: CV data dictionary
            sector: Target job sector
            base_score: Score from rule-based system

        Returns:
            Adjusted score
        """
        if self.model is None or not self.model.is_trained:
            return base_score  # No adjustment if not trained

        features = extract_features(cv_data, sector, self.sector_data)
        adjustment = self.model.get_adjustment_factor(features, base_score)

        adjusted = base_score * adjustment
        return max(0.0, min(100.0, adjusted))

    def record_feedback(
        self,
        cv_data: dict,
        sector: str,
        predicted_score: float,
        actual_score: Optional[float] = None,
        was_hired: Optional[bool] = None,
        user_rating: Optional[int] = None,
        notes: str = "",
    ):
        """
        Record feedback for a prediction.

        Args:
            cv_data: CV data that was analyzed
            sector: Job sector
            predicted_score: Score that was predicted
            actual_score: Correct score (if known)
            was_hired: Whether candidate was hired (if known)
            user_rating: User's rating of prediction (1-5)
            notes: Additional notes
        """
        features = extract_features(cv_data, sector, self.sector_data)

        self.feedback_collector.add_feedback(
            cv_data=cv_data,
            sector=sector,
            predicted_score=predicted_score,
            features=features,
            actual_score=actual_score,
            was_hired=was_hired,
            user_rating=user_rating,
            notes=notes,
        )

        # Auto-save feedback
        self.feedback_collector.save()

    def should_retrain(self) -> bool:
        """
        Check if model should be retrained based on feedback.

        Returns:
            True if retraining is recommended
        """
        stats = self.feedback_collector.get_statistics()

        # Need minimum feedback samples
        if stats["entries_with_actual_score"] < self.config.min_samples_for_training:
            return False

        # Check average error
        if stats["average_prediction_error"] > self.config.retrain_threshold:
            return True

        return False

    def retrain_with_feedback(self) -> Optional[ModelMetrics]:
        """
        Retrain model using collected feedback data.

        Combines synthetic data with real feedback for improved accuracy.

        Returns:
            Training metrics if successful, None otherwise
        """
        # Get feedback data
        feedback_X, feedback_y = self.feedback_collector.get_training_data()

        if len(feedback_X) < 10:
            print("Not enough feedback data for retraining")
            return None

        # Load or generate synthetic data
        synthetic_path = os.path.join(self.config.training_dir, "training_data.json")
        synthetic_X = []
        synthetic_y = []

        if os.path.exists(synthetic_path):
            with open(synthetic_path, "r") as f:
                synthetic_data = json.load(f)
            for item in synthetic_data:
                features = extract_features(item["cv"], item["sector"], self.sector_data)
                synthetic_X.append(features)
                synthetic_y.append(item["expected_score"])

        # Combine datasets (weight feedback higher)
        X = []
        y = []

        # Add synthetic data
        for i in range(len(synthetic_X)):
            X.append(synthetic_X[i])
            y.append(synthetic_y[i])

        # Add feedback data (with weight of 2x)
        for i in range(len(feedback_X)):
            X.append(feedback_X[i])
            y.append(feedback_y[i])
            # Duplicate for higher weight
            X.append(feedback_X[i])
            y.append(feedback_y[i])

        print(f"Retraining with {len(X)} samples ({len(feedback_X)} from feedback)...")

        # Train new model
        new_model = ScoringModel(use_sklearn=self.config.use_sklearn)
        metrics = new_model.train(X, y, feature_names=FeatureExtractor.FEATURE_NAMES)

        # Save new model with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(self.config.model_dir, f"scoring_model_{timestamp}.json")
        save_model(new_model, backup_path)

        # Update main model
        self.model = new_model
        model_path = os.path.join(self.config.model_dir, "scoring_model.json")
        save_model(self.model, model_path)

        print(f"Model retrained. MAE: {metrics.mae:.2f}, R²: {metrics.r2:.2f}")

        return metrics

    def get_feature_importance(self) -> dict[str, float]:
        """
        Get feature importance from trained model.

        Returns:
            Dictionary mapping feature names to importance scores
        """
        if self.model is None or not self.model.is_trained:
            return {}

        return self.model.metrics.feature_importances

    def get_weight_recommendations(self) -> dict[str, float]:
        """
        Get recommended weight adjustments for rule-based scoring.

        Based on ML model's learned feature importances.

        Returns:
            Dictionary mapping score categories to recommended adjustments
        """
        if self.model is None or not self.model.is_trained:
            return {}

        return self.model.get_weight_adjustments()

    def get_model_status(self) -> dict:
        """
        Get current status of the ML pipeline.

        Returns:
            Dictionary with pipeline status information
        """
        status = {
            "model_trained": self.model is not None and self.model.is_trained,
            "feedback_count": len(self.feedback_collector.entries),
            "should_retrain": self.should_retrain(),
        }

        if self.model and self.model.is_trained:
            status.update({
                "model_mae": self.model.metrics.mae,
                "model_r2": self.model.metrics.r2,
                "training_samples": self.model.metrics.training_samples,
                "training_date": self.model.metrics.training_date,
            })

        stats = self.feedback_collector.get_statistics()
        status["feedback_stats"] = stats

        return status

    def export_pipeline_state(self, output_dir: str):
        """
        Export complete pipeline state for backup or transfer.

        Args:
            output_dir: Directory to export to
        """
        os.makedirs(output_dir, exist_ok=True)

        # Export model
        if self.model and self.model.is_trained:
            model_path = os.path.join(output_dir, "model.json")
            save_model(self.model, model_path)

        # Export feedback
        feedback_path = os.path.join(output_dir, "feedback.json")
        save_feedback(self.feedback_collector, feedback_path)

        # Export status
        status = self.get_model_status()
        status_path = os.path.join(output_dir, "pipeline_status.json")
        with open(status_path, "w") as f:
            json.dump(status, f, indent=2)

        print(f"Pipeline state exported to {output_dir}")

    def import_pipeline_state(self, input_dir: str):
        """
        Import pipeline state from backup.

        Args:
            input_dir: Directory to import from
        """
        # Import model
        model_path = os.path.join(input_dir, "model.json")
        if os.path.exists(model_path):
            self.model = load_model(model_path)
            # Also save to config location
            save_model(self.model, os.path.join(self.config.model_dir, "scoring_model.json"))

        # Import feedback
        feedback_path = os.path.join(input_dir, "feedback.json")
        if os.path.exists(feedback_path):
            self.feedback_collector = load_feedback(feedback_path)
            self.feedback_collector.save()

        print(f"Pipeline state imported from {input_dir}")
