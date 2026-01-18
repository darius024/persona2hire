"""Feedback collection and aggregation for continuous learning."""

import json
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional


@dataclass
class FeedbackEntry:
    """A single feedback entry from user interaction."""

    timestamp: str
    cv_hash: str  # Hash of CV data for identification
    sector: str
    predicted_score: float
    actual_score: Optional[float] = None  # User-provided correct score
    was_hired: Optional[bool] = None  # Whether candidate was hired
    user_rating: Optional[int] = None  # 1-5 star rating of prediction
    notes: str = ""
    features: list[float] = field(default_factory=list)


class FeedbackCollector:
    """
    Collects and manages user feedback for model improvement.

    Feedback is used to:
    1. Identify when predictions are wrong
    2. Collect actual outcomes (hired/not hired)
    3. Build a dataset for model retraining
    """

    def __init__(self, storage_path: str = "data/feedback"):
        """
        Initialize feedback collector.

        Args:
            storage_path: Directory to store feedback data
        """
        self.storage_path = storage_path
        self.entries: list[FeedbackEntry] = []
        self._ensure_storage_dir()

    def _ensure_storage_dir(self):
        """Create storage directory if it doesn't exist."""
        os.makedirs(self.storage_path, exist_ok=True)

    def add_feedback(
        self,
        cv_data: dict,
        sector: str,
        predicted_score: float,
        features: list[float],
        actual_score: Optional[float] = None,
        was_hired: Optional[bool] = None,
        user_rating: Optional[int] = None,
        notes: str = "",
    ) -> FeedbackEntry:
        """
        Add a new feedback entry.

        Args:
            cv_data: The CV data that was analyzed
            sector: Job sector analyzed for
            predicted_score: Score predicted by the system
            features: Feature vector used for prediction
            actual_score: User-corrected score (optional)
            was_hired: Whether candidate was hired (optional)
            user_rating: User's rating of prediction quality (optional)
            notes: Additional notes (optional)

        Returns:
            The created FeedbackEntry
        """
        # Create hash of CV for identification
        cv_hash = self._hash_cv(cv_data)

        entry = FeedbackEntry(
            timestamp=datetime.now().isoformat(),
            cv_hash=cv_hash,
            sector=sector,
            predicted_score=predicted_score,
            actual_score=actual_score,
            was_hired=was_hired,
            user_rating=user_rating,
            notes=notes,
            features=features,
        )

        self.entries.append(entry)
        return entry

    def record_outcome(
        self,
        cv_hash: str,
        sector: str,
        was_hired: bool,
        actual_score: Optional[float] = None,
    ):
        """
        Record the outcome for a previously analyzed CV.

        Args:
            cv_hash: Hash of the CV data
            sector: Job sector
            was_hired: Whether the candidate was hired
            actual_score: Actual score if known
        """
        # Find matching entries and update
        for entry in self.entries:
            if entry.cv_hash == cv_hash and entry.sector == sector:
                entry.was_hired = was_hired
                if actual_score is not None:
                    entry.actual_score = actual_score
                break

    def get_training_data(self) -> tuple[list[list[float]], list[float]]:
        """
        Get training data from feedback entries.

        Only includes entries with actual scores or hire outcomes.

        Returns:
            Tuple of (feature matrix, target scores)
        """
        X = []
        y = []

        for entry in self.entries:
            if not entry.features:
                continue

            # Use actual score if provided
            if entry.actual_score is not None:
                X.append(entry.features)
                y.append(entry.actual_score)
            # Use hire outcome as proxy (hired = 80+, not hired = 40-)
            elif entry.was_hired is not None:
                X.append(entry.features)
                if entry.was_hired:
                    y.append(max(80.0, entry.predicted_score))
                else:
                    y.append(min(40.0, entry.predicted_score))

        return X, y

    def get_statistics(self) -> dict:
        """
        Get statistics about collected feedback.

        Returns:
            Dictionary with feedback statistics
        """
        total = len(self.entries)
        with_actual = sum(1 for e in self.entries if e.actual_score is not None)
        with_outcome = sum(1 for e in self.entries if e.was_hired is not None)
        hired = sum(1 for e in self.entries if e.was_hired is True)

        # Calculate prediction error for entries with actual scores
        errors = []
        for entry in self.entries:
            if entry.actual_score is not None:
                errors.append(abs(entry.predicted_score - entry.actual_score))

        avg_error = sum(errors) / len(errors) if errors else 0.0

        # Sector distribution
        sector_counts = {}
        for entry in self.entries:
            sector_counts[entry.sector] = sector_counts.get(entry.sector, 0) + 1

        return {
            "total_entries": total,
            "entries_with_actual_score": with_actual,
            "entries_with_outcome": with_outcome,
            "candidates_hired": hired,
            "average_prediction_error": avg_error,
            "sector_distribution": sector_counts,
        }

    def _hash_cv(self, cv_data: dict) -> str:
        """Create a hash of CV data for identification."""
        # Simple hash based on key fields
        key_fields = ["FirstName", "LastName", "EmailAddress", "DateOfBirth"]
        hash_str = "|".join(str(cv_data.get(f, "")) for f in key_fields)
        return str(hash(hash_str))

    def save(self, filename: str = "feedback.json"):
        """
        Save feedback data to file.

        Args:
            filename: Name of file to save to
        """
        filepath = os.path.join(self.storage_path, filename)
        data = [asdict(entry) for entry in self.entries]

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load(self, filename: str = "feedback.json"):
        """
        Load feedback data from file.

        Args:
            filename: Name of file to load from
        """
        filepath = os.path.join(self.storage_path, filename)

        if not os.path.exists(filepath):
            return

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.entries = [
            FeedbackEntry(**entry) for entry in data
        ]

    def export_for_training(self, output_path: str):
        """
        Export feedback data in format ready for training.

        Args:
            output_path: Path to save training data
        """
        X, y = self.get_training_data()

        if not X:
            return

        data = {
            "features": X,
            "targets": y,
            "num_samples": len(X),
            "export_date": datetime.now().isoformat(),
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)


def save_feedback(collector: FeedbackCollector, filepath: str):
    """
    Save feedback collector to file.

    Args:
        collector: FeedbackCollector instance
        filepath: Path to save file
    """
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
    data = {
        "storage_path": collector.storage_path,
        "entries": [asdict(e) for e in collector.entries],
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_feedback(filepath: str) -> FeedbackCollector:
    """
    Load feedback collector from file.

    Args:
        filepath: Path to load from

    Returns:
        FeedbackCollector instance
    """
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    collector = FeedbackCollector(data.get("storage_path", "data/feedback"))
    collector.entries = [
        FeedbackEntry(**e) for e in data.get("entries", [])
    ]
    return collector
