# Safetab

## Summary

Safetab outputs two-way tables of descriptive statistics.

It applies conservative small number suppression;
if a cell is redacted, then the table is also redacted.
Safetab creates a log file that shows what has been redacted.

## Usage

Consider the following extract from a study's *project.yaml*:

```yaml
actions:

  generate_study_population:
    run: cohortextractor:latest generate_cohort
    outputs:
      highly_sensitive:
        cohort: output/input.csv

  generate_safetabs:
    run: safetab:v3.0.1 output/input.csv
    needs: [generate_study_population]
    config:
      output_path: output
      redaction_limit: 5
      tables:
        two_way:
          tab_type: 2-way
          variables:
            - sex
            - age_band
    outputs:
      moderately_sensitive:
        safetab_log: output/input_tables/table_log.txt
        safetab_two_way: output/input_tables/two_way/*.md
```

The `generate_safetabs` action outputs one table: `sex` vs `age_band`.
Notice the `run` and `config` properties.
The `run` property passes a specific input table to a specific version of safetab.
In this case, the specific input table is *output/input.csv* and the specific version of safetab is v3.0.1.
The `config` property passes configuration to safetab; for more information, see *Configuration*.

### Configuration

`output_path`, which defaults to `safetab_tables`.
Save the outputs to the given path.
If the given path does not exist, then it is created.

---

`redaction_limit`, which defaults to `5`.
Cells (and tables) with less than or equal to this number of records are redacted.

---

`tables`

`2-way`: Outputs a two-way table for each pair (combination) of variables.
For example, given the variables `sex` and `age_band`, it will output one table:
* `sex` vs `age_band`

Given the variables `sex`, `age_band`, and `has_copd`, it will output three tables:
* `sex` vs `age_band`
* `sex` vs `has_copd`
* `age_band` vs `has_copd`

`target-2-way`: Outputs a two-way table for each pair (combination) of variables for a target variable, which is given by the `target` property.
For example, given the variables `sex` and `age_band`, and the target variable `has_copd`, it will output two tables:

* `sex` vs `has_copd`
* `age_band` vs `has_copd`

`groupby-2-way`: Outputs a two-way table for each pair (combination) of variables for a group-by variable, which is given by the `groupby` property.
For example, given the variables `sex` and `has_copd`, and the group-by variable `age_band`, it will output one table for each unique value of `age_band`:
* `sex` vs `has_copd` for `16-29`
* `sex` vs `has_copd` for `30-39`
* ...

## Developer docs

Please see [DEVELOPERS.md](DEVELOPERS.md).
