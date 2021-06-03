# Safetab Action
Action that can be run by project yaml which gives descriptive 2-way tables 
of specified variables, and redacts if 5 or less in any cell of the subsequent
table. 

### Action Arguments
The action has one required argument called input_files. This is a file or list 
of files that you wish to run the safetab action on. 

##### Config structure
There is one optional argument `--config`. The config can be a string or a json file.

If the input file does not have typing inbuilt, the `--config` should contain
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
 
### Running this action
It can be run in two ways:

##### Run locally with Python
```bash
python3 entrypoint.py [inputfile] --config [config_json_file]

# for example to run test input file and config
python entrypoint.py tests/test_data/test_data.csv --config tests/test_json_configs/test_json_1.json
```

##### Running as CLI
You can pip install this package and use as a command line tool. 
```bash
safetab [inputfile or list of files] --config [config_json_file or json_str]

# for example to run an input file and config
safetab data/input.csv --config test_actions_jsons/test1_config.json

# to run list of input files and same config for each file
safetab data/input.csv data/second_input.csv --config test_actions_jsons/test_json_1.json
```

### Project yaml
This action can be invoked from the `project.yaml`. This is passed into json. 

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

## Local Development

For local (non-Docker) development, first install [pyenv][] and execute:

```sh
pyenv install $(pyenv local)
```

Then, execute:

```sh
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r dev_requirements.txt
```

## QA
Run `make` to access Makefile commands. Black, flake8 and mypy are available 
and have a standard setup. 

## Tests

If you have a local development environment,
then the following command will write [pytest][]'s output to the terminal:

```sh
python -m pytest
```

You can also pass test modules, classes, methods, and functions to pytest:

```sh
python -m pytest tests/test_processing.py::test_load_study_cohort
```

[pyenv]: https://github.com/pyenv/pyenv
[pytest]: https://docs.pytest.org/en/stable/
