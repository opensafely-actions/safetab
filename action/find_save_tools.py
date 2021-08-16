""" this contains useful functions for loading and saving data tables"""
import os
import pathlib
from typing import Dict, Sequence, Union

import pandas as pd

from .errors import ImportActionError

TableConfig = Dict[str, Union[str, Sequence[str]]]


def import_data(file_path: pathlib.Path, table_configs: Dict[str, TableConfig]):
    """
    Imports data and checks that the variables are present

    Will accept input file as csv or dta file (stata).
    """
    if file_path.suffix == ".csv":
        df = pd.read_csv(file_path)
    elif file_path.suffix == ".gz":
        df = pd.read_csv(file_path, compression="gzip")
    elif file_path.suffix == ".dta":
        df = pd.read_stata(file_path)
    elif file_path.suffix == ".feather":
        df = pd.read_feather(file_path)
    else:
        raise ImportActionError("Unsupported filetype attempted to be imported")

    # checks that the variables defined in the json are column names in the
    # csv and raises an error if note
    for table_names, instructions in table_configs.items():
        if not set(instructions["variables"]).issubset(df.columns.values):
            raise ImportActionError

    # returns the csv
    return df


def make_folders(table_config_json, path=None):
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
