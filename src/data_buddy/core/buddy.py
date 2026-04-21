"""Facade API for no-code, low-code data workflows."""

from __future__ import annotations

import numpy as np
import pandas as pd

from data_buddy.models.insight_engine import generate_insight
from data_buddy.preprocessing.cleaner import smart_clean
from data_buddy.preprocessing.loader import load_data
from data_buddy.stats.detector import detect_anomalies
from data_buddy.viz.viewer import auto_view


class Buddy:
    """Primary orchestration class for Data Buddy workflows.

    Example:
        >>> from data_buddy import Buddy
        >>> buddy = Buddy().load("sales.csv").clean()
        >>> report = buddy.detect()
    """

    def __init__(self, dataframe: pd.DataFrame | None = None):
        self.df = dataframe
        self.table = pd
        self.math = np

    def load(self, file_path_or_url: str):
        """Load data into Buddy from a local path or URL.

        Args:
            file_path_or_url: Local path or web URL.

        Returns:
            Self for fluent chaining.
        """

        self.df = load_data(file_path_or_url)
        return self

    def clean(self, strategy_override: dict[str, str] | None = None):
        """Apply smart missing-value cleaning.

        Args:
            strategy_override: Optional per-column imputation strategy.

        Returns:
            Self for fluent chaining.
        """

        self._ensure_loaded()
        self.df = smart_clean(self.df, strategy_override=strategy_override)
        return self

    def detect(self, z_threshold: float = 3.0) -> dict:
        """Detect anomalies and outliers from current dataset.

        Args:
            z_threshold: z-score threshold.

        Returns:
            Detection report.
        """

        self._ensure_loaded()
        return detect_anomalies(self.df, z_threshold=z_threshold)

    def insight(self, target: str | None = None) -> dict:
        """Generate plain-language insights and optional regression output.

        Args:
            target: Optional target column for regression.

        Returns:
            Insight dictionary.
        """

        self._ensure_loaded()
        return generate_insight(self.df, target=target)

    def view(self, mode: str = "auto", x: str | None = None, y: str | None = None):
        """Create charts with automatic type selection.

        Args:
            mode: auto/timeseries/categorical/numerical.
            x: Optional x-axis column.
            y: Optional y-axis column.

        Returns:
            Matplotlib figure.
        """

        self._ensure_loaded()
        return auto_view(self.df, mode=mode, x=x, y=y)

    def _ensure_loaded(self) -> None:
        if self.df is None:
            raise ValueError(
                "No data loaded yet. Start with Buddy.load('your_file.csv') before running this step."
            )
