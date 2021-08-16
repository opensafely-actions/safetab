from unittest import mock

import pandas as pd
import pytest

from action.errors import ImportActionError
from action.find_save_tools import import_data


class TestImportData:
    @mock.patch("action.find_save_tools.pd.read_csv", return_value=pd.DataFrame())
    def test_import_csv_data(self, mocked):
        import_data({}, "data.csv")
        mocked.assert_called_once_with("data.csv")

    @mock.patch("action.find_save_tools.pd.read_csv", return_value=pd.DataFrame())
    def test_import_csv_gz_data(self, mocked):
        import_data({}, "data.csv.gz")
        mocked.assert_called_once_with("data.csv.gz", compression="gzip")

    @mock.patch("action.find_save_tools.pd.read_stata", return_value=pd.DataFrame())
    def test_import_dta_data(self, mocked):
        import_data({}, "data.dta")
        mocked.assert_called_once_with("data.dta")

    @mock.patch("action.find_save_tools.pd.read_feather", return_value=pd.DataFrame())
    def test_import_feather_data(self, mocked):
        import_data({}, "data.feather")
        mocked.assert_called_once_with("data.feather")

    def test_import_unsupported_file_type(self):
        with pytest.raises(ImportActionError):
            import_data({}, "data.xlsx")

    @mock.patch("action.find_save_tools.pd.read_csv")
    def test_variables_are_columns(self, mocked):
        mocked.return_value = pd.DataFrame(columns=["sex", "has_condition"])
        import_data({"my_table": {"variables": ["sex", "has_condition"]}}, "data.csv")
        # We're testing that an error wasn't raised, so we don't need to assert
        # anything.

    @mock.patch("action.find_save_tools.pd.read_csv")
    def test_variables_are_not_columns(self, mocked):
        mocked.return_value = pd.DataFrame(columns=["sex", "has_condition"])
        with pytest.raises(ImportActionError):
            import_data({"my_table": {"variables": ["sex", "age_band"]}}, "data.csv")
