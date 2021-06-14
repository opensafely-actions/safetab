from safetab.create_tables import output_tables, prettify_tables
from safetab.find_save_tools import import_data
from safetab.redaction_tools import process_table_request

TEST_DATA_CSV = "tests/test_data/test_data.csv"

correct_json_dict = {
    "simple_2_way_tabs": {"tab_type": "2-way", "variables": ["sex", "ageband", "copd"]}
}

full_test_json_dict = {
    "simple_2_way_tabs": {"tab_type": "2-way", "variables": ["sex", "ageband", "copd"]},
    "death_2_way_tabs": {
        "tab_type": "target-2-way",
        "variables": ["sex", "ageband", "copd"],
        "target": "death",
    },
    "grouped_by_sex": {
        "tab_type": "groupby-2-way",
        "variables": ["ageband", "copd", "death"],
        "groupby": "sex",
    },
}


def test_prettify_tables():

    # set up table
    no_redaction_needed_variables = ["sex", "copd"]
    test = import_data(correct_json_dict, data=TEST_DATA_CSV)
    variables, test_table = process_table_request(
        test, variables=no_redaction_needed_variables
    )

    output_str = prettify_tables(table=test_table, variables=variables)
    assert isinstance(output_str, str)
    assert output_str[:11] == "sex vs copd"


def test_output_tables():
    data = TEST_DATA_CSV

    output_tables(
        data_csv=data, table_config=full_test_json_dict, output_dir="test_table_outputs"
    )
