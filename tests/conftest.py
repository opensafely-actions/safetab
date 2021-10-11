import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def crosstab():
    index = pd.Index(["M", "F"], name="sex")
    columns = pd.Index([1, 0], name="has_copd")
    data = np.full((len(index), len(columns)), 6)
    return pd.DataFrame(data, index, columns)


@pytest.fixture
def table_configs():
    return {
        "my_two_way": {
            "tab_type": "2-way",
            "variables": ["sex", "age_band"],
        },
        "my_target_two_way": {
            "tab_type": "target-2-way",
            "target": "has_copd",
            "variables": ["sex", "age_band"],
        },
        "my_groupby_two_way": {
            "tab_type": "groupby-2-way",
            "groupby": "age_band",
            "variables": ["sex", "has_copd"],
        },
    }
