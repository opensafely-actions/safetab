import pytest

from safetab.errors import ImportActionError
from safetab.find_save_tools import import_data


TEST_DATA_CSV = "test_data/test_data.csv"

correct_json_dict = {"simple_2_way_tabs":
                           {"tab_type": "2-way",
                            "variables":["sex","ageband","copd","death"]}}

bad_json_dict = {"simple_2_way_tabs":
                           {"tab_type": "2-way",
                            "variables":["sex","test","copd","death"]}}

def test_import_data():
    # Import test data
    test = import_data(correct_json_dict, data=TEST_DATA_CSV)

    # Check expected 20 rows in dataframe of test data
    assert(len(test.index) == 40)

    # Check column names match
    assert(list(test.columns.values) == ['patient_id','sex', "ageband", "copd", "death"])

    # Checks if raises an error if json does not match the csv columns.
    with pytest.raises(ImportActionError):
        test2 = import_data(bad_json_dict, data="test_data/test_data.csv")
