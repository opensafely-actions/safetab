
import argparse
import json

from safetab.create_tables import output_tables


def make_tables(input_files, table_config):
    output_tables(data_csv=input_files[0],
                         table_config=table_config,
                         output_dir="tests/test_table_outputs")


def main():
    # make args parser
    parser = argparse.ArgumentParser(description="Creates tables and redacts small numbers")

    # version
    parser.add_argument("--version", action='version', version="safetab 0.0.1")
    
    # configurations
    parser.add_argument("config", type=str, help="The yaml passed in as a json obj")

    # parse args
    args = parser.parse_args()
    
    kwargs = vars(args)
    yaml_str = kwargs.pop("config")
    
    # TODO: Make sure file exists
    with open(yaml_str) as json_file:
        instructions = json.load(json_file)

    make_tables(input_files=instructions['inputs'], table_config=instructions['config'])
    

if __name__ == "__main__":
    main()
