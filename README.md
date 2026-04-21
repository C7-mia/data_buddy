# Data Buddy 📊

**Data Buddy** is a no-code, open-source data analysis toolkit for business users, analysts, and developers who want fast insights from raw files without building pipelines from scratch.

It combines a simple API with robust statistical tooling, automatic retry behavior for transient failures, and report-generation utilities.

## Features

- **No-code statistical analysis API** via `run_no_code_analysis(...)` for one-call summaries from tabular files.
- **Advanced statistical engine** with confidence intervals, variance/standard deviation, outlier detection (IQR + z-score), and data quality scoring through `StatisticalAnalyzer`.
- **Automatic retry logic** (exponential backoff + jitter) for transient read/IO failures during analysis workflows.
- **Multi-format loading** support for:
  - CSV datasets (fully analyzed)
  - Jupyter notebooks (`.ipynb`) with notebook metadata hints
  - Images (`.png`) with file metadata hints
  - PDF files (`.pdf`) with extraction guidance
- **Report generation utilities**:
  - Line-chart visual reports (`business_chart.png` by default)
  - Auto-generated Python analysis script (`generated_analysis.py`)

## Architecture Overview

Data Buddy is organized around two core analysis layers:

- **`data_buddy/project_analyzer.py`**
  - Public no-code operations (`run_no_code_analysis`, `create_visual_report`, `generate_notebook_code`)
  - Resilient file loading (`safe_load_and_clean`)
  - Retry helpers (`retry_with_exponential_backoff`, `is_transient_error`)
  - Numeric/statistics helper functions
- **`data_buddy/statistics_engine.py`**
  - `StatisticalAnalyzer` class for deeper statistical rigor:
    - Confidence intervals
    - Outlier detection (IQR and z-score)
    - Distribution and variability metrics
    - Data quality report and quality rating

Both layers are exported from `data_buddy/__init__.py` so open-source users can access either the no-code workflow or a deeper statistics API from a single package import.

## Automatic Retry Logic (Exponential Backoff + Jitter)

Data Buddy now includes built-in retry behavior for transient failures during data loading/analysis.

### How it works

- `retry_with_exponential_backoff(...)` wraps operations that may fail temporarily.
- Delay grows exponentially by attempt (`base_delay_seconds * 2^(attempt-1)`), capped by `max_delay_seconds`.
- A random jitter component is added to avoid synchronized retry spikes.
- Retries stop when:
  - the maximum attempt count is reached, or
  - an error is classified as non-transient.

### Transient error handling

An error is treated as retryable when it is:
- a known transient exception type (`TimeoutError`, `ConnectionError`, `OSError`), or
- an exception message containing transient markers such as timeout/rate-limit/service-unavailable style signals.

### Where retries are applied

`safe_load_and_clean(...)` applies this mechanism to CSV reads (`pandas.read_csv`) so short-lived IO/network-like issues do not immediately fail user analysis flows.

## Installation

Data Buddy uses a modern **`pyproject.toml`** build configuration with `setuptools.build_meta`.

### Editable install (recommended for contributors)

```bash
python -m pip install -e .
```

### Optional development tools

```bash
python -m pip install -e .[dev]
```

This installs linting/format/test tooling defined under optional dependencies (e.g., `pytest`, `black`, `flake8`).

## Quick Start

```python
import data_buddy

# One-call no-code analysis
result = data_buddy.run_no_code_analysis("expenses.csv")
print(result)

# Generate a visual report
chart_path = data_buddy.create_visual_report("expenses.csv")
print(chart_path)  # business_chart.png

# Generate reusable Python analysis code
code_path = data_buddy.generate_notebook_code("expenses.csv")
print(code_path)   # generated_analysis.py
```

## Statistics API (StatisticalAnalyzer)

Use `StatisticalAnalyzer` when you want deeper statistical diagnostics.

```python
from data_buddy import StatisticalAnalyzer

analyzer = StatisticalAnalyzer([85, 90, 78, 92, 88, 500])
report = analyzer.get_summary_report()
print(report["data_quality"])
```

Useful methods include:
- `get_variance()`, `get_std_dev()`
- `get_confidence_interval(confidence=0.95)`
- `detect_outliers_iqr()`, `detect_outliers_zscore(threshold=3)`
- `get_data_quality_report()`, `get_summary_report()`

## Development

### Run tests

Data Buddy includes a pytest suite for the updated architecture.

```bash
pytest -q
```

### Typical contributor flow

```bash
python -m pip install -e .[dev]
pytest -q
```

## Project Structure

```text
data_buddy/
├── data_buddy/
│   ├── __init__.py
│   ├── project_analyzer.py
│   └── statistics_engine.py
├── pyproject.toml
├── README.md
└── test_*.py
```

## License

Add your preferred open-source license (for example, MIT) in this repository.
