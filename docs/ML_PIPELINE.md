# Machine Learning Pipeline Documentation

This document describes the ML pipeline integrated into Persona2Hire for adaptive scoring and continuous learning. The ML system was added in 2026 to enhance the original rule-based scoring from the 2022 high school project.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Components](#components)
  - [Feature Extractor](#1-feature-extractor)
  - [Scoring Model](#2-scoring-model)
  - [Data Generator](#3-data-generator)
  - [Feedback Collector](#4-feedback-collector)
  - [Pipeline Orchestrator](#5-pipeline-orchestrator)
- [How ML Scoring Works](#how-ml-scoring-works)
- [Feature Engineering Details](#feature-engineering-details)
- [Training Process](#training-process)
- [Integration with Rule-Based Scoring](#integration-with-rule-based-scoring)
- [Shortcomings & Limitations](#shortcomings--limitations)
- [Usage](#usage)
- [API Reference](#api-reference)

---

## Overview

The ML pipeline enhances the rule-based CV scoring system by:

1. **Learning patterns** in CV data that correlate with job fit
2. **Adjusting scores** based on real-world feedback (hiring outcomes)
3. **Providing insights** into which features matter most for different sectors

**Key Design Decision**: The ML model doesn't replace rule-based scoring. Instead, it provides an adjustment factor that refines the base score. This hybrid approach ensures:
- Predictable baseline behavior
- Graceful degradation when ML is unavailable
- Explainable scoring (users can see both rule-based and adjusted scores)

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                     ML Pipeline Architecture                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐           │
│  │ CV Data      │───▶│ Feature      │───▶│ ML Model     │           │
│  │ (dict)       │    │ Extractor    │    │ (Gradient    │           │
│  └──────────────┘    │ (31 features)│    │ Boosting)    │           │
│                      └──────────────┘    └──────┬───────┘           │
│                                                  │                   │
│                                                  ▼                   │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐           │
│  │ Rule-Based   │◀──▶│ Score        │◀───│ ML Predicted │           │
│  │ Score        │    │ Adjustment   │    │ Score        │           │
│  │ (0-100)      │    │ (±30% max)   │    │              │           │
│  └──────────────┘    └──────┬───────┘    └──────────────┘           │
│                             │                                        │
│                             ▼                                        │
│                      ┌──────────────┐                               │
│                      │ Final Score  │                               │
│                      │ (Hybrid)     │                               │
│                      └──────────────┘                               │
│                                                                      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐           │
│  │ User         │───▶│ Feedback     │───▶│ Periodic     │           │
│  │ Feedback     │    │ Collector    │    │ Retraining   │           │
│  │ (hired/not)  │    │ (JSON)       │    │              │           │
│  └──────────────┘    └──────────────┘    └──────────────┘           │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Components

### 1. Feature Extractor

**File**: `ml/feature_extractor.py`

Converts unstructured CV dictionary data into a fixed-size numerical vector suitable for ML models.

**Why 31 Features?**

The features were designed to capture the same information used by the rule-based scorer, allowing the ML model to learn potential weight adjustments:

| Category | Count | Purpose |
|----------|-------|---------|
| Education | 5 | Academic background strength |
| Work Experience | 6 | Professional history depth |
| Skills | 5 | Technical capability match |
| Languages | 4 | Communication ability |
| Soft Skills | 3 | Interpersonal traits |
| Additional | 4 | Extra achievements |
| Personality | 4 | MBTI alignment with sector |

**Feature Normalization**:
- Most features are normalized to 0-1 or small integer ranges
- Year counts are capped (e.g., max 20 years experience)
- This prevents features with large ranges from dominating

### 2. Scoring Model

**File**: `ml/model.py`

The `ScoringModel` class wraps the ML algorithm with training, prediction, and persistence logic.

**Algorithm Choice: Gradient Boosting**

Gradient Boosting Regression was chosen because:
- Handles non-linear relationships between features and scores
- Resistant to overfitting with proper hyperparameters
- Provides feature importance for interpretability
- Works well with the feature count (31) and expected dataset size

**Fallback Linear Model**:

If scikit-learn is not installed, a simple gradient descent linear regression is used:
```python
# Simplified fallback training
for epoch in range(1000):
    predictions = X @ weights + bias
    errors = predictions - y
    weights -= learning_rate * (X.T @ errors) / n
    bias -= learning_rate * errors.mean()
```

This ensures the system works without heavy dependencies, though with reduced accuracy.

**Hyperparameters**:
- `n_estimators`: 100 trees
- `max_depth`: 4 (prevents overfitting)
- `learning_rate`: 0.1
- `test_size`: 20% for validation

### 3. Data Generator

**File**: `ml/data_generator.py`

Generates synthetic training data with realistic CV patterns when real data is unavailable.

**Why Synthetic Data?**

- **Cold start problem**: Need data to train initial model
- **Privacy**: Real CVs contain personal information
- **Balance**: Can generate equal samples for different quality levels

**Generation Strategy**:
1. Select a target quality level (low, medium, high)
2. Generate appropriate education level for quality
3. Add work experience matching quality (years, seniority)
4. Include skills from sector's required/extra lists
5. Add personality that may or may not match sector
6. Calculate "ground truth" score using rule-based system

**Limitations of Synthetic Data**:
- Patterns may not match real-world CV distributions
- Unusual but valid combinations might be underrepresented
- Cultural and regional variations aren't captured

### 4. Feedback Collector

**File**: `ml/feedback.py`

Collects and stores user feedback for model improvement.

**Feedback Types**:
| Type | Data Collected | Value |
|------|----------------|-------|
| Score Correction | User provides "correct" score | High |
| Hiring Outcome | Whether candidate was hired | High |
| User Rating | Quality rating (1-5) | Medium |

**Storage Format** (JSON):
```json
{
  "cv_hash": "abc123...",
  "sector": "Computers_ICT",
  "predicted_score": 75.0,
  "actual_score": 82.0,
  "was_hired": true,
  "timestamp": "2026-01-15T10:30:00",
  "features": [...]
}
```

### 5. Pipeline Orchestrator

**File**: `ml/pipeline.py`

Coordinates all ML components and provides a unified interface.

**Pipeline States**:
1. **Untrained**: No model available, returns rule-based scores only
2. **Initial Training**: Model trained on synthetic data
3. **Active Learning**: Model incorporates feedback
4. **Retraining Due**: Sufficient new feedback to improve model

---

## How ML Scoring Works

### Step-by-Step Process

```
1. User loads CV and selects sector
                │
                ▼
2. Rule-based system calculates base score (e.g., 72.0)
                │
                ▼
3. Feature extractor converts CV to 31-dim vector
                │
                ▼
4. ML model predicts expected score (e.g., 80.0)
                │
                ▼
5. Adjustment factor calculated:
   factor = ml_score / base_score = 80/72 = 1.11
                │
                ▼
6. Factor clamped to ±30%:
   clamped_factor = min(1.3, max(0.7, 1.11)) = 1.11
                │
                ▼
7. Final score:
   adjusted_score = 72.0 × 1.11 = 79.9
```

### Why Adjustment Instead of Replacement?

**Explainability**: Users can see both scores and understand the adjustment.

**Safety**: Capping at ±30% prevents wild swings from ML errors.

**Graceful Degradation**: If ML fails, rule-based score is still valid.

**Transparency**: The adjustment factor reveals when ML disagrees with rules.

---

## Feature Engineering Details

### Education Features (5)

| Feature | Type | Range | Source |
|---------|------|-------|--------|
| `education_level` | Ordinal | 0-6 | QualificationsAwarded, parsed for degree keywords |
| `education_field_match` | Ratio | 0-1 | SubjectsStudied vs sector's School/College keywords |
| `university_prestige` | Ordinal | 0-3 | College/University vs Top50/Top100 lists |
| `years_studied` | Numeric | 0-10 | YearsStudied field |
| `has_masters` | Binary | 0/1 | Presence of Master1 or Master2 |

### Work Experience Features (6)

| Feature | Type | Range | Source |
|---------|------|-------|--------|
| `total_work_years` | Numeric | 0-20 | Sum of date ranges from Dates1/2/3 |
| `num_positions` | Count | 0-3 | Number of non-empty Workplace fields |
| `max_seniority` | Ordinal | 0-6 | Highest seniority from Occupation1/2/3 |
| `work_field_match` | Ratio | 0-1 | Work text vs sector's WorkExperience keywords |
| `current_employment` | Binary | 0/1 | "current" or "present" in date range |
| `avg_tenure` | Numeric | 0-10 | Average years per position |

### Skills Features (5)

| Feature | Type | Range | Source |
|---------|------|-------|--------|
| `required_skills_match` | Ratio | 0-1 | Skills vs sector's Skills list |
| `extra_skills_match` | Ratio | 0-1 | Skills vs sector's ExtraSkills list |
| `has_driving_license` | Binary | 0/1 | DrivingLicense not empty/none |
| `computer_skills_count` | Count | 0-15 | Comma-separated items in ComputerSkills |
| `total_skills_words` | Count | 0-100 | Total word count across all skills fields |

### Language Features (4)

| Feature | Type | Range | Source |
|---------|------|-------|--------|
| `num_languages` | Count | 1-5 | Mother + Modern languages |
| `has_english` | Binary | 0/1 | "english" in any language field |
| `max_language_level` | Ordinal | 0-6 | CEFR level from Level1/Level2 |
| `mother_tongue_tier` | Ordinal | 1-3 | Business value tier of mother language |

### Personality Features (4)

| Feature | Type | Range | Source |
|---------|------|-------|--------|
| `personality_match` | Binary | 0/1 | MBTI in sector's Personality list |
| `personality_partial_match` | Binary | 0/1 | First 2 letters match a preferred type |
| `introversion_score` | Ratio | 0/0.5/1 | I=1, E=0, unknown=0.5 |
| `thinking_score` | Ratio | 0/0.5/1 | T=1, F=0, unknown=0.5 |

---

## Training Process

### Initial Training

```bash
python -m scripts.train_model --initial --samples 200
```

1. **Generate Data**: Creates 200 synthetic CVs with known quality levels
2. **Extract Features**: Converts each CV to 31-feature vector
3. **Split Data**: 80% training, 20% validation
4. **Train Model**: Fits Gradient Boosting regressor
5. **Evaluate**: Calculates MAE, RMSE, R² on validation set
6. **Save**: Persists model to `data/models/scoring_model.json`

**Expected Metrics** (synthetic data):
- MAE: < 10 points
- RMSE: < 15 points
- R²: > 0.7

### Retraining with Feedback

```bash
python -m scripts.train_model --retrain
```

1. **Load Feedback**: Reads collected feedback entries
2. **Combine Data**: Synthetic + feedback (feedback weighted 2×)
3. **Retrain Model**: Full training on combined dataset
4. **Compare Metrics**: Validates improvement over previous model
5. **Backup & Save**: Archives old model, saves new one

**Retraining Triggers**:
- At least 50 feedback entries with actual scores
- Or average prediction error exceeds 15 points

---

## Integration with Rule-Based Scoring

### Enabling ML Scoring

```python
from persona2hire.analysis.job_analyzer import enable_ml_scoring, analyze_job

# Enable globally
enable_ml_scoring(True)

# Score now uses ML adjustment
score = analyze_job(cv_data, "Computers_ICT")
```

### Getting Detailed Insights

```python
from persona2hire.analysis.job_analyzer import analyze_job_with_ml

result = analyze_job_with_ml(cv_data, "Computers_ICT")
print(f"Rule-based: {result['rule_based_score']}")
print(f"ML adjusted: {result['ml_adjusted_score']}")
print(f"Adjustment: {result['adjustment_factor']:.2f}x")
print(f"ML available: {result['ml_available']}")
```

### Recording Feedback

```python
from persona2hire.analysis.job_analyzer import record_score_feedback

# When a candidate is hired
record_score_feedback(
    cv_data,
    sector="Computers_ICT",
    predicted_score=75.0,
    was_hired=True
)

# When user corrects a score
record_score_feedback(
    cv_data,
    sector="Computers_ICT",
    predicted_score=75.0,
    actual_score=85.0
)
```

---

## Shortcomings & Limitations

### Data Quality Issues

1. **Synthetic Data Bias**: Initial model learns from generated patterns, not real hiring decisions. These patterns may not reflect actual workplace success factors.

2. **Feedback Sparsity**: Most users won't provide feedback, leading to slow model improvement. The system may never accumulate enough data to outperform rule-based scoring.

3. **Selection Bias**: Feedback typically comes from candidates who were considered (high scorers), not those filtered out. The model doesn't learn well about low-scoring candidates.

### Model Limitations

4. **Sector Generalization**: A single model is used across all 30+ sectors. Sector-specific patterns (e.g., tech values skills over education) aren't well captured.

5. **Feature Interdependencies**: The 31 features are treated independently. Complex interactions (e.g., PhD + 0 years experience = academic track) aren't modeled explicitly.

6. **Temporal Blindness**: The model can't distinguish recent vs. old experience. Five years of experience from 2015 vs. 2023 are treated identically.

7. **No Uncertainty Quantification**: The model produces point estimates without confidence intervals. Users can't tell when the model is guessing.

### Integration Issues

8. **±30% Cap Limits Impact**: While safety-focused, this cap means the ML model can only make modest adjustments. If rule-based scoring is significantly wrong, ML can't fully correct it.

9. **Cold Start**: New sectors or unusual candidate profiles have no training data. ML provides little value for edge cases.

10. **Feedback Attribution**: When hiring fails, it's unclear if the issue was bad scoring or other factors (interview performance, salary mismatch).

### Technical Debt

11. **No Online Learning**: Model must be retrained in batch mode. Can't continuously improve from individual feedback.

12. **Single Model Architecture**: No easy way to swap in different algorithms (neural networks, random forests) for comparison.

13. **Missing A/B Testing**: No framework to measure if ML adjustment actually improves hiring outcomes vs. rule-based only.

---

## Usage

### Training Commands

```bash
# Initial training with synthetic data
python -m scripts.train_model --initial --samples 200

# Check model status
python -m scripts.train_model --status

# Retrain with accumulated feedback
python -m scripts.train_model --retrain
```

### Sample Generation

```bash
# Generate 10 random CVs
python -m scripts.generate_samples --count 10

# Generate for specific sector
python -m scripts.generate_samples --sector Computers_ICT --count 20

# List available sectors
python -m scripts.generate_samples --list-sectors
```

### Data Storage

```
data/
├── models/
│   ├── scoring_model.json          # Main model (weights, metrics)
│   ├── scoring_model_sklearn.pkl   # sklearn objects (if used)
│   └── scoring_model_YYYYMMDD.json # Backups
├── feedback/
│   └── feedback.json               # Collected feedback
└── training/
    ├── training_data.json          # Synthetic training data
    └── cvs/                         # Individual CV files
```

---

## API Reference

### MLPipeline

```python
class MLPipeline:
    def __init__(config: PipelineConfig, sector_data: dict)
    
    # Training
    def train_initial_model(num_synthetic_samples: int) -> ModelMetrics
    def retrain_with_feedback() -> ModelMetrics
    def should_retrain() -> bool
    
    # Prediction
    def predict_score(cv_data: dict, sector: str) -> float
    def get_adjusted_score(cv_data: dict, sector: str, base_score: float) -> float
    
    # Feedback
    def record_feedback(cv_data: dict, sector: str, 
                       predicted_score: float,
                       actual_score: float = None,
                       was_hired: bool = None) -> None
    
    # Insights
    def get_feature_importance() -> dict[str, float]
    def get_weight_recommendations() -> dict[str, float]
    def get_model_status() -> dict
    
    # Persistence
    def export_pipeline_state(output_dir: str) -> None
    def import_pipeline_state(input_dir: str) -> None
```

### ScoringModel

```python
class ScoringModel:
    def train(X: list[list[float]], y: list[float], 
              feature_names: list[str]) -> ModelMetrics
    def predict(X: list[list[float]]) -> list[float]
    def predict_single(features: list[float]) -> float
    def get_adjustment_factor(features: list[float], 
                              base_score: float) -> float
    def get_weight_adjustments() -> dict[str, float]
```

### FeatureExtractor

```python
class FeatureExtractor:
    FEATURE_NAMES: list[str]  # 31 feature names
    
    def __init__(sector_data: dict)
    def extract(cv_data: dict, sector: str) -> list[float]
```

### FeedbackCollector

```python
class FeedbackCollector:
    def add_feedback(cv_data: dict, sector: str,
                    predicted_score: float,
                    actual_score: float = None,
                    was_hired: bool = None) -> FeedbackEntry
    def record_outcome(cv_hash: str, sector: str, 
                       was_hired: bool) -> None
    def get_training_data() -> tuple[list, list]  # X, y
    def get_statistics() -> dict
    def save(filename: str) -> None
    def load(filename: str) -> None
```

### ModelMetrics

```python
@dataclass
class ModelMetrics:
    mae: float           # Mean Absolute Error
    rmse: float          # Root Mean Square Error
    r2: float            # R-squared coefficient
    training_samples: int
    training_date: str
    feature_importances: dict[str, float]
```

---

## Performance Benchmarks

### Training Time

| Samples | sklearn | Fallback Linear |
|---------|---------|-----------------|
| 100 | ~0.5s | ~0.1s |
| 500 | ~2s | ~0.3s |
| 2000 | ~10s | ~1s |

### Prediction Time

| Operation | Time |
|-----------|------|
| Feature extraction | ~1ms |
| Model prediction | ~0.1ms |
| Full adjusted score | ~2ms |

### Memory Usage

| Component | Memory |
|-----------|--------|
| Loaded model | ~1-2 MB |
| Feature extractor | ~0.5 MB |
| 1000 feedback entries | ~2 MB |
