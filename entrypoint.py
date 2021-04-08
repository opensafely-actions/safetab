
import argparse
import json
import os

from safetab.create_tables import output_tables


def make_tables(input_files, table_config):
    
    for input_file in input_files:
        output_file_name = os.path.splitext(input_file)[0]
        output_tables(data_csv=input_file,
                      table_config=table_config,
                      output_dir=f"{output_file_name}_tables")


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
    json_path = kwargs.pop("config")
    
    # TODO: Make sure file exists
    with open(json_path) as json_file:
        instructions = json.load(json_file)
        
    # pass the data from the json file to the output_tables arguments
    make_tables(input_files=instructions['inputs'], table_config=instructions['config'])
    

if __name__ == "__main__":
    main()
