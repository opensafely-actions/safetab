
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

    # version
    parser.add_argument("--version", action='version', version="safetab 0.0.1")
    
    parser.add_argument("--config", type=str, help="The yaml str passed in")

    # parse args
    args = parser.parse_args()
    
    kwargs = vars(args)
    yaml_str = kwargs.pop("config")

    # check the files exists
    make_tables(yaml_str)
    

if __name__ == "__main__":
    main()
