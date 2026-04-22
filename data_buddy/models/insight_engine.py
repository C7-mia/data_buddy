"""Insight and lightweight predictive utilities."""

from __future__ import annotations

import pandas as pd

from data_buddy.utils.errors import BuddyValidationError


def generate_insight(df: pd.DataFrame, target: str | None = None) -> dict:
    """Generate business-friendly insights and optional regression summary.

    Args:
        df: Dataset to analyze.
        target: Optional numeric target column for regression.

    Returns:
        Dictionary containing plain-language insights and model details.

    Example:
        >>> insights = generate_insight(df, target="sales")
    """

    numeric = df.select_dtypes(include="number")
    if numeric.empty:
        raise BuddyValidationError(
            "Data Buddy couldn't find numeric columns for insight generation."
        )

    summaries = {
        col: {
            "average": float(numeric[col].mean()),
            "volatility": float(
                numeric[col].std(ddof=1) if len(numeric[col]) > 1 else 0.0
            ),
            "business_note": (
                "Stable metric"
                if numeric[col].std(ddof=0) < abs(numeric[col].mean() * 0.1)
                else "Shows meaningful fluctuation"
            ),
        }
        for col in numeric.columns
    }

    result = {"high_level_summary": summaries, "model": None}

    if target and target in numeric.columns and len(numeric.columns) > 1:
        try:
            import statsmodels.api as sm  # lazy import
        except ImportError as exc:
            raise BuddyValidationError(
                "Install Data Buddy ML extras to run regression insights: pip install data-buddy[ml]"
            ) from exc

        predictors = numeric.drop(columns=[target])
        x = sm.add_constant(predictors)
        y = numeric[target]
        model = sm.OLS(y, x).fit()

        best_feature = model.params.drop("const", errors="ignore").abs().idxmax()
        result["model"] = {
            "target": target,
            "r_squared": float(model.rsquared),
            "top_driver": best_feature,
            "plain_english": (
                f"{best_feature} appears to be the strongest driver of {target} in this dataset."
            ),
        }

    return result
