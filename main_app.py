import sys
import pandas as pd
import numpy as np

# Pointing to your core logic folder
sys.path.append('./data_buddy')
try:
    import project_analyzer
except ImportError:
    print("❌ Error: 'project_analyzer.py' not found in 'data_buddy' folder.")

# --- PART 1: Statistical Engine ---
def get_iqr_outliers(series):
    """Detects outliers using the Interquartile Range method."""
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers = series[(series < lower_bound) | (series > upper_bound)]
    return outliers.tolist()

def get_confidence_interval(series):
    """Calculates a 95% confidence interval for a numeric column."""
    n = len(series)
    if n < 2: return (0, 0)
    mean = series.mean()
    std_err = series.std() / (n**0.5)
    h = std_err * 1.96 
    return (round(float(mean - h), 2), round(float(mean + h), 2))

# --- PART 2: The Report Generator ---
def run_outstanding_analysis(file_name):
    print(f"\n🚀 Data_Buddy Professional Report: {file_name}")
    print("="*45)
    
    # Load and clean via the engine
    df, profile = project_analyzer.safe_load_and_clean(file_name)
    if df is None:
        print(f"❌ Error: {profile}")
        return

    # Data Quality Summary
    missing = df.isnull().sum().sum()
    print(f"🛠️  QUALITY: {missing} missing values | {df.shape[0]} rows detected.")

    # Loop through numeric columns for deep analysis
    numeric_cols = df.select_dtypes(include=['number']).columns
    for col in numeric_cols:
        print(f"\n📊 COLUMN: {col}")
        
        mean_val = df[col].mean()
        ci_low, ci_high = get_confidence_interval(df[col])
        outliers = get_iqr_outliers(df[col])
        
        print(f"  - Average Value: {mean_val:.2f}")
        print(f"  - 95% Confidence: ({ci_low} to {ci_high})")
        
        if outliers:
            print(f"  - ⚠️ Outliers Detected: {outliers}")
        else:
            print(f"  - ✅ No Outliers found.")

    print("\n" + "="*45)
    print("Analysis Complete.")

# --- PART 3: Execution ---
if __name__ == "__main__":
    # Change 'expenses.csv' here if you want to test other files!
    run_outstanding_analysis('expenses.csv')