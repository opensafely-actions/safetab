
import argparse

from safetab.create_tables import output_tables

full_test_json_dict = {"simple_2_way_tabs":
                           {"tab_type": "2-way",
                            "variables":["sex","ageband","copd"]},
                       "death_2_way_tabs":
                           {"tab_type": "target-2-way",
                            "variables": ["sex", "ageband", "copd"],
                            "target": "death"},
                       "grouped_by_sex":
                            {"tab_type": "groupby-2-way",
                             "variables":["ageband","copd","death"],
                             "groupby": "sex"}
                       }

def make_tables(yaml_str):
    print(yaml_str)
    output_tables(data_csv="tests/test_data/test_data.csv",
                         table_config=full_test_json_dict,
                         output_dir="tests/test_table_outputs")


def main():
    # make args parser
    parser = argparse.ArgumentParser(description="Creates tables and redacts small numbers")

    # make subparser
    subparsers = parser.add_subparsers(
        title="available commands", description="", metavar="COMMAND")
    
    # version
    parser.add_argument("--version", action='version', version="safetab 0.0.1")
    
    # make safetab action
    parser_make_tabs = subparsers.add_parser(
        "safetab",
        help="add some help here"
    )
    parser_make_tabs.add_argument("--config", type=str, help="The yaml str passed in")
    parser_make_tabs.set_defaults(function=make_tables)

    # parse args
    args = parser.parse_args()
    
    kwargs = vars(args)
    function = kwargs.pop("function")
    yaml_str = kwargs.pop("config")
    success = function(yaml_str)

if __name__ == "__main__":
    main()
