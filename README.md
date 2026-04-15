# Data Buddy 📊

A simple, modular Python package designed for quick data analysis. This project was built to demonstrate the fundamentals of Python packaging, backward compatibility, and version control.

## 🚀 Features
- **Average Calculation**: Quickly find the mean of a dataset.
- **Median Calculation**: Robust statistical analysis that handles outliers.
- **Developer Friendly**: Built with `pyproject.toml` for modern standards.

## 🛠️ Installation
To install this package in editable mode (perfect for development), clone the repository and run:
```bash
pip install -e .
#USAGE
📈 Usage
Here is how you can use Data Buddy in your own scripts
import data_buddy
data = [10,20,30,40,500]
print(f"Average:{data_buddy.get_average(data)}")
print(f"Median:{data_buddy.get_median(data)}")

🏗️ Project Structure
data_buddy/: Main package folder.
__init__.py: Package connector.
project_analyzer.py: Contains the core logic and functions.
test_buddy.py: A script to verify everything is working.

