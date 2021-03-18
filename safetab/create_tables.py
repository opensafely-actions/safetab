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


def process_table_request(df, variables, small_no_limit=5):
    """
    Take one table request and processes. It creates the table, and if
    cell counts 5 or less in any cell, it redacts the whole table. It keeps
    the title of the table.
    """
    # Make crosstab table
    table = pd.crosstab(df[variables[0]], df[variables[1]])

    # Check if redaction needed
    redaction_needed = check_for_low_numbers(table=table, small_no_limit=small_no_limit)

    # if redacted needed then return redacted table
    if redaction_needed:
        final_table = "REDACTED"
    else:
        final_table = table

    return final_table


def prettify_tables(table, variables):
    """
    This takes in a table that has been okayed for redaction and produced 2 nice
    version of the table, 1 with row percetnages, and 1 with column percentages. These
    are outputted as a markdown file.
    """
    table2 = table.copy()
    percent_col = table2.apply(lambda r: round(((r / r.sum()) * 100), 1), axis=0)
    table2.insert(loc=1, column="Column1 %", value=percent_col[0])
    table2.insert(loc=3, column="Column2 %", value=percent_col[1])

    table3 = table.copy()
    percent_row = table3.apply(lambda r: round(((r / r.sum()) * 100), 1), axis=1)
    table3.insert(loc=1, column="Row1 %", value=percent_row[0])
    table3.insert(loc=3, column="Row2 %", value=percent_row[1])

    table.loc['Total', :] = table.sum(axis=0)
    table.loc[:, 'Total'] = table.sum(axis=1)

    output_str = f"{variables[0]} vs {variables[1]}\n"
    output_str = output_str + f"ROWS: {variables[0]}, COLUMNS: {variables[1]}\n"
    output_str = output_str + table.to_markdown()

    output_str = output_str + f"\n\n{variables[0]} vs {variables[1]} with Column Percentages\n"
    output_str = output_str + f"ROWS: {variables[0]}, COLUMNS: {variables[1]}\n"
    output_str = output_str + table2.to_markdown()

    output_str = output_str + f"\n\n{variables[0]} vs {variables[1]} with Row Percentages\n"
    output_str = output_str + f"ROWS: {variables[0]}, COLUMNS: {variables[1]}\n"
    output_str = output_str + table3.to_markdown()

    return output_str

def output_tables(output_dir):
    """
    Takes the list of requests for various table configurations, and processes them
    by calling process_table_request() on each request.
    """
    
    # Load data by calling import_data() function

    pass


