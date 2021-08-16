import itertools

import pandas as pd
from pandas import testing

from action.redaction_tools import contains_small_numbers, make_crosstab


class TestContainsSmallNumbers:
    def test_contains_small_numbers(self):
        table = pd.DataFrame({"col_1": [5, 6], "col_2": [6, 6]})
        assert contains_small_numbers(table)

    def test_does_not_contain_small_numbers(self):
        table = pd.DataFrame({"col_1": [6, 6], "col_2": [6, 6]})
        assert not contains_small_numbers(table)


class TestMakeCrosstab:
    @staticmethod
    def table_factory(num_repeated_rows):
        return pd.DataFrame(
            list(itertools.product(["F", "M"], [0, 1])) * num_repeated_rows,
            columns=("sex", "has_condition"),
        )

    def test_contains_small_numbers(self):
        table = self.table_factory(5)
        cols = list(table.columns)

        obs_cols, obs_table = make_crosstab(table, cols)
        exp_cols, exp_table = cols, "REDACTED"

        assert obs_cols == exp_cols
        assert obs_table == exp_table

    def test_does_not_contain_small_numbers(self):
        table = self.table_factory(6)
        cols = list(table.columns)

        obs_cols, obs_table = make_crosstab(table, cols)
        exp_cols = cols
        exp_table = pd.DataFrame(
            [[6, 6], [6, 6]],
            index=pd.Index(["F", "M"], name="sex"),
            columns=pd.Index([0, 1], name="has_condition"),
        )

        assert obs_cols == exp_cols
        testing.assert_frame_equal(obs_table, exp_table)
