"""Auto visualization layer for Data Buddy."""

from __future__ import annotations

import pandas as pd


def auto_view(
    df: pd.DataFrame, mode: str = "auto", x: str | None = None, y: str | None = None
):
    """Render an intelligent chart based on detected data type.

    Args:
        df: Dataset to visualize.
        mode: Visualization mode. Supported: ``auto``, ``timeseries``, ``categorical``, ``numerical``.
        x: Optional x-axis column.
        y: Optional y-axis column.

    Returns:
        Matplotlib figure object.

    Example:
        >>> fig = auto_view(df, mode="auto")
    """

    try:
        import matplotlib.pyplot as plt  # lazy import
        import seaborn as sns  # lazy import
    except ImportError as exc:
        raise ImportError(
            "Install visualization extras to use Buddy.view(): pip install data-buddy[viz]"
        ) from exc

    mode = mode.lower()
    inferred_mode = mode

    if mode == "auto":
        if x and y and pd.api.types.is_datetime64_any_dtype(df[x]):
            inferred_mode = "timeseries"
        elif y and pd.api.types.is_numeric_dtype(df[y]):
            inferred_mode = "numerical"
        else:
            inferred_mode = "categorical"

    fig, ax = plt.subplots(figsize=(10, 5))

    if inferred_mode == "timeseries":
        sns.lineplot(data=df, x=x, y=y, ax=ax)
        ax.set_title(f"Trend view: {y} over {x}")
    elif inferred_mode == "numerical":
        series = df[y] if y else df.select_dtypes(include="number").iloc[:, 0]
        sns.histplot(series.dropna(), kde=True, ax=ax)
        ax.set_title(f"Distribution view: {series.name}")
    else:
        cat = x or df.select_dtypes(exclude="number").columns[0]
        counts = df[cat].value_counts().head(20)
        sns.barplot(x=counts.index, y=counts.values, ax=ax)
        ax.set_title(f"Category summary: {cat}")
        ax.tick_params(axis="x", rotation=45)

    fig.tight_layout()
    return fig
