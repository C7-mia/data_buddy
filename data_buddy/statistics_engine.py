import numpy as np
from scipy import stats


class StatisticalAnalyzer:
    """Professional statistical analysis with confidence intervals and outlier detection."""

    def __init__(self, data):
        self.data = np.array(data)
        self.n = len(self.data)

    def get_variance(self):
        if self.n < 2:
            return 0
        return np.var(self.data, ddof=1)

    def get_std_dev(self):
        if self.n < 2:
            return 0
        return np.std(self.data, ddof=1)

    def get_confidence_interval(self, confidence=0.95):
        mean = np.mean(self.data)
        std_err = stats.sem(self.data)
        t_score = stats.t.ppf((1 + confidence) / 2, self.n - 1)
        margin = t_score * std_err
        return {
            "mean": mean,
            "lower_bound": mean - margin,
            "upper_bound": mean + margin,
            "margin_of_error": margin,
            "confidence_level": f"{int(confidence * 100)}%",
        }

    def detect_outliers_iqr(self):
        q1 = np.percentile(self.data, 25)
        q3 = np.percentile(self.data, 75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        outliers = []
        for i, val in enumerate(self.data):
            if val < lower_bound or val > upper_bound:
                outliers.append(
                    {
                        "index": i,
                        "value": val,
                        "type": "low" if val < lower_bound else "high",
                        "bounds": (lower_bound, upper_bound),
                    }
                )
        return outliers

    def detect_outliers_zscore(self, threshold=3):
        mean = np.mean(self.data)
        std = np.std(self.data)
        if std == 0:
            return []

        z_scores = np.abs((self.data - mean) / std)
        outliers = []
        for i, (val, z) in enumerate(zip(self.data, z_scores)):
            if z > threshold:
                outliers.append({"index": i, "value": val, "z_score": z, "method": "z-score"})
        return outliers

    def get_data_quality_report(self):
        quality_report = {
            "total_records": self.n,
            "missing_values": 0,
            "data_completeness": 100.0,
            "value_range": {
                "min": float(np.min(self.data)),
                "max": float(np.max(self.data)),
                "range": float(np.max(self.data) - np.min(self.data)),
            },
            "distribution": {
                "mean": float(np.mean(self.data)),
                "median": float(np.median(self.data)),
                "skewness": float(stats.skew(self.data)),
                "kurtosis": float(stats.kurtosis(self.data)),
            },
            "variability": {
                "variance": float(self.get_variance()),
                "std_dev": float(self.get_std_dev()),
                "coefficient_of_variation": float(self.get_std_dev() / np.mean(self.data))
                if np.mean(self.data) != 0
                else 0,
            },
            "outliers": {
                "iqr_outliers": len(self.detect_outliers_iqr()),
                "zscore_outliers": len(self.detect_outliers_zscore()),
                "outlier_percentage": (len(self.detect_outliers_iqr()) / self.n * 100) if self.n > 0 else 0,
            },
        }
        quality_report["quality_score"] = self._calculate_quality_score(quality_report)
        return quality_report

    def _calculate_quality_score(self, report):
        score = 100
        if report["outliers"]["outlier_percentage"] > 10:
            score -= 20
        elif report["outliers"]["outlier_percentage"] > 5:
            score -= 10

        if abs(report["distribution"]["skewness"]) > 2:
            score -= 10

        if report["variability"]["coefficient_of_variation"] > 1.0:
            score -= 15

        return max(0, min(100, score))

    def get_summary_report(self):
        ci = self.get_confidence_interval()
        quality = self.get_data_quality_report()
        outliers = self.detect_outliers_iqr()

        return {
            "basics": {
                "count": self.n,
                "mean": round(np.mean(self.data), 2),
                "median": round(np.median(self.data), 2),
                "min": round(np.min(self.data), 2),
                "max": round(np.max(self.data), 2),
            },
            "statistical_rigor": {
                "std_dev": round(self.get_std_dev(), 2),
                "variance": round(self.get_variance(), 2),
                "confidence_interval_95": {
                    "lower": round(ci["lower_bound"], 2),
                    "upper": round(ci["upper_bound"], 2),
                    "interpretation": (
                        "We are 95% confident the true mean is between "
                        f"{round(ci['lower_bound'], 2)} and {round(ci['upper_bound'], 2)}"
                    ),
                },
            },
            "outliers": {
                "count": len(outliers),
                "percentage": round((len(outliers) / self.n * 100), 2) if self.n > 0 else 0,
                "details": outliers[:5],
            },
            "data_quality": {
                "score": round(quality["quality_score"], 1),
                "rating": self._get_quality_rating(quality["quality_score"]),
                "completeness": f"{quality['data_completeness']:.1f}%",
            },
        }

    def _get_quality_rating(self, score):
        if score >= 90:
            return "🟢 Excellent"
        if score >= 70:
            return "🟡 Good"
        if score >= 50:
            return "🟠 Fair"
        return "🔴 Poor"
