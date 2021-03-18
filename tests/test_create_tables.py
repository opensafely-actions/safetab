import pandas as pd
import pytest
from safetab.errors import ImportActionError

from safetab.create_tables import import_data, process_table_request, check_for_low_numbers

correct_json_dict = {"keyword_args":
                {"2_way_tabs":
                    {"variables":["sex","ageband","copd","death"],
                    "percentages":"row"}}}

bad_json_dict = {"keyword_args":
                {"2_way_tabs":
                    {"variables":["sex","test","copd","death"],
                    "percentages":"row"}}}

def test_import_data():
    # Import test data
    test = import_data(correct_json_dict, data="test_data/test_data.csv")

    # Check expected 20 rows in dataframe of test data
    assert(len(test.index) == 20)

    # Check column names match
    assert(list(test.columns.values) == ['patient_id','sex', "ageband", "copd", "death"])

    # Checks if raises an error if json does not match the csv columns.
    with pytest.raises(ImportActionError):
        test2 = import_data(bad_json_dict, data="test_data/test_data.csv")


def test_check_for_low_numbers():
    no_redact_data = {'test_col_1': [10, 20], 'test_col_2': [20, 40]}
    no_redact_df = pd.DataFrame(data=no_redact_data)

    # use check_for_low_numbers() on a dataframe that does not require redaction
    result = check_for_low_numbers(table=no_redact_df, small_no_limit=5)
    assert(result == False)

    need_redact_data = {'test_col_1': [1, 10], 'test_col_2': [20, 40]}
    need_redact_df = pd.DataFrame(data=need_redact_data)

    # use check_for_low_numbers() on a dataframe that does require redaction
    result2 = check_for_low_numbers(table=need_redact_df, small_no_limit=5)
    assert(result2 == True)


def test_process_table_request():
    test_variables = ['sex', 'death']
    percentage_direction = "row"

    # Import test data
    test = import_data(correct_json_dict, data="test_data/test_data.csv")
    test_table = process_table_request(test, variables=['sex', 'copd'])

    asser





