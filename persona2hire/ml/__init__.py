"""Machine Learning module for adaptive scoring and analysis."""

from .feature_extractor import extract_features, FeatureExtractor
from .model import ScoringModel, load_model, save_model
from .pipeline import MLPipeline
from .feedback import FeedbackCollector, load_feedback, save_feedback
from .data_generator import generate_training_data, generate_synthetic_cv

__all__ = [
    "extract_features",
    "FeatureExtractor",
    "ScoringModel",
    "load_model",
    "save_model",
    "MLPipeline",
    "FeedbackCollector",
    "load_feedback",
    "save_feedback",
    "generate_training_data",
    "generate_synthetic_cv",
]
