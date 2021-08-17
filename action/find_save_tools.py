""" this contains useful functions for loading and saving data tables"""
import itertools
import os
import pathlib
from typing import Dict, Iterable, Optional, Sequence, Union

import pandas as pd

from .errors import ImportActionError

TableConfig = Dict[str, Union[str, Sequence[str]]]


def import_data(file_path: pathlib.Path, table_configs: Dict[str, TableConfig]):
    """Imports data, checking that the required variables are present."""
    if file_path.suffix == ".csv":
        table = pd.read_csv(file_path)
    elif file_path.suffix == ".gz":
        table = pd.read_csv(file_path, compression="gzip")
    elif file_path.suffix == ".dta":
        table = pd.read_stata(file_path)
    elif file_path.suffix == ".feather":
        table = pd.read_feather(file_path)
    else:
        raise ImportActionError(f"'{file_path.suffix}' is not a supported file-type")

    variables = set(itertools.chain(*[x["variables"] for x in table_configs.values()]))
    if not variables <= set(table.columns):
        raise ImportActionError("Missing required variables")

    return table


def make_output_dirs(table_names: Iterable[str], base_dir: Optional[str] = None):
    """Makes output directories for tables and log files.

    Args:
        table_names: The names of the tables are the names of the output directories.
        base_dir: The base directory, beneath which the output directories are made.
            If `None`, then the base directory is the current directory.
    """
    for table_name in table_names:
        if base_dir is None:
            dir_out = table_name
        else:
            dir_out = os.path.join(base_dir, table_name)
        os.makedirs(dir_out, exist_ok=True)
