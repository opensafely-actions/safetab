import json
# import pandas as pd
from safetab.create_tables import import_data

test_dict = {"keyword_args":
                {"2_way_tabs":
                    {"variables":["sex","age","copd","death"],
                    "percentages":"row"}}}


def test_import_data():
    # Import test data
    test = import_data(test_dict, data="test_data/test_data.csv")

    # Check expected 20 rows in dataframe of test data
    assert(len(test.index) == 20)

    # Check column names match

