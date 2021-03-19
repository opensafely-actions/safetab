import itertools

from .redaction_tools import process_table_request
from .find_save_tools import import_data, make_folders

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

    output_str = f"{variables[0]} vs {variables[1]}\n\n"
    output_str = output_str + f"ROWS: {variables[0]}, COLUMNS: {variables[1]}\n\n"
    output_str = output_str + table.to_markdown()

    output_str = output_str + f"\n\n{variables[0]} vs {variables[1]} with Column Percentages\n\n"
    output_str = output_str + f"ROWS: {variables[0]}, COLUMNS: {variables[1]}\n\n"
    output_str = output_str + table2.to_markdown()

    output_str = output_str + f"\n\n{variables[0]} vs {variables[1]} with Row Percentages\n\n"
    output_str = output_str + f"ROWS: {variables[0]}, COLUMNS: {variables[1]}\n\n"
    output_str = output_str + table3.to_markdown()

    return output_str

def output_tables(data_csv, table_config, output_dir=None):
    """
    Takes the list of requests for various table configurations, and processes them
    by calling process_table_request() on each request. Each group of tables are
    put into folders by that name.

    The redacted tables are logged as redacted.
    Tables that do not need redacting are exported to markdown with titles and
    column and row percentages.
    """
    # Load data by calling import_data() function
    df = import_data(data=data_csv, variable_json=table_config)

    # Make folder for tables
    make_folders(table_config_json=table_config, path=output_dir)

    # Sort the json into options
    two_way_tables = {}
    for name_tables, instructions in table_config.items():
        if instructions['tab_type'] == "2-way":
            two_way_tables[name_tables] = list(itertools.combinations(instructions['variables'], 2))

    # run through all two way tables
    for name_tables, table_info in two_way_tables.items():

        # run through create each table and log if table made
        for table_instructions in two_way_tables[name_tables]:
            output_simple_two_way(df, name_tables, table_instructions, output_dir=output_dir)


def output_simple_two_way(df, name_tables, table_instructions, output_dir=None):
    variable_names, new_table = process_table_request(df, table_instructions)
    table_name_str = f"{variable_names[0]} vs {variable_names[1]}"

    if type(new_table) == str:
        # create log of table
        table_log = f"{table_name_str} - Table REDACTED, small numbers\n"
        # save log entry into master file
        with open(f"{output_dir}/table_log.txt", "a") as file_write:
            file_write.write(table_log)
    else:
        # create log of table
        table_log = f"{table_name_str} - Table created\n"
        # save log entry into master file
        with open(f"{output_dir}/table_log.txt", "a") as file_write:
            file_write.write(table_log)

        # prettify all the tables that were made
        pretty_new_table = prettify_tables(table=new_table, variables=variable_names)

        # save these as markdown files
        with open(f"{output_dir}/{name_tables}/{table_name_str}.md", "w") as file_write:
            file_write.write(pretty_new_table)

