"""Smart data cleaning engine."""

from __future__ import annotations

import pandas as pd


def smart_clean(df: pd.DataFrame, strategy_override: dict[str, str] | None = None) -> pd.DataFrame:
    """Automatically clean missing values using distribution-aware rules.

    Args:
        df: Source DataFrame to clean.
        strategy_override: Optional per-column override: ``{"col": "mean|median|mode"}``.

    Returns:
        Cleaned DataFrame with missing values imputed.

    Example:
        >>> cleaned = smart_clean(df)
    """

    strategy_override = strategy_override or {}
    cleaned = df.copy()

    for column in cleaned.columns:
        series = cleaned[column]
        if not series.isna().any():
            continue

        chosen = strategy_override.get(column)
        if chosen is None:
            if pd.api.types.is_numeric_dtype(series):
                skewness = series.dropna().skew()
                chosen = "mean" if abs(skewness) < 0.5 else "median"
            else:
                chosen = "mode"

        if chosen == "mean":
            cleaned[column] = series.fillna(series.mean())
        elif chosen == "median":
            cleaned[column] = series.fillna(series.median())
        else:
            mode = series.mode(dropna=True)
            fill_value = mode.iloc[0] if not mode.empty else "Unknown"
            cleaned[column] = series.fillna(fill_value)

    return cleaned
