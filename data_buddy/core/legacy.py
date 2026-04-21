"""Legacy helpers preserved for backward compatibility."""

from __future__ import annotations

import numpy as np

from data_buddy.core.buddy import Buddy


def _arr(data):
    arr = np.array(list(data), dtype=float)
    if arr.size == 0:
        raise ValueError("Data cannot be empty")
    return arr


def get_average(data):
    return float(np.mean(_arr(data)))


def get_median(data):
    return float(np.median(_arr(data)))


def get_min(data):
    return float(np.min(_arr(data)))


def get_max(data):
    return float(np.max(_arr(data)))


def get_mode(data):
    arr = _arr(data)
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


def run_no_code_analysis(file_name: str):
    buddy = Buddy().load(file_name).clean()
    return {"success": True, "summary": buddy.insight()}
