import numpy as np
import pandas as pd
import statistics
from scipy import stats

# --- STATISTICAL RIGOR MODULE ---
# Add confidence intervals, variance, std dev, and outlier detection

class StatisticalAnalyzer:
    """Professional statistical analysis with confidence intervals and outlier detection."""
    
    def __init__(self, data):
        """Initialize with data array."""
        self.data = np.array(data)
        self.n = len(self.data)
    
    # 1. VARIANCE & STANDARD DEVIATION
    def get_variance(self):
        """Calculate sample variance."""
        if self.n < 2:
            return 0
        return np.var(self.data, ddof=1)  # Sample variance
    
    def get_std_dev(self):
        """Calculate sample standard deviation."""
        if self.n < 2:
            return 0
        return np.std(self.data, ddof=1)
    
    # 2. CONFIDENCE INTERVALS (95% CI - most common)
    def get_confidence_interval(self, confidence=0.95):
        """
        Calculate 95% confidence interval for the mean.
        
        Returns: (lower_bound, upper_bound, margin_of_error)
        Example: If CI is (45, 55), we're 95% confident the true mean is between 45-55
        """
        mean = np.mean(self.data)
        std_err = stats.sem(self.data)  # Standard error of mean
        
        # t-score for confidence level
        t_score = stats.t.ppf((1 + confidence) / 2, self.n - 1)
        margin = t_score * std_err
        
        return {
            'mean': mean,
            'lower_bound': mean - margin,
            'upper_bound': mean + margin,
            'margin_of_error': margin,
            'confidence_level': f"{int(confidence * 100)}%"
        }
    
    # 3. OUTLIER DETECTION (IQR Method)
    def detect_outliers_iqr(self):
        """
        Detect outliers using Interquartile Range (IQR) method.
        Values beyond 1.5 * IQR are flagged as outliers.
        
        Returns: List of outlier values with their positions
        """
        Q1 = np.percentile(self.data, 25)
        Q3 = np.percentile(self.data, 75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = []
        for i, val in enumerate(self.data):
            if val < lower_bound or val > upper_bound:
                outliers.append({
                    'index': i,
                    'value': val,
                    'type': 'low' if val < lower_bound else 'high',
                    'bounds': (lower_bound, upper_bound)
                })
        
        return outliers
    
    def detect_outliers_zscore(self, threshold=3):
        """
        Detect outliers using Z-Score method.
        Values with |z-score| > threshold are outliers (default: 3 sigma rule).
        """
        mean = np.mean(self.data)
        std = np.std(self.data)
        
        if std == 0:
            return []
        
        z_scores = np.abs((self.data - mean) / std)
        outliers = []
        
        for i, (val, z) in enumerate(zip(self.data, z_scores)):
            if z > threshold:
                outliers.append({
                    'index': i,
                    'value': val,
                    'z_score': z,
                    'method': 'z-score'
                })
        
        return outliers
    
    # 4. DATA QUALITY METRICS
    def get_data_quality_report(self):
        """
        Generate comprehensive data quality metrics.
        
        Returns: Dictionary with quality indicators
        """
        quality_report = {
            'total_records': self.n,
            'missing_values': 0,  # Already filtered
            'data_completeness': 100.0,
            'value_range': {
                'min': float(np.min(self.data)),
                'max': float(np.max(self.data)),
                'range': float(np.max(self.data) - np.min(self.data))
            },
            'distribution': {
                'mean': float(np.mean(self.data)),
                'median': float(np.median(self.data)),
                'skewness': float(stats.skew(self.data)),  # Distribution shape
                'kurtosis': float(stats.kurtosis(self.data))  # Tail heaviness
            },
            'variability': {
                'variance': float(self.get_variance()),
                'std_dev': float(self.get_std_dev()),
                'coefficient_of_variation': float(self.get_std_dev() / np.mean(self.data)) if np.mean(self.data) != 0 else 0
            },
            'outliers': {
                'iqr_outliers': len(self.detect_outliers_iqr()),
                'zscore_outliers': len(self.detect_outliers_zscore()),
                'outlier_percentage': (len(self.detect_outliers_iqr()) / self.n * 100) if self.n > 0 else 0
            }
        }
        
        # Interpret data quality
        quality_report['quality_score'] = self._calculate_quality_score(quality_report)
        
        return quality_report
    
    def _calculate_quality_score(self, report):
        """
        Calculate overall data quality score (0-100).
        - 90-100: Excellent
        - 70-89: Good
        - 50-69: Fair
        - <50: Poor
        """
        score = 100
        
        # Penalize for high outlier percentage
        if report['outliers']['outlier_percentage'] > 10:
            score -= 20
        elif report['outliers']['outlier_percentage'] > 5:
            score -= 10
        
        # Check for extreme skewness
        if abs(report['distribution']['skewness']) > 2:
            score -= 10
        
        # Check for high variation
        cv = report['variability']['coefficient_of_variation']
        if cv > 1.0:
            score -= 15
        
        return max(0, min(100, score))  # Keep between 0-100
    
    # 5. SUMMARY REPORT (for no-code users)
    def get_summary_report(self):
        """Human-readable summary of all statistics."""
        ci = self.get_confidence_interval()
        quality = self.get_data_quality_report()
        outliers = self.detect_outliers_iqr()
        
        return {
            'basics': {
                'count': self.n,
                'mean': round(np.mean(self.data), 2),
                'median': round(np.median(self.data), 2),
                'min': round(np.min(self.data), 2),
                'max': round(np.max(self.data), 2),
            },
            'statistical_rigor': {
                'std_dev': round(self.get_std_dev(), 2),
                'variance': round(self.get_variance(), 2),
                'confidence_interval_95': {
                    'lower': round(ci['lower_bound'], 2),
                    'upper': round(ci['upper_bound'], 2),
                    'interpretation': f"We are 95% confident the true mean is between {round(ci['lower_bound'], 2)} and {round(ci['upper_bound'], 2)}"
                }
            },
            'outliers': {
                'count': len(outliers),
                'percentage': round((len(outliers) / self.n * 100), 2) if self.n > 0 else 0,
                'details': outliers[:5]  # Show first 5
            },
            'data_quality': {
                'score': round(quality['quality_score'], 1),
                'rating': self._get_quality_rating(quality['quality_score']),
                'completeness': f"{quality['data_completeness']:.1f}%"
            }
        }
    
    def _get_quality_rating(self, score):
        """Convert score to readable rating."""
        if score >= 90:
            return "🟢 Excellent"
        elif score >= 70:
            return "🟡 Good"
        elif score >= 50:
            return "🟠 Fair"
        else:
            return "🔴 Poor"
