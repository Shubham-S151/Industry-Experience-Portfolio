import os
import pandas as pd
import logging
from typing import List

# Configure logger (can be centralized later)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_files_paths(root_path: str) -> List[str]:
    """
    Recursively fetch all parquet file paths from a given directory.

    Args:
        root_path (str): Root directory containing parquet files

    Returns:
        List[str]: List of full file paths
    """
    paths = []
    try:
        for root, _, files in os.walk(root_path):
            for file in files:
                if file.endswith(".parquet"):
                    full_path = os.path.join(root, file)
                    paths.append(full_path)

        logger.info(f"Found {len(paths)} parquet files in {root_path}")
        return paths

    except Exception as e:
        logger.error(f"Error fetching file paths from {root_path}: {e}")
        raise


def combine_files(paths: List[str]) -> pd.DataFrame:
    """
    Combine multiple parquet files into a single DataFrame.

    Args:
        paths (List[str]): List of parquet file paths

    Returns:
        pd.DataFrame: Combined DataFrame
    """
    try:
        if not paths:
            raise ValueError("No file paths provided")

        df_list = []
        for path in paths:
            logger.info(f"Reading file: {path}")
            df = pd.read_parquet(path)
            df_list.append(df)

        combined_df = pd.concat(df_list, ignore_index=True)

        logger.info(f"Successfully combined {len(paths)} files")
        return combined_df

    except Exception as e:
        logger.error(f"Error combining parquet files: {e}")
        raise
