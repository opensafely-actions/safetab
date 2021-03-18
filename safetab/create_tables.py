import pandas as pd
import json

from .errors import ImportActionError

def import_data(variable_json, data="output/input.csv"):
    """
    Imports data and checks that the variables are present
    """
    # load the data into a pandas DataFame
    test_df = pd.read_csv(data)

    for var_item in variable_json['keyword_args']['2_way_tabs']["variables"]:
        print(var_item)
#         if var_item in test_df.columns:
#             pass
#         else:
#             raise ImportActionError

    return test_df

def process_table_request(variables, percent_direction, groupby=False):
    """
    Take one table request and processes. It creates the table, and if
    cell counts 5 or less in any cell, it redacts the whole table. It keeps
    the title of the table.
    """
    pass

def output_tables(output_dir):
    """
    Takes the list of requests for various table configurations, and processes them
    by calling process_table_request() on each request.
    """
    pass


