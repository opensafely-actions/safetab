import pandas as pd
import json

from .errors import ImportActionError

def import_data(variable_json, data="output/input.csv"):
    """
    Imports data and checks that the variables are present
    """
    # load the data into a pandas DataFame
    test_df = pd.read_csv(data)

    # checks that the variables defined in the json are column names in the
    # csv and raises an error if note
    for var_item in variable_json['keyword_args']['2_way_tabs']["variables"]:
        if var_item not in test_df.columns.values:
            raise ImportActionError

    # returns the csv
    return test_df

def check_for_low_numbers(table, small_no_limit=5):
    """
    Takes in a dataframe such as 2x2 contigency table and checks each value
    to see if any cell values are small numbers.

    Args:
        table (Dataframe): table to be redacted
        small_no_limit (int): the number at which values should be redacted. Defaults to
            5.

    returns
        boolean (redaction_needed): True if needs redaction, False if not.
    """
    # Convert table into list for iteration
    all_values = table.values.tolist()

    # set condition_met to False to start with. This changes if limit breached
    condition_met = False

    # check if retraction needs to occur based on small_no_limit. Default is 5.
    for column in all_values:
        for item in column:
            if type(item) == str:
                pass
            elif item <= small_no_limit:
                condition_met = True

    return condition_met


def process_table_request(df, variables, percent_direction=False, groupby=False, small_no_limit=5):
    """
    Take one table request and processes. It creates the table, and if
    cell counts 5 or less in any cell, it redacts the whole table. It keeps
    the title of the table.
    """
    # Make crosstab table
    table = pd.crosstab(df[variables[0]], df[variables[1]], margins=True, margins_name="Total")



    return condition_met

def output_tables(output_dir):
    """
    Takes the list of requests for various table configurations, and processes them
    by calling process_table_request() on each request.
    """

    # Load data by calling import_data() function

    pass


