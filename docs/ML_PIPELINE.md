# Machine Learning Pipeline Documentation

This document describes the ML pipeline integrated into Persona2Hire for adaptive scoring and continuous learning.

## Overview

The ML pipeline enhances the rule-based CV scoring system by:

1. **Learning from patterns** in CV data that predict job fit
2. **Adapting scores** based on real-world feedback (hiring outcomes)
3. **Continuously improving** through periodic retraining
4. **Providing insights** into which features matter most

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     ML Pipeline Architecture                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │ CV Data      │───▶│ Feature      │───▶│ ML Model     │       │
│  │              │    │ Extractor    │    │ (Gradient    │       │
│  └──────────────┘    │ (31 features)│    │ Boosting)    │       │
│                      └──────────────┘    └──────┬───────┘       │
│                                                  │               │
│                                                  ▼               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │ Rule-Based   │◀──▶│ Score        │◀───│ ML Predicted │       │
│  │ Score        │    │ Adjustment   │    │ Score        │       │
│  └──────────────┘    └──────┬───────┘    └──────────────┘       │
│                             │                                    │
│                             ▼                                    │
│                      ┌──────────────┐                           │
│                      │ Final Score  │                           │
│                      │ (Hybrid)     │                           │
│                      └──────────────┘                           │
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │ User         │───▶│ Feedback     │───▶│ Periodic     │       │
│  │ Feedback     │    │ Collector    │    │ Retraining   │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Components

### 1. Feature Extractor (`feature_extractor.py`)

Extracts 31 numerical features from CV data:

| Category | Features | Description |
|----------|----------|-------------|
| **Education** (5) | education_level, education_field_match, university_prestige, years_studied, has_masters | Academic background |
| **Work Experience** (6) | total_work_years, num_positions, max_seniority, work_field_match, current_employment, avg_tenure | Professional history |
| **Skills** (5) | required_skills_match, extra_skills_match, has_driving_license, computer_skills_count, total_skills_words | Technical abilities |
| **Languages** (4) | num_languages, has_english, max_language_level, mother_tongue_tier | Language proficiency |
| **Soft Skills** (3) | soft_skills_categories, has_leadership, has_communication | Interpersonal skills |
| **Additional** (4) | publications_count, awards_count, projects_count, professional_memberships | Extra achievements |
| **Personality** (4) | personality_match, personality_partial_match, introversion_score, thinking_score | MBTI alignment |

### 2. Scoring Model (`model.py`)

Uses **Gradient Boosting Regression** (sklearn) or a fallback linear model:

- **Training**: Learns weights for features that predict job fit scores
- **Prediction**: Predicts expected score for new CV-sector combinations
- **Adjustment**: Provides adjustment factors for rule-based scores

### 3. Data Generator (`data_generator.py`)

Generates synthetic training data with realistic CV patterns:

- **Sector-specific content**: Tech CVs have Python, Finance CVs have Excel
- **Quality levels**: Low, medium, high scoring profiles
- **Realistic distribution**: Names, companies, skills from curated pools

### 4. Feedback Collector (`feedback.py`)

Collects user feedback for continuous learning:

- **Score corrections**: When user indicates correct score
- **Hiring outcomes**: Whether candidates were hired
- **User ratings**: Quality ratings for predictions

### 5. Pipeline (`pipeline.py`)

Orchestrates the complete ML workflow:

- Initial training on synthetic data
- Score prediction and adjustment
- Feedback collection
- Periodic retraining

## Usage

### Quick Start

```python
from persona2hire.ml.pipeline import MLPipeline
from persona2hire.data.job_sectors import JobSectors

# Initialize pipeline
pipeline = MLPipeline(sector_data=JobSectors)

# Train initial model
metrics = pipeline.train_initial_model(num_synthetic_samples=200)
print(f"Model trained with MAE: {metrics.mae:.2f}")

# Predict score
score = pipeline.predict_score(cv_data, "Computers_ICT")

# Get adjusted score (hybrid approach)
adjusted = pipeline.get_adjusted_score(cv_data, "Computers_ICT", rule_based_score)
```

### Training the Model

```bash
# Train initial model on synthetic data
python -m scripts.train_model --initial --samples 200

# View model status
python -m scripts.train_model --status

# Retrain with feedback
python -m scripts.train_model --retrain
```

### Generating Sample Data

```bash
# Generate 10 sample CVs
python -m scripts.generate_samples --count 10

# Generate for specific sector
python -m scripts.generate_samples --sector Computers_ICT --count 20

# List available sectors
python -m scripts.generate_samples --list-sectors
```

### Integration with Scoring

```python
from persona2hire.analysis.job_analyzer import (
    analyze_job,
    enable_ml_scoring,
    is_ml_available,
    analyze_job_with_ml,
    record_score_feedback,
)

# Enable ML scoring globally
enable_ml_scoring(True)

# Check if ML is available
if is_ml_available():
    print("ML model is trained and ready")

# Analyze with ML adjustment
score = analyze_job(cv_data, sector, use_ml=True)

# Get detailed ML insights
result = analyze_job_with_ml(cv_data, sector)
print(f"Rule score: {result['rule_based_score']}")
print(f"ML adjusted: {result['ml_adjusted_score']}")
print(f"Adjustment: {result['adjustment_factor']}x")

# Record feedback for learning
record_score_feedback(
    cv_data, sector,
    predicted_score=75.0,
    was_hired=True
)
```

## Training Pipeline

### Initial Training

1. **Generate synthetic data**: Creates diverse CV profiles with known quality levels
2. **Extract features**: Converts CVs to 31-dimensional feature vectors
3. **Train model**: Uses Gradient Boosting to learn feature importance
4. **Evaluate**: Measures MAE, RMSE, and R² on held-out test set
5. **Save model**: Persists to `data/models/scoring_model.json`

### Retraining with Feedback

1. **Collect feedback**: User corrections and hiring outcomes
2. **Combine datasets**: Synthetic + feedback (feedback weighted 2x)
3. **Retrain model**: Updates weights based on real-world data
4. **Validate improvement**: Compares metrics to previous model
5. **Deploy**: Saves new model, backs up old one

### Automatic Retraining

The system recommends retraining when:
- At least 50 feedback entries with actual scores/outcomes
- Average prediction error exceeds 15 points

## Feature Importance

After training, you can see which features matter most:

```python
importances = pipeline.get_feature_importance()
for name, imp in sorted(importances.items(), key=lambda x: -x[1])[:10]:
    print(f"{name}: {imp:.3f}")
```

Typical important features:
1. `total_work_years` - Experience matters most
2. `education_level` - Qualification level
3. `required_skills_match` - Relevant skills
4. `max_seniority` - Career progression
5. `work_field_match` - Industry relevance

## Weight Recommendations

The ML model suggests adjustments to rule-based weights:

```python
recommendations = pipeline.get_weight_recommendations()
# Example output:
# {
#   "work_experience": 1.25,  # Suggest increasing weight
#   "education": 0.95,        # Slightly decrease
#   "skills": 1.10,           # Slightly increase
#   ...
# }
```

## Data Storage

```
data/
├── models/
│   ├── scoring_model.json      # Main model
│   ├── scoring_model_sklearn.pkl  # sklearn objects (if used)
│   └── scoring_model_YYYYMMDD_HHMMSS.json  # Backups
├── feedback/
│   └── feedback.json           # Collected feedback
└── training/
    ├── training_data.json      # Synthetic training data
    └── cvs/                    # Individual CV files
```

## Performance Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| **MAE** | Mean Absolute Error | < 10 |
| **RMSE** | Root Mean Square Error | < 15 |
| **R²** | Coefficient of Determination | > 0.7 |

## Fallback Behavior

The ML system gracefully degrades:

1. **sklearn not installed**: Uses simple linear regression
2. **Model not trained**: Returns rule-based score only
3. **Prediction error**: Falls back to rule-based score
4. **Extreme adjustment**: Capped at ±30% to prevent wild swings

## Best Practices

### Training
- Start with 200+ synthetic samples
- Retrain monthly or after 100+ feedback entries
- Monitor MAE - if > 15, investigate data quality

### Feedback Collection
- Encourage users to provide hiring outcomes
- Score corrections are most valuable
- Track sector-specific performance

### Integration
- Use hybrid scoring (rule + ML adjustment)
- Don't replace rule-based entirely
- Show both scores to users for transparency

## Troubleshooting

### "Model not trained" error
```bash
python -m scripts.train_model --initial
```

### Poor prediction accuracy
1. Check training data distribution
2. Verify feature extraction is working
3. Try retraining with more samples

### sklearn import error
```bash
pip install scikit-learn numpy
```

## API Reference

### MLPipeline

```python
class MLPipeline:
    def train_initial_model(num_synthetic_samples: int) -> ModelMetrics
    def predict_score(cv_data: dict, sector: str) -> float
    def get_adjusted_score(cv_data: dict, sector: str, base_score: float) -> float
    def record_feedback(...) -> None
    def should_retrain() -> bool
    def retrain_with_feedback() -> ModelMetrics
    def get_feature_importance() -> dict[str, float]
    def get_weight_recommendations() -> dict[str, float]
    def get_model_status() -> dict
    def export_pipeline_state(output_dir: str) -> None
    def import_pipeline_state(input_dir: str) -> None
```

### ScoringModel

```python
class ScoringModel:
    def train(X: list, y: list, feature_names: list) -> ModelMetrics
    def predict(X: list) -> list[float]
    def predict_single(features: list) -> float
    def get_adjustment_factor(features: list, base_score: float) -> float
```

### FeedbackCollector

```python
class FeedbackCollector:
    def add_feedback(...) -> FeedbackEntry
    def record_outcome(cv_hash: str, sector: str, was_hired: bool) -> None
    def get_training_data() -> tuple[list, list]
    def get_statistics() -> dict
    def save(filename: str) -> None
    def load(filename: str) -> None
```
