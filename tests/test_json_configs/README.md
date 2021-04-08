`test_json_1.json`

This is the serialised version of the yaml. The original
yaml looks like this:

```yaml
inputs: [file1]
config:
  simple_2_way_tabs:
    tab_type: 2-way
    variables: [sex, ageband, copd]
  death_2_way_tab:
    tab_type: target-2-way
    variables: [sex, ageband, copd]
    target: death
  grouped_by_sex:
    tab_type: groupby-2-way
    variables: [ageband, copd, death]
    groupby: sex

```