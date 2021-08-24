import pathlib
from unittest import mock

import pandas as pd
import pytest

from action.errors import ImportActionError
from action.find_save_tools import import_data, make_output_dirs


class TestImportData:
    @mock.patch("action.find_save_tools.pd.read_csv", return_value=pd.DataFrame())
    def test_import_csv_data(self, mocked):
        import_data(pathlib.Path("data.csv"), {})
        mocked.assert_called_once_with(pathlib.Path("data.csv"))

    @mock.patch("action.find_save_tools.pd.read_csv", return_value=pd.DataFrame())
    def test_import_csv_gz_data(self, mocked):
        import_data(pathlib.Path("data.csv.gz"), {})
        mocked.assert_called_once_with(pathlib.Path("data.csv.gz"), compression="gzip")

    @mock.patch("action.find_save_tools.pd.read_stata", return_value=pd.DataFrame())
    def test_import_dta_data(self, mocked):
        import_data(pathlib.Path("data.dta"), {})
        mocked.assert_called_once_with(pathlib.Path("data.dta"))

    @mock.patch("action.find_save_tools.pd.read_feather", return_value=pd.DataFrame())
    def test_import_feather_data(self, mocked):
        import_data(pathlib.Path("data.feather"), {})
        mocked.assert_called_once_with(pathlib.Path("data.feather"))

    def test_import_unsupported_file_type(self):
        with pytest.raises(ImportActionError):
            import_data(pathlib.Path("data.xlsx"), {})

    @mock.patch("action.find_save_tools.pd.read_csv")
    def test_variables_are_columns(self, mocked, table_configs):
        mocked.return_value = pd.DataFrame(columns=["sex", "age_band", "has_copd"])
        import_data(pathlib.Path("data.csv"), table_configs)
        # We're testing that an error wasn't raised, so we don't need to assert
        # anything.

    @mock.patch("action.find_save_tools.pd.read_csv")
    def test_variables_are_not_columns(self, mocked, table_configs):
        mocked.return_value = pd.DataFrame(columns=["sex", "age_band"])  # no has_copd
        with pytest.raises(ImportActionError):
            import_data(pathlib.Path("data.csv"), table_configs)


@mock.patch("os.makedirs")
class TestMakeOutputDirs:
    def test_with_base_dir(self, mocked, table_configs):
        make_output_dirs(table_configs, "my_base_dir")
        mocked.assert_has_calls(
            [
                mock.call("my_base_dir/my_two_way", exist_ok=True),
                mock.call("my_base_dir/my_target_two_way", exist_ok=True),
                mock.call("my_base_dir/my_groupby_two_way", exist_ok=True),
            ]
        )

    def test_without_base_dir(self, mocked, table_configs):
        make_output_dirs(table_configs)
        mocked.assert_has_calls(
            [
                mock.call("my_two_way", exist_ok=True),
                mock.call("my_target_two_way", exist_ok=True),
                mock.call("my_groupby_two_way", exist_ok=True),
            ]
        )
