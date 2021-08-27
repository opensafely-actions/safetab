import argparse
import json
import os
from pathlib import Path
from typing import Dict

from action import __version__
from action.create_tables import output_tables
from action.utils import load_config


def convert_config(file_or_string: str) -> Dict:
    """Deserializes the JSON given by a string or a path to a file.

    Args:
        file_or_string: Either a JSON string or a path to a JSON file.

    Raises:
        ArgumentTypeError: There was a problem deserializing the JSON.
    """
    path = Path(file_or_string)

    try:
        path_exists = path.exists()
    except OSError as e:
        if e.errno == 63:  # File name too long
            # The name component of the path is too long for the file system. It's
            # likely that `file_or_string` is a string, so we won't re-raise the error.
            path_exists = False
        else:
            raise e

    try:
        if path_exists:
            with path.open() as f:
                config = json.load(f)
        else:
            config = json.loads(file_or_string)
    except json.JSONDecodeError as exc:
        raise argparse.ArgumentTypeError(f"Could not parse {file_or_string}\n{exc}")

    return config


def run_action(input_files, config):
    """
    :param input_files: The input csvs that the tables are created. These csvs
        must contain the columns names of the table configuration
    :param config: the table configuration as a json object.
    :return: a folder per csv which itself contains directories of each
        table specified. Each folder for the csv contains a table log
        text file showing redaction, and the subfolders contain the
        actual tables

        E.g. for input_one.csv and table configurations of 2-way-simple
            and groupby-by-copd, you end up with a structure of:

             - input_one_tables/
                - 2-way-simple/
                - group-by-copd
                - table-log.txt
             - input_two_tables/
                - 2-way-simple/
                - group-by-copd
                - table-log.txt
    """
    for input_file in input_files:
        input_filename_with_ext = os.path.basename(input_file)
        input_filename = os.path.splitext(input_filename_with_ext)[0]
        output_tables(
            data_csv=input_file,
            table_config=config["tables"],
            output_dir=f"{config['output_path']}/{input_filename}_tables",
            limit=config["redaction_limit"],
        )


def main():
    """
    Command line tool for running safe tab. Config takes in an argument
        of a json string which has a pointer for input csvs and
        table configurations. These arguments are parsed to
        make_tables() function.
    """
    # make args parser
    parser = argparse.ArgumentParser(
        description="Creates tables and redacts small numbers"
    )

    # configurations
    parser.add_argument(
        "--config",
        help="Configuration as either a JSON str or a path to a JSON file",
    )

    # version
    parser.add_argument("--version", action="version", version=f"action {__version__}")

    # input files
    parser.add_argument(
        "input_files", nargs="*", help="Files that action will be run on"
    )

    # parse args
    args = parser.parse_args()

    # convert config path to config dict
    config_dict = convert_config(args.config)
    processed_config = load_config(config_dict)

    # pass the data from the json file to the output_tables arguments
    run_action(input_files=args.input_files, config=processed_config)


if __name__ == "__main__":
    main()
