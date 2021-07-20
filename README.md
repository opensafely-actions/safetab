### Action Summary
This is an action that can be called into the 
`project.yaml`. It requires data in
a support data file  format (`.csv`, `csv.gz`,
`.dta`, `feather`), and outputs a folder of markdown files. 
This action takes in a dataset and a configuration and 
outputs different types of 2 way tables for descriptive
statistics. 

Small numbers suppression is applied. A conservative approach
is adopted where any indiviudal cell that needs to be redacted, 
results in the whole table being redacted. A log file is created
that shows what has been redacted. 

### Using Safetab Action 
The following example blocks should be included 
in the `project.yaml` file. 

##### Example
```yaml 
inputs: 
  input: tests/test_data/input.feather
```

The `--config` should contain
a key called `tables` containing the tables requested. See
[test1_config](tests/test_json_configs/test_json_1.json). The available tables are:

- `2-way` - simple 2-way table. For example, sex by copd. It creates all combinations
  of available variables if given a list. For example if provided with age, sex and copd. 
  It will produce 3 tables - age vs sex, age vs copd, and sex vs copd. 
- `target-2-way` - 2 way tables by one specified variable. For example if 
  target variable is death and the other variables provided are sex and copd, 
  it will produce 2 tables: sex vs death and copd vs death.
- `groupby-2-way` - simple 2 way table that is stratifed by a third variable. If
  variable to group by is 2 age groups (under 50, over 50), and the 
  variables provided are copd and heart disease, it will produce 2 tables: 
  copd vs heart disease for under 50s, and copd vs heart disease for over 50s.  

If you require the safetab markdown files to be saved 
in a particular folder, you can specify this in the `--config` with `output_path`. If 
no output path is provided, the default place is `safetab_tables`. The action 
will make this folder if it does not exist. 

If you want to change the limit at which redaction occurs, specify this in the 
`--config` with `redaction_limit`. The default is 5 or below. 

##### Example 
```yaml
actions: 
  safetab_data:
    run: safetab:latest input.csv
config:
  tables:
    simple_2_way_tabs:
      tab_type: 2-way
      variables:
      - sex
      - ageband
      - copd
    death_2_way_tab:
      tab_type: target-2-way
      variables:
      - sex
      - ageband
      - copd
      target: death
    grouped_by_sex:
      tab_type: groupby-2-way
      variables:
      - ageband
      - copd
      - death
      groupby: sex
  output_path: safetab_outputs
  redaction_limit: 5
```