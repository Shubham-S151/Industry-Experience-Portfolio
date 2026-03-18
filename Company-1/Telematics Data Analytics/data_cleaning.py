import numpy as np
import pandas as pd
import logging
from typing import List

# Logger Setup

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants

DEFAULT_BASE_VALUE = 100
MAX_STEP = 100


# File Loader (Supports Demo + Real)

def load_file_paths(root_path: str, demo: bool = True) -> List[str]:
    """
    Load file paths (demo or real).
    """
    if demo:
        logger.info("Using demo file paths")
        return ["file1.csv", "file2.csv"]
    else:
        from data_import import get_files_paths
        return get_files_paths(root_path)


def merge_files(file_list: List[str], demo: bool = True) -> pd.DataFrame:
    """
    Merge files into a single DataFrame.
    """
    if demo:
        logger.info("Generating synthetic demo data")

        data = {
            'timestamp': pd.date_range(start='2024-01-01', periods=100, freq='s'),
            'step': np.arange(100),
            'feature_a': np.random.rand(100) * 100,
            'feature_b': np.random.rand(100) * 50,
            'feature_c': np.random.randint(1, 7, size=100),
            'feature_d': np.random.rand(100) * 10
        }
        return pd.DataFrame(data)

    else:
        from data_import import combine_files
        return combine_files(file_list)

# Validation

def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate required columns and basic structure.
    """
    required_cols = [
        'timestamp', 'step',
        'feature_a', 'feature_b',
        'feature_c', 'feature_d'
    ]

    missing = [col for col in required_cols if col not in df.columns]

    if missing:
        raise ValueError(f"Missing columns: {missing}")

    return df

# Processing Steps

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Sort and remove null values.
    """
    logger.info("Cleaning data")
    return df.sort_values(by=['timestamp', 'step']).dropna()


def convert_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ensure consistent data types.
    """
    logger.info("Converting data types")

    return df.astype({
        'step': int,
        'feature_a': float,
        'feature_b': float,
        'feature_c': int,
        'feature_d': float
    })

# Feature Engineering

def compute_delta(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute step difference safely.
    """
    df['delta'] = df['step'].diff().fillna(0)
    df['delta'] = np.where(df['delta'] < 0, df['delta'] + MAX_STEP, df['delta'])
    return df


def create_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create derived metrics.
    """
    df['metric_1'] = df['feature_a'] * 0.1
    df['metric_2'] = df['feature_b'] / (DEFAULT_BASE_VALUE + 1)

    for power in [2, 3]:
        df[f'estimate_{power}'] = (df['feature_a'] / (DEFAULT_BASE_VALUE + 1)) ** power

    return df


def get_config_value(config_df: pd.DataFrame, entity_id: int, column: str):
    row = config_df[config_df['id'] == entity_id]

    if row.empty:
        raise ValueError(f"No record found for id={entity_id}")

    return row.iloc[0][column]


def apply_config_features(df: pd.DataFrame, entity_id: int, config_df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply config-driven transformations.
    """
    param = get_config_value(config_df, entity_id, 'param_1')
    df['adjusted_value'] = df['feature_d'] * param
    return df


def feature_engineering(df: pd.DataFrame, entity_id: int, config_df: pd.DataFrame) -> pd.DataFrame:
    """
    Full feature engineering pipeline.
    """
    logger.info("Performing feature engineering")

    df = df[(df['feature_c'] > 0) & (df['feature_c'] < 7)].copy()

    df = compute_delta(df)
    df = create_metrics(df)
    df = apply_config_features(df, entity_id, config_df)

    return df


# Mock Config

def get_mock_config() -> pd.DataFrame:
    """
    Create demo configuration data.
    """
    return pd.DataFrame({
        'id': [1, 2, 3],
        'param_1': [1.1, 1.2, 1.3],
        'param_2': [2.1, 2.2, 2.3],
        'meta': ['A', 'B', 'C']
    })


# Main Pipeline

def process_pipeline(root_path: str, entity_id: int, demo: bool = True) -> pd.DataFrame:
    """
    End-to-end data processing pipeline.
    """
    try:
        logger.info("Starting pipeline")

        files = load_file_paths(root_path, demo)
        df = merge_files(files, demo)

        df = validate_data(df)
        df = clean_data(df)
        df = convert_dtypes(df)

        config_df = get_mock_config()

        df = feature_engineering(df, entity_id, config_df)

        logger.info("Pipeline completed successfully")
        return df

    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise

# CLI Execution

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, default="demo_path")
    parser.add_argument("--entity_id", type=int, default=1)
    parser.add_argument("--demo", type=bool, default=True)

    args = parser.parse_args()

    df = process_pipeline(args.path, args.entity_id, args.demo)
    print(df.head())
