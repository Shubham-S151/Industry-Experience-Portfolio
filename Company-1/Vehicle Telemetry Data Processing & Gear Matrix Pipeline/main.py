import os
import argparse
import logging
import pandas as pd

from data_import import get_files_paths, combine_files
from data_cleaning import process_pipeline
from matrix_creation import create_gear_matrix

# Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Main Pipeline

def run_pipeline(data_path: str, entity_id: int):
    """
    Full pipeline:
    Load → Process → Analyze
    """
    try:
        logger.info("Starting pipeline")

        # Load Data
        paths = get_files_paths(data_path)
        logger.info(f"Found {len(paths)} files")

        df = combine_files(paths)
        logger.info(f"Loaded data shape: {df.shape}")

        # Process Data 
        df_processed = process_pipeline(df, entity_id)

        # Create Matrix 
        matrix_result = create_gear_matrix(df_processed)

        logger.info("Pipeline completed successfully")

        return matrix_result

    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise

# CLI Entry

def main():
    parser = argparse.ArgumentParser(description="Vehicle Telematics Pipeline")

    parser.add_argument(
        "--data_path",
        type=str,
        required=True,
        help="Path to telemetry data"
    )

    parser.add_argument(
        "--entity_id",
        type=int,
        default=1,
        help="Entity ID for config"
    )

    args = parser.parse_args()

    result = run_pipeline(args.data_path, args.entity_id)

    # Simple output preview
    print("\nMatrix Summary:")
    print("Total Mileage:", result["total_mileage"])
    print("Matrix Shape:", result["mileage_values"].shape)


# Entry Point

if __name__ == "__main__":
    main()
