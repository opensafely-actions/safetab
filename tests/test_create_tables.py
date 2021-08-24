from action.create_tables import prettify_tables


def test_prettify_tables(crosstab):
    output_str = prettify_tables(
        table=crosstab,
        variables=[crosstab.index.name, crosstab.columns.name],
    )
    assert isinstance(output_str, str)
    assert output_str[:11] == "sex vs copd"
