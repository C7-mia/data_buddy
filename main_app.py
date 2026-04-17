import sys
import pandas as pd
import numpy as np
import os
import zipfile

# Add core engine to path
sys.path.append('./data_buddy')
try:
    import project_analyzer
except ImportError:
    print("❌ Error: 'project_analyzer.py' not found in 'data_buddy' folder.")

# --- PART 1: The Statistical Tools ---
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

# --- PART 2: The Universal Analysis Engine ---
def run_outstanding_analysis(file_name):
    print(f"\n🌍 Universal Data_Buddy: Analyzing {file_name}")
    print("="*55)
    
    # Load and Clean (Engine now handles CSV, IPYNB, PNG, PDF)
    df, profile = project_analyzer.safe_load_and_clean(file_name)
    
    if df is None:
        # If it's not a DataFrame, it might be a message about a PNG/PDF/Notebook
        print(f"ℹ️  Result: {profile}")
        return

    # Use the Universal Cleaner for actual dataframes
    df = project_analyzer.universal_cleaner(df)

    # 1. Discovery Phase
    print(f"🔎 DISCOVERY: Found {df.shape[1]} variables and {df.shape[0]} observations.")
    
    # 2. Deep Insight Phase
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) == 0:
        print("📊 INFO: No numeric columns found for statistical analysis.")
    
    for col in numeric_cols:
        print(f"\n📊 INSIGHT: {col}")
        mean_val = df[col].mean()
        ci_low, ci_high = get_confidence_interval(df[col])
        outliers = get_iqr_outliers(df[col])
        
        print(f"  - Average Value: {mean_val:.2f}")
        print(f"  - 95% Confidence: ({ci_low} to {ci_high})")
        
        if outliers:
            print(f"  - 💡 ALERT: Found {len(outliers)} unusual data points (Outliers).")
        else:
            print(f"  - ✅ Consistency: Data is statistically stable.")

    print("\n" + "="*55)
    print("Strategy: Data-driven solutions ready.")

# --- PART 3: Interactive Start ---
if __name__ == "__main__":
    # LOOK FOR BOTH CSV AND ZIP FILES
    files = [f for f in os.listdir('.') if f.endswith('.csv') or f.endswith('.zip')]
    
    if not files:
        print("❌ No data files found in this folder!")
    else:
        print("Available Problems to Solve:", files)
        target = input("\n📁 Enter the filename (CSV or ZIP): ")
        
        if os.path.exists(target):
            # Special logic if the user picks a ZIP
            if target.endswith('.zip'):
                print(f"📦 Unzipping {target}...")
                folder, contents = project_analyzer.unpack_and_list_data(target)
                print(f"✅ Extracted to '{folder}'. Found: {contents}")
                
                # Ask which file inside the ZIP to analyze
                if contents:
                    sub_file = input(f"Which file from the ZIP should I analyze? ")
                    full_path = os.path.join(folder, sub_file)
                    if os.path.exists(full_path):
                        run_outstanding_analysis(full_path)
            else:
                run_outstanding_analysis(target)
        else:
            print(f"❌ '{target}' not found. Did you type it correctly?")