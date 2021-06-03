import argparse
import json
import os
from pathlib import Path

from safetab.create_tables import output_tables
from version import __version__


class ActionConfig:
    def __init__(self, validator=None):
        self.validator = validator

    def __call__(self, file_or_string):
        path = Path(file_or_string)
        try:
            if path.exists():
                with path.open() as f:
                    config = json.load(f)
            else:
                config = json.loads(file_or_string)
        except json.JSONDecodeError as exc:
            raise argparse.ArgumentTypeError(f"Could not parse {file_or_string}\n{exc}")

        if self.validator:
            try:
                self.validator(config)
            except Exception as exc:
                raise argparse.ArgumentTypeError(f"Invalid action config:\n{exc}")

        return config

    @classmethod
    def add_to_parser(
        cls, parser, help="The configuration for the safetab action", validator=None
    ):
        parser.add_argument(
            "--config",
            required=True,
            help=help,
            type=ActionConfig(validator),
        )

def make_tables(input_files, config):
    """
    :param input_files: The input csvs that the tables are created. These csvs must contain the columns
        names of the table configuration
    :param config: the table configuration as a json object.
    :return: a folder per csv which itself contains directories of each table specified. Each folder for
        the csv contains a table log text file showing redaction, and the subfolders contain the actual tables

        E.g. for input_one.csv and table configurations of 2-way-simple and groupby-by-copd, you end up
            with a structure of:

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
            table_config=config['tables'],
            output_dir=f"{config['output_path']}/{input_filename}_tables",
        )


def main():
    """
    Command line tool for running safe tab. Config takes in an argument of a json string which
        has a pointer for input csvs and table configurations. These arguments are parsed to
        make_tables() function.
    """
    # make args parser
    parser = argparse.ArgumentParser(
        description="Creates tables and redacts small numbers"
    )

    # configurations
    ActionConfig.add_to_parser(parser)

    # version
    parser.add_argument("--version", action="version", version=f"safetab {__version__}")

    # input files
    parser.add_argument(
        "input_files", nargs="*", help="Files that safetab will be run on"
    )

    # parse args
    args = parser.parse_args()

    # pass the data from the json file to the output_tables arguments
    make_tables(input_files=args.input_files, config=args.config)


if __name__ == "__main__":
    main()
