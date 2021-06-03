import pandas as pd
from safetab.redaction_tools import check_for_low_numbers, process_table_request
from safetab.find_save_tools import import_data


TEST_DATA_CSV = "tests/test_data/test_data.csv"

correct_json_dict = {
    "simple_2_way_tabs": {
        "tab_type": "2-way",
        "variables": ["sex", "ageband", "copd", "death"],
    }
}


def test_check_for_low_numbers():
    no_redact_data = {"test_col_1": [10, 20], "test_col_2": [20, 40]}
    no_redact_df = pd.DataFrame(data=no_redact_data)

    # use check_for_low_numbers() on a dataframe that does not require redaction
    result = check_for_low_numbers(table=no_redact_df, small_no_limit=5)
    assert result is False

    need_redact_data = {"test_col_1": [1, 10], "test_col_2": [20, 40]}
    need_redact_df = pd.DataFrame(data=need_redact_data)

    # use check_for_low_numbers() on a dataframe that does require redaction
    result2 = check_for_low_numbers(table=need_redact_df, small_no_limit=5)
    assert result2 is True


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
