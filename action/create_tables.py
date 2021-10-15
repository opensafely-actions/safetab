import itertools
import pathlib
from typing import Dict, Optional, Sequence, Union

import pandas as pd

from .find_save_tools import import_data, make_output_dirs
from .redaction_tools import make_crosstab


def prettify_tables(table: pd.DataFrame, variables: list) -> str:
    """
    This takes in a table that has been okayed for redaction and produced 2 nice
    version of the table, 1 with row percentages, and 1 with column percentages. These
    are outputted as a markdown file.

    Args:
        table (Dataframe): The table to be converted to markdown, or other format
        variables (list): The list of variables that this table contains

    Returns:
        str (output_str): a string which can be saved as markdown file, which renders
            3 tables.
    """
    table2 = table.copy()

    # make a new table with the values being changed to column percentages
    # rather than values
    percent_col = table2.apply(lambda r: round(((r / r.sum()) * 100), 1), axis=0)

    start_counter = 1
    column_counter = 1
    no_of_columns = len(table2.columns)
    # iterate through all the columns of the table and insert the corresponding
    # column from the table of column percents
    for x in range(0, no_of_columns):
        table2.insert(
            loc=start_counter,
            column=f"Column{column_counter} %",
            value=percent_col.iloc[:, column_counter - 1],
        )
        start_counter = start_counter + 2
        column_counter = column_counter + 1

    table3 = table.copy()
    # make a new table with the values being changed to column percentages rather
    # than values
    percent_row = table3.apply(lambda r: round(((r / r.sum()) * 100), 1), axis=1)

    start_counter = 1
    column_counter = 1
    no_of_columns = len(table3.columns)
    # iterate through all the columns of the table and insert the corresponding
    # column from the table of row percents
    for x in range(0, no_of_columns):
        table3.insert(
            loc=start_counter,
            column=f"Row{column_counter} %",
            value=percent_row.iloc[:, column_counter - 1],
        )
        start_counter = start_counter + 2
        column_counter = column_counter + 1

    table.loc["Total", :] = table.sum(axis=0)
    table.loc[:, "Total"] = table.sum(axis=1)

    output_str = f"{variables[0]} vs {variables[1]}\n\n"
    output_str = output_str + f"ROWS: {variables[0]}, COLUMNS: {variables[1]}\n\n"
    output_str = output_str + table.to_markdown()

    output_str = (
        output_str + f"\n\n{variables[0]} vs {variables[1]} with Column Percentages\n\n"
    )
    output_str = output_str + f"ROWS: {variables[0]}, COLUMNS: {variables[1]}\n\n"
    output_str = output_str + table2.to_markdown()

    output_str = (
        output_str + f"\n\n{variables[0]} vs {variables[1]} with Row Percentages\n\n"
    )
    output_str = output_str + f"ROWS: {variables[0]}, COLUMNS: {variables[1]}\n\n"
    output_str = output_str + table3.to_markdown()

    return output_str


def output_tables(
    data_csv: str,
    table_config: Dict,
    output_dir: Union[None, str] = None,
    limit: int = 5,
) -> None:
    """
    Takes the list of requests for various table configurations, and processes them
    by calling make_crosstab() on each request. Each group of tables are
    put into folders by that name.

    The redacted tables are logged as redacted.
    Tables that do not need redacting are exported to markdown with titles and
    column and row percentages.

    Args:
        data_csv (str): path and name of the csv to be loaded. This is typically
        the CSV generated from the study definition
        table_config (dict): this is the table configuration which is passed
            in as a dict, but is from the project.yaml.
        output_dir (str): path to a directory to save all the tables.
            Default is None. If none provided will save tables in the root where
            function is called.
        limit (int): limit at which should redact small numbers

    """
    df = import_data(pathlib.Path(data_csv), table_config)

    make_output_dirs(table_config, output_dir)

    # For each item in the configuration dictionary, expand the variables as required by
    # the type of table.
    #
    # 2-way:
    # all two element combinations of variables
    #
    # target-2-way:
    # two element combinations of each variable and the target variable
    #
    # groupby-2-way:
    # all two element combinations of variables
    # data split by values of the groupby variable

    two_way_tables: Dict = {}
    targeted_two_way_tables: Dict = {}
    groupby_two_way_tables: Dict = {}

    for name_tables, instructions in table_config.items():
        if instructions["tab_type"] == "2-way":
            two_way_tables[name_tables] = list(
                itertools.combinations(instructions["variables"], 2)
            )

        elif instructions["tab_type"] == "target-2-way":
            targeted_two_way_tables[name_tables] = []
            for var in instructions["variables"]:
                targeted_two_way_tables[name_tables].append(
                    [var, instructions["target"]]
                )

        elif instructions["tab_type"] == "groupby-2-way":
            data = _split_groupby(df, instructions["groupby"])
            permutations = list(itertools.combinations(instructions["variables"], 2))

            groupby_two_way_tables[name_tables] = {
                "grouped_datasets": data,
                "permutations": permutations,
            }

    # Call function for each pair of variables for each named group of 2-way tables
    for group_name, variable_pairs in two_way_tables.items():
        for variable_pair in variable_pairs:
            _output_simple_two_way(
                df, group_name, variable_pair, output_dir=output_dir, limit=limit
            )

    # Call function for each pair of variables for each named group of target-2-way
    # tables
    for group_name, variable_pairs in targeted_two_way_tables.items():
        for variable_pair in variable_pairs:
            _output_simple_two_way(
                df, group_name, variable_pair, output_dir=output_dir, limit=limit
            )

    # run through all the grouped 2 way tables
    for folder_names, table_info in groupby_two_way_tables.items():

        for dataset_name, dataset in table_info["grouped_datasets"].items():
            for combination in table_info["permutations"]:
                _output_simple_two_way(
                    dataset,
                    folder_names,
                    combination,
                    output_dir=output_dir,
                    additional_info=dataset_name,
                    limit=limit,
                )


def _output_simple_two_way(
    df: pd.DataFrame,
    name_tables: str,
    table_instructions: Sequence,
    output_dir: Union[None, str] = None,
    limit: int = 5,
    additional_info: Optional[str] = None,
) -> None:
    """
    This function generated simple 2 way tables given some inputs.

    Args:
        df (Dataframe): the data to be used to generate the table. This
            is data that has already been through the import_data() and is a Dataframe.
        name_tables (str): this is the name of the tables to be generated and is user
            defined in the project.yaml file and imported in as a Python dict.
        table_instructions: this is the information in the project.yaml file
            that is imported in as a Python dict, and contains the instructions
            for the type of table to be generated
        output (str or None): this the sub folder that these tables should be saved in.
        limit (int): limit at which small numbers should be redacted
        additional_info (str or None): this additional argument for labelling
            tables that look similar to each other for example copd vs death,
            in both sexes.
    """
    variable_names, new_table = make_crosstab(df, table_instructions, threshold=limit)
    if additional_info is not None:
        table_name_str = (
            f"{additional_info} - {variable_names[0]} vs {variable_names[1]}"
        )
    else:
        table_name_str = f"{variable_names[0]} vs {variable_names[1]}"

    if type(new_table) == str:
        # create log of table
        table_log = (
            f"{name_tables} - {table_name_str} - Table REDACTED, small numbers\n"
        )
        # save log entry into master file
        with open(f"{output_dir}/table_log.txt", "a") as file_write:
            file_write.write(table_log)
    else:
        # create log of table
        table_log = f"{name_tables} - {table_name_str} - Table created\n"
        # save log entry into master file
        with open(f"{output_dir}/table_log.txt", "a") as file_write:
            file_write.write(table_log)

        # prettify all the tables that were made
        pretty_new_table = prettify_tables(table=new_table, variables=variable_names)

        # save these as markdown files
        with open(f"{output_dir}/{name_tables}/{table_name_str}.md", "w") as file_write:
            file_write.write(pretty_new_table)


def _split_groupby(df: pd.DataFrame, groupby_variable: str) -> Dict[str, pd.DataFrame]:

    # empty dict that collects the grouped dataframes
    df_dict = {}

    # for designated column groupby and save
    for index, group in df.groupby(groupby_variable):
        df_dict.update({f"df_{index}": group})

    # return the dict of dataframes
    return df_dict
