#!/usr/bin/env python3
"""
Train or retrain the ML scoring model.

Usage:
    python -m scripts.train_model [options]

Options:
    --initial       Train initial model on synthetic data
    --retrain       Retrain using collected feedback
    --samples N     Number of synthetic samples (default: 200)
    --export DIR    Export pipeline state to directory
    --status        Show current model status
"""

import argparse
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from persona2hire.data.job_sectors import JobSectors
from persona2hire.ml.pipeline import MLPipeline, PipelineConfig


def main():
    parser = argparse.ArgumentParser(
        description="Train or retrain the ML scoring model"
    )
    parser.add_argument(
        "--initial",
        action="store_true",
        help="Train initial model on synthetic data",
    )
    parser.add_argument(
        "--retrain",
        action="store_true",
        help="Retrain using collected feedback",
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=200,
        help="Number of synthetic samples for initial training",
    )
    parser.add_argument(
        "--export",
        type=str,
        help="Export pipeline state to directory",
    )
    parser.add_argument(
        "--import-from",
        type=str,
        dest="import_from",
        help="Import pipeline state from directory",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show current model status",
    )
    parser.add_argument(
        "--no-sklearn",
        action="store_true",
        help="Use simple model instead of sklearn",
    )

    args = parser.parse_args()

    # Initialize pipeline
    config = PipelineConfig(use_sklearn=not args.no_sklearn)
    pipeline = MLPipeline(config=config, sector_data=JobSectors)

    if args.status:
        print("\n=== ML Pipeline Status ===\n")
        status = pipeline.get_model_status()

        print(f"Model trained: {status['model_trained']}")
        if status['model_trained']:
            print(f"  - MAE: {status['model_mae']:.2f}")
            print(f"  - R²: {status['model_r2']:.2f}")
            print(f"  - Training samples: {status['training_samples']}")
            print(f"  - Training date: {status['training_date']}")

        print(f"\nFeedback collected: {status['feedback_count']} entries")
        if status['feedback_stats']:
            stats = status['feedback_stats']
            print(f"  - With actual scores: {stats.get('entries_with_actual_score', 0)}")
            print(f"  - With outcomes: {stats.get('entries_with_outcome', 0)}")
            print(f"  - Candidates hired: {stats.get('candidates_hired', 0)}")
            if stats.get('average_prediction_error', 0) > 0:
                print(f"  - Avg prediction error: {stats['average_prediction_error']:.1f}")

        print(f"\nShould retrain: {status['should_retrain']}")

        # Feature importance
        importances = pipeline.get_feature_importance()
        if importances:
            print("\nTop 10 Feature Importances:")
            sorted_imp = sorted(importances.items(), key=lambda x: x[1], reverse=True)[:10]
            for name, imp in sorted_imp:
                print(f"  - {name}: {imp:.3f}")

        return

    if args.import_from:
        print(f"Importing pipeline state from {args.import_from}...")
        pipeline.import_pipeline_state(args.import_from)
        print("Import complete!")
        return

    if args.export:
        print(f"Exporting pipeline state to {args.export}...")
        pipeline.export_pipeline_state(args.export)
        print("Export complete!")
        return

    if args.initial:
        print(f"\n=== Training Initial Model ===")
        print(f"Generating {args.samples} synthetic samples...\n")

        metrics = pipeline.train_initial_model(num_synthetic_samples=args.samples)

        print(f"\n=== Training Complete ===")
        print(f"Mean Absolute Error: {metrics.mae:.2f}")
        print(f"Root Mean Square Error: {metrics.rmse:.2f}")
        print(f"R² Score: {metrics.r2:.2f}")
        print(f"Training samples: {metrics.training_samples}")

        print("\nTop 5 Most Important Features:")
        sorted_imp = sorted(
            metrics.feature_importances.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        for name, imp in sorted_imp:
            print(f"  - {name}: {imp:.3f}")

        # Weight recommendations
        recommendations = pipeline.get_weight_recommendations()
        if recommendations:
            print("\nWeight Adjustment Recommendations:")
            for category, factor in sorted(recommendations.items(), key=lambda x: -x[1]):
                direction = "↑" if factor > 1.1 else "↓" if factor < 0.9 else "="
                print(f"  {direction} {category}: {factor:.2f}x")

        return

    if args.retrain:
        print("\n=== Retraining Model with Feedback ===\n")

        if not pipeline.model or not pipeline.model.is_trained:
            print("No existing model found. Training initial model first...")
            pipeline.train_initial_model(num_synthetic_samples=100)

        metrics = pipeline.retrain_with_feedback()

        if metrics:
            print(f"\n=== Retraining Complete ===")
            print(f"Mean Absolute Error: {metrics.mae:.2f}")
            print(f"R² Score: {metrics.r2:.2f}")
        else:
            print("Retraining skipped - not enough feedback data")

        return

    # Default: show help
    parser.print_help()


if __name__ == "__main__":
    main()
