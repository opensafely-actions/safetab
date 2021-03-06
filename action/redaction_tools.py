from typing import Sequence

import pandas as pd


def contains_small_numbers(table: pd.DataFrame, threshold: int = 5) -> bool:
    """Does `table` contain numbers less than or equal to `threshold`?"""
    return table.le(threshold).any(axis=None)


def make_crosstab(table: pd.DataFrame, cols: Sequence, threshold: int = 5):
    """Make a crosstab from `cols` in `table`.

    If the crosstab would contain numbers less than or equal to `threshold`, then return
    "REDACTED" instead.
    """
    crosstab = pd.crosstab(table[cols[0]], table[cols[1]])

    if contains_small_numbers(table=crosstab, threshold=threshold):
        return cols, "REDACTED"

    return cols, crosstab
