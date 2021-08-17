""" this contains useful functions for loading and saving data tables"""
import itertools
import os
import pathlib
from typing import Dict, Sequence, Union

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


def make_output_dirs(table_config_json, path=None):
    """
    Makes the output folders for the markdown files to land into based on the json
    provided
    """
    folder_names = table_config_json
    if path is None:
        for folder_name, table_dets in folder_names.items():
            os.makedirs(folder_name, exist_ok=True)
    else:
        os.makedirs(path, exist_ok=True)
        for folder_name, table_dets in folder_names.items():
            full_path = os.path.join(path, folder_name)
            os.makedirs(full_path, exist_ok=True)
