#!/usr/bin/env python3
"""
Generate sample CVs for testing and training.

Usage:
    python -m scripts.generate_samples [options]

Options:
    --count N       Number of CVs to generate (default: 10)
    --sector NAME   Generate CVs for specific sector
    --output DIR    Output directory (default: samples/generated)
    --format FMT    Output format: json, txt, both (default: both)
"""

import argparse
import json
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from persona2hire.ml.data_generator import generate_synthetic_cv, SECTOR_PROFILES
from persona2hire.cv.writer import write_cv_file


def main():
    parser = argparse.ArgumentParser(
        description="Generate sample CVs for testing and training"
    )
    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="Number of CVs to generate",
    )
    parser.add_argument(
        "--sector",
        type=str,
        help="Generate CVs for specific sector",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="samples/generated",
        help="Output directory",
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["json", "txt", "both"],
        default="both",
        help="Output format",
    )
    parser.add_argument(
        "--list-sectors",
        action="store_true",
        help="List available sectors",
    )

    args = parser.parse_args()

    if args.list_sectors:
        print("\nAvailable sectors for CV generation:")
        for sector in SECTOR_PROFILES.keys():
            print(f"  - {sector}")
        return

    # Create output directory
    os.makedirs(args.output, exist_ok=True)

    sectors = [args.sector] if args.sector else list(SECTOR_PROFILES.keys())

    print(f"\nGenerating {args.count} CVs...")
    print(f"Sectors: {', '.join(sectors[:3])}{'...' if len(sectors) > 3 else ''}")
    print(f"Output: {args.output}\n")

    generated = []

    for i in range(args.count):
        # Cycle through sectors
        sector = sectors[i % len(sectors)]

        # Generate CV
        cv = generate_synthetic_cv(target_sector=sector, seed=i)

        # Determine quality based on index
        quality = ["low", "medium", "high"][i % 3]

        info = {
            "index": i,
            "sector": sector,
            "quality": quality,
            "name": f"{cv['FirstName']} {cv['LastName']}",
        }
        generated.append(info)

        # Save in requested format(s)
        basename = f"cv_{i:04d}_{sector}_{cv['LastName'].lower()}"

        if args.format in ["json", "both"]:
            json_path = os.path.join(args.output, f"{basename}.json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(cv, f, indent=2)

        if args.format in ["txt", "both"]:
            try:
                txt_path = write_cv_file(cv, output_dir=args.output)
                # Rename to match naming scheme
                new_path = os.path.join(args.output, f"{basename}.txt")
                if txt_path != new_path:
                    os.rename(txt_path, new_path)
            except Exception as e:
                print(f"Warning: Could not write txt for {info['name']}: {e}")

        print(f"  [{i+1}/{args.count}] {info['name']} ({sector}, {quality})")

    # Save manifest
    manifest = {
        "count": args.count,
        "sectors": list(set(g["sector"] for g in generated)),
        "generated": generated,
    }
    manifest_path = os.path.join(args.output, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"\nGenerated {args.count} CVs in {args.output}")
    print(f"Manifest saved to {manifest_path}")


if __name__ == "__main__":
    main()
