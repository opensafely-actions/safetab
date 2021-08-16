import pandas as pd

from action.find_save_tools import import_data
from action.redaction_tools import contains_small_numbers, process_table_request

TEST_DATA_CSV = "tests/test_data/test_data.csv"

correct_json_dict = {
    "simple_2_way_tabs": {
        "tab_type": "2-way",
        "variables": ["sex", "ageband", "copd", "death"],
    }
}


class TestContainsSmallNumbers:
    def test_contains_small_numbers(self):
        table = pd.DataFrame({"col_1": [5, 6], "col_2": [6, 6]})
        assert contains_small_numbers(table)

    def test_does_not_contain_small_numbers(self):
        table = pd.DataFrame({"col_1": [6, 6], "col_2": [6, 6]})
        assert not contains_small_numbers(table)


def test_process_table_request():
    no_redaction_needed_variables = ["sex", "copd"]
    redaction_needed_variables = ["ageband", "sex"]

    # Import test data
    test = import_data(correct_json_dict, data=TEST_DATA_CSV)

    # pick 2 variables which have sufficient numbers to require no redaction
    variables, test_table = process_table_request(
        test, variables=no_redaction_needed_variables
    )

    # check values are correct
    # first row should be female sex. There are 16 women with copd, 16 without
    assert test_table.iloc[0][0] == 16

    # pick 2 variables which have sufficient numbers to require no redaction
    variables2, test_table_2 = process_table_request(
        test, variables=redaction_needed_variables
    )

    # assert redacted
    # print("TABLE 2: ", test_table_2)
    assert test_table_2 == "REDACTED"
