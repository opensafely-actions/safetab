''' this contains useful functions for loading and saving data tables'''
import os
import pandas as pd

from .errors import ImportActionError


def import_data(variable_json, data="output/input.csv"):
    """
    Imports data and checks that the variables are present
    """
    # load the data into a pandas DataFame
    test_df = pd.read_csv(data)

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
            os.mkdir(folder_name)
    else:
        for folder_name, table_dets in folder_names.items():
            full_path = os.path.join(path, folder_name)
            os.mkdir(full_path)
