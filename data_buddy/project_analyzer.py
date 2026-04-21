import json
import os
import random
import time
import zipfile
from typing import Any, Callable, Dict, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

try:
    from PIL import Image
except ImportError:  # optional dependency
    Image = None


# ---------- Retry utilities ----------
TRANSIENT_EXCEPTIONS = (
    TimeoutError,
    ConnectionError,
    OSError,
)


def is_transient_error(exc: Exception) -> bool:
    """Best-effort classification for retryable failures."""
    if isinstance(exc, TRANSIENT_EXCEPTIONS):
        return True

    message = str(exc).lower()
    transient_markers = (
        "tempor",
        "timeout",
        "timed out",
        "rate limit",
        "too many requests",
        "throttl",
        "connection reset",
        "connection aborted",
        "try again",
        "service unavailable",
    )
    return any(marker in message for marker in transient_markers)


def retry_with_exponential_backoff(
    operation: Callable[[], Any],
    *,
    max_attempts: int = 4,
    base_delay_seconds: float = 0.25,
    max_delay_seconds: float = 3.0,
    jitter_seconds: float = 0.25,
    retry_on: Callable[[Exception], bool] = is_transient_error,
) -> Any:
    """
    Execute an operation with automatic retries using exponential backoff + jitter.
    """
    attempt = 0
    while True:
        attempt += 1
        try:
            return operation()
        except Exception as exc:
            if attempt >= max_attempts or not retry_on(exc):
                raise

            delay = min(max_delay_seconds, base_delay_seconds * (2 ** (attempt - 1)))
            delay += random.uniform(0, jitter_seconds)
            time.sleep(delay)


# ---------- Basic stats + arithmetic ----------
def _to_numeric_array(data) -> np.ndarray:
    arr = np.array(list(data), dtype=float)
    if arr.size == 0:
        raise ValueError("Data cannot be empty")
    return arr


def get_average(data):
    arr = _to_numeric_array(data)
    return float(np.mean(arr))


def get_median(data):
    arr = _to_numeric_array(data)
    return float(np.median(arr))


def get_min(data):
    arr = _to_numeric_array(data)
    return float(np.min(arr))


def get_max(data):
    arr = _to_numeric_array(data)
    return float(np.max(arr))


def get_mode(data):
    arr = _to_numeric_array(data)
    values, counts = np.unique(arr, return_counts=True)
    return float(values[np.argmax(counts)])


def add(a, b):
    return a + b


def sub(a, b):
    return a - b


def mul(a, b):
    return a * b


def div(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b


def power(a, b):
    return a**b


def sqrt(x):
    if x < 0:
        raise ValueError("Cannot square-root a negative value")
    return float(np.sqrt(x))


# ---------- File loading + cleaning ----------
def safe_load_and_clean(file_name: str):
    """Universal loader for csv/ipynb/png/pdf with transient retry on read."""
    ext = os.path.splitext(file_name)[1].lower()

    try:
        if ext == ".csv":
            df = retry_with_exponential_backoff(lambda: pd.read_csv(file_name))
            if df.empty:
                return None, "Error: CSV is empty."
            profile = {
                "shape": df.shape,
                "columns": list(df.columns),
                "type": "Tabular Data",
            }
            return df, profile

        if ext == ".ipynb":
            return None, extract_csv_from_ipynb(file_name)

        if ext == ".png":
            if Image:
                img = Image.open(file_name)
                return None, f"🎨 Image Detected: {img.size} size, {img.format} format."
            return None, "🎨 Image found, but 'Pillow' library is not installed."

        if ext == ".pdf":
            return (
                None,
                "📄 PDF Detected. (Full text extraction requires 'PyPDF2' library).",
            )

        return None, f"Error: Format {ext} not supported yet."
    except Exception as e:
        return None, f"System Error: {str(e)}"


def universal_cleaner(df: Optional[pd.DataFrame]):
    if df is None:
        return None

    df = df.copy()

    for col in df.columns:
        if df[col].dtype == "object":
            converted = pd.to_numeric(df[col], errors="coerce")
            if converted.notnull().sum() > (len(df) * 0.8):
                df[col] = converted.fillna(converted.median())

    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if (df[col] >= 0).sum() > (len(df) * 0.95):
            df[col] = df[col].abs()

    text_cols = df.select_dtypes(include=["object"]).columns
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip().str.title()

    return df


def unpack_and_list_data(zip_name: str):
    try:
        with zipfile.ZipFile(zip_name, "r") as zip_ref:
            folder_name = "extracted_data"
            zip_ref.extractall(folder_name)
            all_files = os.listdir(folder_name)
            return folder_name, all_files
    except Exception as e:
        return None, f"Unzip Error: {str(e)}"


def extract_csv_from_ipynb(ipynb_file: str) -> str:
    try:
        with open(ipynb_file, "r", encoding="utf-8") as f:
            nb = json.load(f)

        code_cells = sum(
            1 for cell in nb.get("cells", []) if cell.get("cell_type") == "code"
        )
        return f"📓 Notebook detected with {code_cells} code cells. Run it to generate CSVs."
    except Exception as e:
        return f"Error reading notebook: {e}"


def generate_advanced_stats(df: pd.DataFrame) -> Dict[str, Any]:
    """Return dataframe-level stats used by legacy tests and API clients."""
    if df is None or df.empty:
        return {"error": "Empty dataframe"}

    cleaned = universal_cleaner(df)
    numeric_cols = cleaned.select_dtypes(include=[np.number]).columns.tolist()
    stats = {
        "shape": cleaned.shape,
        "columns": list(cleaned.columns),
        "numeric_columns": numeric_cols,
        "summary": {},
    }

    for col in numeric_cols:
        series = cleaned[col].dropna()
        stats["summary"][col] = {
            "mean": float(series.mean()),
            "median": float(series.median()),
            "std": float(series.std(ddof=1)) if len(series) > 1 else 0.0,
            "min": float(series.min()),
            "max": float(series.max()),
        }

    return stats


# ---------- No-code UX helpers ----------
def run_no_code_analysis(file_name: str) -> Dict[str, Any]:
    df, profile = safe_load_and_clean(file_name)
    if df is None:
        return {"success": False, "message": str(profile)}

    cleaned = universal_cleaner(df)
    numeric_cols = cleaned.select_dtypes(include=[np.number]).columns.tolist()
    if not numeric_cols:
        return {
            "success": True,
            "profile": profile,
            "message": "No numeric columns found.",
        }

    summary = {
        col: {
            "mean": float(cleaned[col].mean()),
            "median": float(cleaned[col].median()),
            "min": float(cleaned[col].min()),
            "max": float(cleaned[col].max()),
        }
        for col in numeric_cols
    }

    return {"success": True, "profile": profile, "summary": summary}


def create_visual_report(
    file_name: str, output_path: str = "business_chart.png"
) -> str:
    df, _ = safe_load_and_clean(file_name)
    if df is None:
        raise ValueError("Could not load a tabular dataset from the provided file")

    cleaned = universal_cleaner(df)
    numeric_cols = cleaned.select_dtypes(include=[np.number]).columns.tolist()
    if not numeric_cols:
        raise ValueError("No numeric columns available for charting")

    col = numeric_cols[0]
    ax = cleaned[col].plot(kind="line", title=f"Trend: {col}")
    ax.set_xlabel("Index")
    ax.set_ylabel(col)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    return output_path


def generate_notebook_code(
    file_name: str, output_path: str = "generated_analysis.py"
) -> str:
    code = f"""\
# --- Generated by Data_buddy ---
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("{file_name}")
print("📊 Data Summary:")
print(df.describe(include='all'))

numeric_cols = df.select_dtypes(include=['number']).columns
if len(numeric_cols) > 0:
    target = numeric_cols[0]
    df[target].plot(kind='line', title=f'Analysis Trend: {{target}}')
    plt.show()
else:
    print("No numeric columns found for plotting.")
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(code)
    return output_path
