import numpy as np
import pandas as pd

# -----------------------------------
# Demo Constants (non-sensitive)
# -----------------------------------
DEFAULT_BASE_VALUE = 100  # Placeholder value

# -----------------------------------
# Mock Data Loaders (Safe for Demo)
# -----------------------------------

def load_file_paths(root_path: str):
    """Simulate loading file paths"""
    return ["file1.csv", "file2.csv"]


def merge_files(file_list):
    """Simulate merging files into a single DataFrame"""
    # Creating synthetic demo data
    data = {
        'timestamp': pd.date_range(start='2024-01-01', periods=100, freq='S'),
        'step': np.arange(100),
        'feature_a': np.random.rand(100) * 100,
        'feature_b': np.random.rand(100) * 50,
        'feature_c': np.random.randint(1, 7, size=100),
        'feature_d': np.random.rand(100) * 10
    }
    return pd.DataFrame(data)

# -----------------------------------
# Config Helpers (Mocked)
# -----------------------------------

def get_config_value(config_df, entity_id, column):
    """Fetch a configuration value (mock-safe)"""
    row = config_df[config_df['id'] == entity_id]

    if row.empty:
        raise ValueError(f"No record found for id={entity_id}")

    return row.iloc[0][column]


def get_mock_config():
    """Create a fake configuration dataset"""
    return pd.DataFrame({
        'id': [1, 2, 3],
        'param_1': [1.1, 1.2, 1.3],
        'param_2': [2.1, 2.2, 2.3],
        'meta': ['A', 'B', 'C']
    })

# -----------------------------------
# Processing Steps
# -----------------------------------

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Sort and remove null values"""
    return df.sort_values(by=['timestamp', 'step']).dropna()


def convert_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure consistent data types"""
    return df.astype({
        'step': int,
        'feature_a': float,
        'feature_b': float,
        'feature_c': int,
        'feature_d': float
    })


def feature_engineering(df: pd.DataFrame, entity_id: int, config_df: pd.DataFrame) -> pd.DataFrame:
    """Create derived features (demo-safe logic)"""

    df = df[(df['feature_c'] > 0) & (df['feature_c'] < 7)].copy()

    # Time step calculation
    df['delta'] = df['step'].diff().fillna(0)
    df['delta'] = np.where(df['delta'] < 0, df['delta'] + 100, df['delta'])

    # Simple derived metrics (non-proprietary)
    df['metric_1'] = df['feature_a'] * 0.1
    df['metric_2'] = df['feature_b'] / (DEFAULT_BASE_VALUE + 1)

    # Simulated transformation (safe replacement)
    for power in [2, 3]:
        df[f'estimate_{power}'] = (df['feature_a'] / (DEFAULT_BASE_VALUE + 1)) ** power

    # Config-driven feature (safe)
    param = get_config_value(config_df, entity_id, 'param_1')
    df['adjusted_value'] = df['feature_d'] * param

    return df


# -----------------------------------
# Main Pipeline
# -----------------------------------

def process_pipeline(root_path: str, entity_id: int):
    """End-to-end demo pipeline"""

    print("Loading files...")
    files = load_file_paths(root_path)

    print("Merging data...")
    df = merge_files(files)

    print("Cleaning data...")
    df = clean_data(df)

    print("Converting types...")
    df = convert_dtypes(df)

    print("Loading config...")
    config_df = get_mock_config()

    print("Generating features...")
    df = feature_engineering(df, entity_id, config_df)

    print("Pipeline completed successfully ✅")

    return df


# -----------------------------------
# Example Run
# -----------------------------------

if __name__ == "__main__":
    output_df = process_pipeline("demo_path", entity_id=1)
    print(output_df.head())