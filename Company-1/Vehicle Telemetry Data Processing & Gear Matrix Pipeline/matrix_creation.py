import pandas as pd
import numpy as np
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

# Validation

def validate_input(df: pd.DataFrame, cols: list):
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


# Matrix Creation

def create_gear_matrix(
    df: pd.DataFrame,
    speed_col: str = "Spd",
    torque_col: str = "Trq",
    mileage_col: str = "Mileage"
) -> Dict[str, Any]:
    """
    Create gear matrix using speed and torque bands.
    """

    logger.info("Creating gear matrix")

    # Validation
    validate_input(df, [speed_col, torque_col, mileage_col])

    # Work on copy
    gear_df = df.copy()

    # Define bins
    spd_bins = list(range(-25, 1426, 50))
    spd_labels = list(range(0, 1401, 50))

    torque_bins = list(range(-325, 726, 50))
    torque_labels = list(range(-300, 701, 50))

    # Binning
    gear_df["spd_band"] = pd.cut(
        gear_df[speed_col],
        bins=spd_bins,
        labels=spd_labels,
        right=False
    )

    gear_df["torque_band"] = pd.cut(
        gear_df[torque_col],
        bins=torque_bins,
        labels=torque_labels,
        right=False
    )

    # Drop invalid rows
    gear_df = gear_df.dropna(subset=["spd_band", "torque_band"])

    # Aggregation
    grouped = (
        gear_df
        .groupby(["torque_band", "spd_band"])[mileage_col]
        .sum()
        .reset_index()
    )

    # Pivot
    matrix_df = (
        grouped
        .pivot(index="torque_band", columns="spd_band", values=mileage_col)
        .fillna(0)
        .sort_index(ascending=False)
    )

    # Convert to numpy
    matrix = matrix_df.values

    total = matrix.sum()

    mileage_values = matrix
    mileage_percentages = np.divide(
        matrix,
        total,
        where=total != 0
    )

    # Return structured output
    result = {
        "mileage_values": mileage_values,
        "mileage_percentages": mileage_percentages,
        "speed_labels": list(matrix_df.columns),
        "torque_labels": list(matrix_df.index),
        "total_mileage": float(total)
    }

    logger.info("Gear matrix created successfully")

    return result
