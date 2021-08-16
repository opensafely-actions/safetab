""" Tools for redaction """
from typing import Dict

import pandas as pd


def contains_small_numbers(table: pd.DataFrame, threshold: int = 5) -> bool:
    """Does `table` contain numbers less than or equal to `threshold`?"""
    return table.le(threshold).any(axis=None)


def process_table_request(df: pd.DataFrame, variables: Dict, small_no_limit: int = 5):
    """
    Take one table request and processes. It creates the table, and if
    cell counts 5 or less in any cell, it redacts the whole table. It keeps
    the title of the table.
    """
    # Make crosstab table
    table = pd.crosstab(df[variables[0]], df[variables[1]])
    table_variables = [variables[0], variables[1]]

    # Check if redaction needed
    redaction_needed = contains_small_numbers(table=table, threshold=small_no_limit)

    # if redacted needed then return redacted table
    if redaction_needed:
        final_table = "REDACTED"
    else:
        final_table = table

    return table_variables, final_table
