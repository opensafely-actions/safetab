from unittest import mock

import pytest

from action.create_tables import output_tables, prettify_tables


def test_prettify_tables(crosstab):
    output_str = prettify_tables(
        table=crosstab,
        variables=[crosstab.index.name, crosstab.columns.name],
    )
    assert isinstance(output_str, str)
    assert output_str[:11] == "sex vs copd"


class TestOutputTables:
    @pytest.mark.xfail(reason="#20")
    @mock.patch("action.create_tables.import_data")
    @mock.patch("action.create_tables.make_crosstab")
    @mock.patch("action.create_tables.make_output_dirs")
    def test_output_file_paths(
        self,
        mocked_import_data,
        mocked_make_crosstab,
        mocked_make_output_dirs,
        crosstab,
        table_configs,
    ):
        # The `output_tables` function mixes reading, wrangling, and writing data. This
        # test begins to unpick it, by mocking this functionality. The intention is to:
        # 1. refactor, by testing this functionality
        # 2. identify bugs, by writing tests that we expect to fail

        mocked_make_crosstab.return_value = [
            crosstab.index.name,
            crosstab.columns.name,
        ], crosstab

        with mock.patch("action.create_tables.open", mock.mock_open()) as mock_open:
            output_tables("output/input.csv", table_configs, "output")

        # What do the mocked calls represent?
        # 0. Open the file
        # 1. Enter the context manager
        # 2. Write to the file
        # 3. Exit the context manager
        open_calls = mock_open.mock_calls[::4]
        assert len(open_calls) == 6

        assert open_calls[0].args[0] == "output/table_log.txt"
        assert open_calls[1].args[0] == "output/my_two_way/sex vs copd.md"

        assert open_calls[2].args[0] == "output/table_log.txt"
        assert open_calls[3].args[0] == "output/my_target_two_way/sex vs copd.md"

        assert open_calls[4].args[0] == "output/table_log.txt"
        assert open_calls[5].args[0] == "output/my_groupby_two_way/sex vs copd.md"
