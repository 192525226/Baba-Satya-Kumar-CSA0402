"""
Utility Functions for UniCore OS Resource Orchestration System
Course: CSA04 Operating Systems

Provides helper functions for:
- Loading configuration & workload JSON datasets
- Exporting CSV benchmark tables
- Formatted console display of OS metrics
- Mathematical validations
"""

import json
import csv
import os
from typing import Dict, List, Any, Tuple


def get_project_root() -> str:
    """Returns absolute path to the UniCore project root directory."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, ".."))


def load_json_data(relative_path: str) -> Any:
    """Loads a JSON file relative to the project root or data directory."""
    root = get_project_root()
    full_path = os.path.join(root, relative_path)
    if not os.path.exists(full_path):
        # Fallback to checking data directory directly
        alt_path = os.path.join(root, "data", os.path.basename(relative_path))
        if os.path.exists(alt_path):
            full_path = alt_path
        else:
            raise FileNotFoundError(f"Data file not found at: {full_path} or {alt_path}")
    
    with open(full_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_csv_results(relative_path: str, headers: List[str], rows: List[List[Any]]) -> str:
    """Saves structured metrics to a CSV file in the results directory."""
    root = get_project_root()
    full_path = os.path.join(root, relative_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    with open(full_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    return full_path


def save_text_results(relative_path: str, content: str) -> str:
    """Saves text report to a file in the results directory."""
    root = get_project_root()
    full_path = os.path.join(root, relative_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    return full_path


def format_table(headers: List[str], rows: List[List[Any]], col_widths: List[int] = None) -> str:
    """Formats headers and rows into a clean ASCII table."""
    if col_widths is None:
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, val in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(val)))
        col_widths = [w + 2 for w in col_widths]

    header_line = " | ".join(f"{h:<{col_widths[i]}}" for i, h in enumerate(headers))
    separator = "-+-".join("-" * col_widths[i] for i in range(len(headers)))
    row_lines = []
    for row in rows:
        row_str = " | ".join(f"{str(val):<{col_widths[i]}}" for i, val in enumerate(row))
        row_lines.append(row_str)

    return f"{header_line}\n{separator}\n" + "\n".join(row_lines)
