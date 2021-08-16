""" Tools for redaction """
from typing import Dict

import pandas as pd


def contains_small_numbers(table: pd.DataFrame, threshold: int = 5) -> bool:
    """Does `table` contain numbers less than or equal to `threshold`?"""
    return table.le(threshold).any(axis=None)


def process_table_request(table: pd.DataFrame, cols: Dict, threshold: int = 5):
    """Make a crosstab from `cols` in `table`.

    If the crosstab would contain numbers less than or equal to `threshold`, then return
    "REDACTED" instead.
    """
    # Make crosstab table
    table = pd.crosstab(table[cols[0]], table[cols[1]])
    table_variables = [cols[0], cols[1]]

    # Check if redaction needed
    redaction_needed = contains_small_numbers(table=table, threshold=threshold)

    # if redacted needed then return redacted table
    if redaction_needed:
        final_table = "REDACTED"
    else:
        final_table = table

    return table_variables, final_table
