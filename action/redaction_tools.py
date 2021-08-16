""" Tools for redaction """
from typing import Dict

import pandas as pd


def check_for_low_numbers(table: pd.DataFrame, small_no_limit: int = 5) -> bool:
    """Does `table` contain numbers less than or equal to `small_no_limit`?"""
    # Convert table into list for iteration
    all_values = table.values.tolist()

    # set condition_met to False to start with. This changes if limit breached
    condition_met = False

    # check if retraction needs to occur based on small_no_limit. Default is 5.
    for column in all_values:
        for item in column:
            if isinstance(item, str):
                pass
            elif item <= small_no_limit:
                condition_met = True

    return condition_met


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
    redaction_needed = check_for_low_numbers(table=table, small_no_limit=small_no_limit)

    # if redacted needed then return redacted table
    if redaction_needed:
        final_table = "REDACTED"
    else:
        final_table = table

    return table_variables, final_table
