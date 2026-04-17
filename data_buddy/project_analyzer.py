import pandas as pd
import numpy as np
import zipfile
import os
import json

# Try to import extra libraries for PNG and PDF support
try:
    from PIL import Image
except ImportError:
    Image = None

def safe_load_and_clean(file_name):
    """
    The Universal Loader: Now detects .csv, .ipynb, .png, and .pdf
    """
    ext = os.path.splitext(file_name)[1].lower()
    
    try:
        # 1. HANDLE CSV
        if ext == '.csv':
            df = pd.read_csv(file_name)
            if df.empty: return None, "Error: CSV is empty."
            profile = {'shape': df.shape, 'columns': list(df.columns), 'type': 'Tabular Data'}
            return df, profile

        # 2. HANDLE NOTEBOOKS (.ipynb)
        elif ext == '.ipynb':
            return None, extract_csv_from_ipynb(file_name)

        # 3. HANDLE IMAGES (.png)
        elif ext == '.png':
            if Image:
                img = Image.open(file_name)
                return None, f"🎨 Image Detected: {img.size} size, {img.format} format."
            return None, "🎨 Image found, but 'Pillow' library is not installed."

        # 4. HANDLE PDF
        elif ext == '.pdf':
            return None, "📄 PDF Detected. (Full text extraction requires 'PyPDF2' library)."

        else:
            return None, f"Error: Format {ext} not supported yet."

    except Exception as e:
        return None, f"System Error: {str(e)}"

def universal_cleaner(df):
    """Automatically detects and fixes common data flaws in any dataset."""
    if df is None: return None
    
    # 1. Handle Strings in Numeric Columns
    for col in df.columns:
        if df[col].dtype == 'object':
            converted = pd.to_numeric(df[col], errors='coerce')
            if converted.notnull().sum() > (len(df) * 0.8):
                df[col] = converted.fillna(converted.median())

    # 2. Logic Protection (Absolutes)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if (df[col] >= 0).sum() > (len(df) * 0.95):
            df[col] = df[col].abs()

    # 3. Universal Text Standardization (Title Case)
    text_cols = df.select_dtypes(include=['object']).columns
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip().str.title()
        
    return df

def unpack_and_list_data(zip_name):
    """Unzips a file and finds all usable content inside."""
    try:
        with zipfile.ZipFile(zip_name, 'r') as zip_ref:
            folder_name = "extracted_data"
            zip_ref.extractall(folder_name)
            all_files = os.listdir(folder_name)
            return folder_name, all_files
    except Exception as e:
        return None, f"Unzip Error: {str(e)}"

def extract_csv_from_ipynb(ipynb_file):
    """Attempts to scan a Notebook for data structures."""
    try:
        with open(ipynb_file, 'r', encoding='utf-8') as f:
            nb = json.load(f)
            code_cells = 0
            for cell in nb['cells']:
                if cell['cell_type'] == 'code':
                    code_cells += 1
            return f"📓 Notebook detected with {code_cells} code cells. Run it to generate CSVs."
    except Exception as e:
        return f"Error reading notebook: {e}"


# --- PART 3: Statistical Rigor Analysis ---
def run_rigorous_analysis(filename):
    """
    Run comprehensive statistical analysis with confidence intervals, 
    variance, and outlier detection.
    """
    from .statistics_engine import StatisticalAnalyzer
    
    try:
        with open(filename, 'r') as file:
            data = [float(line.strip()) for line in file if line.strip()]
        
        if not data:
            print("❌ Error: File is empty.")
            return
        
        analyzer = StatisticalAnalyzer(data)
        report = analyzer.get_summary_report()
        
        print(f"\n{'='*60}")
        print(f"📊 RIGOROUS STATISTICAL ANALYSIS: {filename}")
        print(f"{'='*60}\n")
        
        # Basic statistics
        print("📈 BASIC STATISTICS:")
        print(f"  • Sample Size: {report['basics']['count']}")
        print(f"  • Mean: {report['basics']['mean']}")
        print(f"  • Median: {report['basics']['median']}")
        print(f"  • Range: [{report['basics']['min']}, {report['basics']['max']}]")
        
        # Statistical rigor
        print("\n📐 STATISTICAL RIGOR:")
        print(f"  • Std Dev: {report['statistical_rigor']['std_dev']}")
        print(f"  • Variance: {report['statistical_rigor']['variance']}")
        ci = report['statistical_rigor']['confidence_interval_95']
        print(f"  • 95% CI: [{ci['lower']}, {ci['upper']}]")
        print(f"  • {ci['interpretation']}")
        
        # Outliers
        print("\n⚠️  OUTLIER DETECTION:")
        print(f"  • Outliers Found: {report['outliers']['count']} ({report['outliers']['percentage']}%)")
        if report['outliers']['details']:
            print(f"  • Examples:")
            for outlier in report['outliers']['details']:
                print(f"    - Position {outlier['index']}: {outlier['value']} ({outlier['type']})")
        
        # Data Quality
        print("\n✅ DATA QUALITY ASSESSMENT:")
        print(f"  • Quality Score: {report['data_quality']['score']}/100 {report['data_quality']['rating']}")
        print(f"  • Completeness: {report['data_quality']['completeness']}")
        
        print(f"\n{'='*60}\n")
        
        return analyzer
        
    except Exception as e:
        print(f"❌ Analysis Error: {e}")
        return None
