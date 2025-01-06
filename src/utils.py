import os
import pandas as pd
import calendar
from datetime import datetime
from itertools import product
from typing import Dict, Tuple


def test_env():
    """Check current environment for testing purposes"""
    return os.getenv("ENV") == "TEST"


def list_range(n=0):
    """Create a list of integers from 1 to n (inclusive)."""
    return [*range(1, n + 1)]


def month(month: int | None = None):
    """Returns the provided month or the current month if none is provided."""
    if month is not None:
        if not isinstance(month, int):
            raise ValueError(f"Invalid month: {month}. Month must be an integer.")
        if month < 1 or month > 12:
            raise ValueError(f"Invalid month: {month}. Month must be between 1 and 12.")
    return month if month else datetime.now().month


def year(year: int | None = None):
    """Returns the provided year or the current year if none is provided."""
    if year is not None:
        if not isinstance(year, int):
            raise ValueError(f"Invalid year: {year}. Year must be an integer.")
        if year < 0:
            raise ValueError(
                f"Invalid year: {year}. Year must be a non-negative integer."
            )
    return year if year else datetime.now().year


def num_days(year=None, month=None):
    """Get number of days in specific year and month"""
    if year is None:
        year = datetime.now().year
    if month is None:
        month = datetime.now().month
    _, total_days = calendar.monthrange(year, month)
    return total_days


def list_indices(*dimensions):
    """
    Generates a Cartesian product of indices for the given dimensions.

    Args:
        dimensions: Variable-length list of integers representing the range for each dimension.

    Returns:
        List of tuples representing the Cartesian product of indices.
    """
    if len(dimensions) == 0:
        return []  # Handle no dimensions gracefully
    if len(dimensions) == 1:
        # Return a flat list for a single dimension
        return [i for i in range(1, dimensions[0] + 1)]

    # Generate ranges and compute the Cartesian product
    ranges = [range(1, dim + 1) for dim in dimensions]
    return list(product(*ranges))


def competency_dict(data_frame: pd.DataFrame):
    """Get compency dictionary from panda data frame

    Args:
        data_frame (pd.DataFrame): data frame of excel file loaded by pandas

    Returns:
        dict: competency dictionary consists of personnel competency for each sections
    """
    first_column = data_frame.columns[0]
    re_indexed_data_frame = data_frame.set_index(first_column)
    re_indexed_dict = re_indexed_data_frame.to_dict(orient="index")

    _dict = {}
    for outer_key, inner_dict in re_indexed_dict.items():
        # Transform inner dictionary keys
        new_inner_dict = {
            int(key[key.index("(") + 1 : key.index(")")]): value
            for key, value in inner_dict.items()
        }
        _dict[outer_key] = new_inner_dict
    return _dict


def save_solution_dict(solution: dict):
    with open("./src/solution/solution.py", "w") as file:
        file.write(f"solution_dict = {solution}")


def group_solutions(solution_dict: dict) -> Tuple[dict, dict, dict]:
    grouped_data = {"X": {}, "h": {}, "d": {}}

    for key, value in solution_dict.items():
        if key.startswith("X"):
            grouped_data["X"][key] = value
        elif key.startswith("h"):
            grouped_data["h"][key] = value
        elif key.startswith("d"):
            grouped_data["d"][key] = value

    return (grouped_data["X"], grouped_data["h"], grouped_data["d"])
