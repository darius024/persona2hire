"""
Machine learning model for adaptive scoring.

This module provides the core ML model used to predict and adjust CV scores.
It supports both scikit-learn's GradientBoostingRegressor and a simple fallback
linear model for environments without ML dependencies.

Model Architecture
==================
Primary: Gradient Boosting Regression (scikit-learn)
- Ensemble of decision trees trained sequentially
- Each tree corrects errors from previous trees
- Hyperparameters: 100 trees, max_depth=4, learning_rate=0.1

Fallback: Linear Regression (pure Python)
- Simple weighted sum: score = Σ(weight_i × feature_i) + bias
- Trained via gradient descent (1000 iterations)
- Used when scikit-learn is not installed

Why Gradient Boosting?
======================
1. Handles non-linear feature relationships
2. Resistant to overfitting with proper regularization
3. Provides feature importance for interpretability
4. Works well with moderate dataset sizes (100-10000 samples)
5. Fast prediction time (~0.1ms per sample)

Score Adjustment vs Replacement
===============================
The model provides an **adjustment factor** rather than replacing rule-based scores:

    adjusted_score = rule_based_score × adjustment_factor
    
The adjustment factor is clamped to ±30%:
    
    factor = min(1.3, max(0.7, ml_score / rule_based_score))

This design provides:
- Explainable baselines (rule-based score always available)
- Safety limits (ML can't cause wild score swings)
- Graceful degradation (falls back to rule-based if ML fails)

Model Persistence
=================
Models are saved as JSON with sklearn objects pickled separately:

    data/models/
    ├── scoring_model.json       # Weights, metrics, metadata
    └── scoring_model_sklearn.pkl # sklearn model + scaler

The JSON file contains everything needed for the fallback linear model,
ensuring the system works even if sklearn is unavailable at load time.

Training Metrics
================
The ModelMetrics dataclass tracks:
- MAE (Mean Absolute Error): Average prediction error
- RMSE (Root Mean Square Error): Penalizes large errors
- R² (Coefficient of Determination): Variance explained

Target metrics for trained model:
- MAE < 10 points
- RMSE < 15 points  
- R² > 0.7

Usage
=====
    from persona2hire.ml.model import ScoringModel, save_model, load_model
    
    # Create and train
    model = ScoringModel(use_sklearn=True)
    metrics = model.train(X, y, feature_names)
    
    # Predict
    scores = model.predict(X_new)
    single_score = model.predict_single(features)
    
    # Get adjustment factor
    factor = model.get_adjustment_factor(features, base_score=72.0)
    
    # Save/load
    save_model(model, "path/to/model.json")
    loaded_model = load_model("path/to/model.json")
"""

import json
import os
import pickle
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import math


@dataclass
class ModelMetrics:
    """Metrics from model training/evaluation."""

    mae: float = 0.0  # Mean Absolute Error
    rmse: float = 0.0  # Root Mean Square Error
    r2: float = 0.0  # R-squared score
    training_samples: int = 0
    training_date: str = ""
    feature_importances: dict = field(default_factory=dict)


class ScoringModel:
    """
    Machine learning model for predicting and adjusting CV scores.

    Uses gradient boosting or simple ensemble methods that work
    without heavy dependencies (can be extended with sklearn).
    """

    def __init__(self, use_sklearn: bool = True):
        """
        Initialize the scoring model.

        Args:
            use_sklearn: Whether to use scikit-learn (if available)
        """
        self.use_sklearn = use_sklearn
        self.model = None
        self.is_trained = False
        self.metrics = ModelMetrics()
        self.feature_names: list[str] = []
        self.weight_adjustments: dict[str, float] = {}
        self._sklearn_available = False

        # Try to import sklearn
        if use_sklearn:
            try:
                from sklearn.ensemble import GradientBoostingRegressor
                from sklearn.preprocessing import StandardScaler

                self._sklearn_available = True
            except ImportError:
                self._sklearn_available = False

        # Fallback: simple weighted linear model
        self.weights: list[float] = []
        self.bias: float = 0.0
        self.scaler_mean: list[float] = []
        self.scaler_std: list[float] = []

    def train(
        self,
        X: list[list[float]],
        y: list[float],
        feature_names: Optional[list[str]] = None,
    ) -> ModelMetrics:
        """
        Train the model on feature data.

        Args:
            X: Feature matrix (list of feature vectors)
            y: Target scores
            feature_names: Names of features (for importance tracking)

        Returns:
            ModelMetrics with training results
        """
        if len(X) < 10:
            raise ValueError("Need at least 10 samples for training")

        self.feature_names = feature_names or [f"feature_{i}" for i in range(len(X[0]))]

        if self._sklearn_available:
            return self._train_sklearn(X, y)
        else:
            return self._train_simple(X, y)

    def _train_sklearn(self, X: list[list[float]], y: list[float]) -> ModelMetrics:
        """Train using scikit-learn."""
        from sklearn.ensemble import GradientBoostingRegressor
        from sklearn.preprocessing import StandardScaler
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
        import numpy as np

        X_array = np.array(X)
        y_array = np.array(y)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_array, y_array, test_size=0.2, random_state=42
        )

        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        # Train model
        self.model = GradientBoostingRegressor(
            n_estimators=100,
            max_depth=4,
            learning_rate=0.1,
            random_state=42,
        )
        self.model.fit(X_train_scaled, y_train)

        # Evaluate
        y_pred = self.model.predict(X_test_scaled)

        self.metrics = ModelMetrics(
            mae=mean_absolute_error(y_test, y_pred),
            rmse=math.sqrt(mean_squared_error(y_test, y_pred)),
            r2=r2_score(y_test, y_pred),
            training_samples=len(X),
            training_date=datetime.now().isoformat(),
            feature_importances={
                name: float(imp)
                for name, imp in zip(self.feature_names, self.model.feature_importances_)
            },
        )

        self.is_trained = True
        return self.metrics

    def _train_simple(self, X: list[list[float]], y: list[float]) -> ModelMetrics:
        """Train using simple linear regression (no sklearn)."""
        n_samples = len(X)
        n_features = len(X[0])

        # Compute mean and std for scaling
        self.scaler_mean = [0.0] * n_features
        self.scaler_std = [1.0] * n_features

        for j in range(n_features):
            col = [X[i][j] for i in range(n_samples)]
            self.scaler_mean[j] = sum(col) / n_samples
            variance = sum((x - self.scaler_mean[j]) ** 2 for x in col) / n_samples
            self.scaler_std[j] = max(math.sqrt(variance), 1e-6)

        # Scale features
        X_scaled = []
        for i in range(n_samples):
            row = [
                (X[i][j] - self.scaler_mean[j]) / self.scaler_std[j]
                for j in range(n_features)
            ]
            X_scaled.append(row)

        # Simple gradient descent for linear regression
        self.weights = [0.0] * n_features
        self.bias = sum(y) / n_samples
        learning_rate = 0.01

        for _ in range(1000):
            # Compute predictions
            predictions = [
                sum(X_scaled[i][j] * self.weights[j] for j in range(n_features)) + self.bias
                for i in range(n_samples)
            ]

            # Compute gradients
            errors = [predictions[i] - y[i] for i in range(n_samples)]

            # Update weights
            for j in range(n_features):
                gradient = sum(errors[i] * X_scaled[i][j] for i in range(n_samples)) / n_samples
                self.weights[j] -= learning_rate * gradient

            # Update bias
            bias_gradient = sum(errors) / n_samples
            self.bias -= learning_rate * bias_gradient

        # Compute metrics on full dataset
        predictions = self._predict_simple(X)
        mae = sum(abs(predictions[i] - y[i]) for i in range(n_samples)) / n_samples
        mse = sum((predictions[i] - y[i]) ** 2 for i in range(n_samples)) / n_samples
        rmse = math.sqrt(mse)

        # R2 score
        y_mean = sum(y) / n_samples
        ss_tot = sum((yi - y_mean) ** 2 for yi in y)
        ss_res = sum((y[i] - predictions[i]) ** 2 for i in range(n_samples))
        r2 = 1 - (ss_res / max(ss_tot, 1e-6))

        # Feature importance (absolute weight values)
        total_weight = sum(abs(w) for w in self.weights) + 1e-6
        importances = {
            name: abs(w) / total_weight
            for name, w in zip(self.feature_names, self.weights)
        }

        self.metrics = ModelMetrics(
            mae=mae,
            rmse=rmse,
            r2=r2,
            training_samples=n_samples,
            training_date=datetime.now().isoformat(),
            feature_importances=importances,
        )

        self.is_trained = True
        return self.metrics

    def predict(self, X: list[list[float]]) -> list[float]:
        """
        Predict scores for feature vectors.

        Args:
            X: Feature matrix

        Returns:
            List of predicted scores
        """
        if not self.is_trained:
            raise ValueError("Model not trained. Call train() first.")

        if self._sklearn_available and self.model is not None:
            import numpy as np

            X_scaled = self.scaler.transform(np.array(X))
            return self.model.predict(X_scaled).tolist()
        else:
            return self._predict_simple(X)

    def _predict_simple(self, X: list[list[float]]) -> list[float]:
        """Predict using simple linear model."""
        predictions = []
        n_features = len(self.weights)

        for row in X:
            # Scale
            scaled = [
                (row[j] - self.scaler_mean[j]) / self.scaler_std[j]
                for j in range(n_features)
            ]
            # Predict
            pred = sum(scaled[j] * self.weights[j] for j in range(n_features)) + self.bias
            # Clamp to valid range
            predictions.append(max(0.0, min(100.0, pred)))

        return predictions

    def predict_single(self, features: list[float]) -> float:
        """
        Predict score for a single feature vector.

        Args:
            features: Feature vector

        Returns:
            Predicted score
        """
        return self.predict([features])[0]

    def get_adjustment_factor(self, features: list[float], base_score: float) -> float:
        """
        Get an adjustment factor to modify the base score.

        This allows the ML model to refine the rule-based score
        rather than replacing it entirely.

        Args:
            features: Feature vector
            base_score: Original rule-based score

        Returns:
            Adjustment factor (multiply with base_score)
        """
        if not self.is_trained:
            return 1.0  # No adjustment if not trained

        ml_score = self.predict_single(features)

        # Calculate adjustment as ratio, but dampen extreme adjustments
        if base_score < 1:
            return 1.0

        ratio = ml_score / base_score

        # Dampen: limit adjustment to ±30%
        ratio = max(0.7, min(1.3, ratio))

        return ratio

    def get_weight_adjustments(self) -> dict[str, float]:
        """
        Get suggested weight adjustments based on feature importance.

        Returns:
            Dictionary mapping feature categories to adjustment factors
        """
        if not self.is_trained or not self.metrics.feature_importances:
            return {}

        # Group features by category
        categories = {
            "education": ["education_level", "education_field_match", "university_prestige", "years_studied", "has_masters"],
            "work_experience": ["total_work_years", "num_positions", "max_seniority", "work_field_match", "current_employment", "avg_tenure"],
            "skills": ["required_skills_match", "extra_skills_match", "has_driving_license", "computer_skills_count", "total_skills_words"],
            "languages": ["num_languages", "has_english", "max_language_level", "mother_tongue_tier"],
            "soft_skills": ["soft_skills_categories", "has_leadership", "has_communication"],
            "additional": ["publications_count", "awards_count", "projects_count", "professional_memberships"],
            "personality": ["personality_match", "personality_partial_match", "introversion_score", "thinking_score"],
        }

        adjustments = {}
        importances = self.metrics.feature_importances

        for category, features in categories.items():
            # Sum importance for category features
            category_importance = sum(
                importances.get(f, 0.0) for f in features
            )
            # Normalize: if importance is higher than expected, suggest increase
            expected = 1.0 / len(categories)  # Equal distribution
            if category_importance > 0:
                adjustments[category] = category_importance / expected
            else:
                adjustments[category] = 1.0

        return adjustments


def save_model(model: ScoringModel, filepath: str):
    """
    Save trained model to file.

    Args:
        model: Trained ScoringModel
        filepath: Path to save file
    """
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)

    data = {
        "is_trained": model.is_trained,
        "use_sklearn": model._sklearn_available,
        "feature_names": model.feature_names,
        "metrics": {
            "mae": model.metrics.mae,
            "rmse": model.metrics.rmse,
            "r2": model.metrics.r2,
            "training_samples": model.metrics.training_samples,
            "training_date": model.metrics.training_date,
            "feature_importances": model.metrics.feature_importances,
        },
        "weights": model.weights,
        "bias": model.bias,
        "scaler_mean": model.scaler_mean,
        "scaler_std": model.scaler_std,
    }

    # Save sklearn model separately if available
    if model._sklearn_available and model.model is not None:
        sklearn_path = filepath.replace(".json", "_sklearn.pkl")
        with open(sklearn_path, "wb") as f:
            pickle.dump({"model": model.model, "scaler": model.scaler}, f)
        data["sklearn_model_path"] = os.path.basename(sklearn_path)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_model(filepath: str) -> ScoringModel:
    """
    Load model from file.

    Args:
        filepath: Path to model file

    Returns:
        Loaded ScoringModel
    """
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    model = ScoringModel(use_sklearn=data.get("use_sklearn", False))
    model.is_trained = data.get("is_trained", False)
    model.feature_names = data.get("feature_names", [])
    model.weights = data.get("weights", [])
    model.bias = data.get("bias", 0.0)
    model.scaler_mean = data.get("scaler_mean", [])
    model.scaler_std = data.get("scaler_std", [])

    metrics_data = data.get("metrics", {})
    model.metrics = ModelMetrics(
        mae=metrics_data.get("mae", 0.0),
        rmse=metrics_data.get("rmse", 0.0),
        r2=metrics_data.get("r2", 0.0),
        training_samples=metrics_data.get("training_samples", 0),
        training_date=metrics_data.get("training_date", ""),
        feature_importances=metrics_data.get("feature_importances", {}),
    )

    # Load sklearn model if available
    sklearn_path = data.get("sklearn_model_path")
    if sklearn_path:
        sklearn_full_path = os.path.join(os.path.dirname(filepath), sklearn_path)
        if os.path.exists(sklearn_full_path):
            try:
                with open(sklearn_full_path, "rb") as f:
                    sklearn_data = pickle.load(f)
                model.model = sklearn_data["model"]
                model.scaler = sklearn_data["scaler"]
                model._sklearn_available = True
            except Exception:
                model._sklearn_available = False

    return model
