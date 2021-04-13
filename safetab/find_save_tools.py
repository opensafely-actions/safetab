''' this contains useful functions for loading and saving data tables'''
import os
import pandas as pd
from pathlib import PurePosixPath

from .errors import ImportActionError


def import_data(variable_json, data="output/input.csv"):
    """
    Imports data and checks that the variables are present
    
    Will accept input file as csv or dta file (stata).
    """
    # load the data into a pandas DataFrame depending on ext
    ext = PurePosixPath(data).suffix
    if ext == ".csv":
        test_df = pd.read_csv(data)
    elif ext == ".gz":
        test_df = pd.read_csv(data, compression="gzip")
    elif ext == ".dta":
        test_df = pd.read_stata(data)
    elif ext == ".feather":
        test_df = pd.read_feather(data)
    else:
        raise ImportActionError("Unsupported filetype attempted to be imported")

    # checks that the variables defined in the json are column names in the
    # csv and raises an error if note
    for name_table, instructions in variable_json.items():
        for var_item in instructions['variables']:
            if var_item not in test_df.columns.values:
                raise ImportActionError

    # returns the csv
    return test_df


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
