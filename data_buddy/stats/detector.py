"""Statistical detection and anomaly helpers."""

from __future__ import annotations

import numpy as np
import pandas as pd


def detect_anomalies(df: pd.DataFrame, z_threshold: float = 3.0) -> dict:
    """Run distribution checks and hybrid outlier detection.

    Args:
        df: Input dataset.
        z_threshold: Absolute z-score threshold for anomaly flagging.

    Returns:
        Dictionary with per-column summaries and anomaly indexes.

    Example:
        >>> report = detect_anomalies(df)
    """

    report: dict[str, dict] = {}
    numeric_cols = df.select_dtypes(include=[np.number]).columns

    for col in numeric_cols:
        series = df[col].dropna()
        if series.empty:
            continue

        q1 = np.percentile(series, 25)
        q3 = np.percentile(series, 75)
        iqr = q3 - q1
        lower = q1 - (1.5 * iqr)
        upper = q3 + (1.5 * iqr)

        std = series.std(ddof=0)
        z_scores = (
            np.zeros(len(series)) if std == 0 else ((series - series.mean()) / std)
        )

        iqr_idx = series[(series < lower) | (series > upper)].index.tolist()
        z_idx = series[np.abs(z_scores) > z_threshold].index.tolist()

        report[col] = {
            "distribution": {
                "mean": float(series.mean()),
                "median": float(series.median()),
                "skew": float(series.skew()),
                "kurtosis": float(series.kurtosis()),
            },
            "outliers": {
                "iqr_indexes": iqr_idx,
                "zscore_indexes": z_idx,
                "hybrid_indexes": sorted(set(iqr_idx).union(z_idx)),
            },
        }

    return {
        "columns": report,
        "row_count": len(df),
        "numeric_columns": len(numeric_cols),
    }
