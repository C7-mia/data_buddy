"""Backwards-compatible statistical analyzer."""

from __future__ import annotations

import numpy as np
from scipy import stats


class StatisticalAnalyzer:
    """Professional statistical analysis with confidence intervals and outlier detection."""

    def __init__(self, data):
        self.data = np.array(data)
        self.n = len(self.data)

    def get_variance(self):
        return 0 if self.n < 2 else np.var(self.data, ddof=1)

    def get_std_dev(self):
        return 0 if self.n < 2 else np.std(self.data, ddof=1)

    def get_confidence_interval(self, confidence=0.95):
        mean = np.mean(self.data)
        std_err = stats.sem(self.data)
        t_score = stats.t.ppf((1 + confidence) / 2, self.n - 1)
        margin = t_score * std_err
        return {"mean": mean, "lower_bound": mean - margin, "upper_bound": mean + margin}

    def detect_outliers_iqr(self):
        q1 = np.percentile(self.data, 25)
        q3 = np.percentile(self.data, 75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        return [val for val in self.data if val < lower_bound or val > upper_bound]

    def get_summary_report(self):
        ci = self.get_confidence_interval()
        outliers = self.detect_outliers_iqr()
        return {
            "basics": {"count": self.n, "mean": round(np.mean(self.data), 2)},
            "statistical_rigor": {"std_dev": round(self.get_std_dev(), 2), "confidence_interval_95": ci},
            "outliers": {"count": len(outliers)},
            "data_quality": {"score": 100 - min(100, len(outliers) * 5)},
        }
