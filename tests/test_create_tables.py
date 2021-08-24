from action.create_tables import output_tables, prettify_tables

TEST_DATA_CSV = "tests/test_data/test_data.csv"

full_test_json_dict = {
    "simple_2_way_tabs": {"tab_type": "2-way", "variables": ["sex", "ageband", "copd"]},
    "death_2_way_tabs": {
        "tab_type": "target-2-way",
        "variables": ["sex", "ageband", "copd"],
        "target": "death",
    },
    "grouped_by_sex": {
        "tab_type": "groupby-2-way",
        "variables": ["ageband", "copd", "death"],
        "groupby": "sex",
    },
}


def test_prettify_tables(crosstab):
    output_str = prettify_tables(
        table=crosstab,
        variables=[crosstab.index.name, crosstab.columns.name],
    )
    assert isinstance(output_str, str)
    assert output_str[:11] == "sex vs copd"


def test_output_tables():
    data = TEST_DATA_CSV

    output_tables(
        data_csv=data, table_config=full_test_json_dict, output_dir="test_table_outputs"
    )
