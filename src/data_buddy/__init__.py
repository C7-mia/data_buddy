"""Public API for the Data Buddy package."""

from data_buddy.core.buddy import Buddy
from data_buddy.core.legacy import (
    add,
    div,
    get_average,
    get_max,
    get_median,
    get_min,
    get_mode,
    mul,
    power,
    run_no_code_analysis,
    sqrt,
    sub,
)
from data_buddy.stats.statistics_engine import StatisticalAnalyzer

__all__ = [
    "Buddy",
    "get_average",
    "get_median",
    "get_min",
    "get_max",
    "get_mode",
    "add",
    "sub",
    "mul",
    "div",
    "power",
    "sqrt",
    "run_no_code_analysis",
    "StatisticalAnalyzer",
]
