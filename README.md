# File manipulator

### Description
Python script will be executed on Linux and will do next:
1. Arguments "input_dir", "output_30r", "output_300r"
2. Search files *.rec in input dir
3. Rename all found .rec files to .30rec files in input dir
4. Move all *.30rec files from input dir to 'output_30r' dir
5. Group files in folder 'output_30r' by name YYYY_mm_DD_HH_MM_SS_\*.30rec in 5 mins groups.   
Example group boundaries: 2021_04_06_19_25_00_\*.30rec - 2021_04_06_19_29_59_\*.30rec     
Example files in the group: 
    - ./2021_04_06_19_25_00_30_3_0_995678_1_12_0.30rec, 
    - ./2021_04_06_19_27_05_30_3_0_995577_1_12_0.30rec, 
    - ./2021_04_06_19_28_39_30_2_0_996256_1_12_0.30rec, 
    - ./2021_04_06_19_29_59_30_3_0_995678_1_12_0.30rec
6. Concatinate content of the group files into one file, with name: 2021_04_06_19_29_59_*.300rec and save to 'output_300r' dir
For example: 2021_04_06_19_29_59_30_3_0_995678_1_12_0.300rec
7. Rename file .300rec to .rec in the'output_300r' dir.
8. Cover all functions with unit tests.


#### TODO:
1. Add setup.py
2. Read each file in the separate tread
3. Add docstrings to all public methods


#### Requirements

* [Python](https://www.python.org/) >= 3.8.0


#### Contribution Guide

You can find contribution guide [here](http://www.contribution-guide.org/).

Also you can read a very nice [guide about commit messages](https://m.habr.com/ru/post/416887/).

### How to work with project

1. Lock poetry dependencies:
    - Activate virtual env
    - Change `pyproject.toml` file
    - Generate `poetry.lock` file: `poetry lock --no-update`
    - Install dependencies: `poetry install`
   
2. Run tests:
    - Run application tests using `make tests`
    - Check application test coverage using `make tests-coverage`

3. Linters:
    - `make lint` - run all linters checks:
        - `make format-check` - to check code formatting (black and isort)
        - `make flake8` - to check code formatting (flake8)
        - `make mypy-check` - to check code types using mypy
    - `make format` - to format code using black and isort

4. To check project source code metrics you can use [Radon](https://pypi.org/project/radon/): `make radon-check`

5. To check your tests quality you can use [mutmut](https://pypi.org/project/mutmut/): 
    - Enter `make mutmut-check`
    - You will get a report `mutmut-report.xml` 


### Environment variables

| name | type | required | default |
|------|------|----------|---------|
| FILE_MANIPULATOR_LOGGER_LEVEL | int | false | 20 (logging.INFO) |
| FILE_MANIPULATOR_INPUT_FILE_EXT | str | false | ".rec" |
| FILE_MANIPULATOR_OUTPUT_30R_FILE_EXT | str | false  | ".30rec" |
| FILE_MANIPULATOR_OUTPUT_300R_FILE_EXT | str | false  | ".300rec" |
