from pathlib import Path

import pytest

from manipulator.file_processor import FileManipulator

TEST_INPUT_DIR = "/test/input/dir"
TEST_OUTPUT_30R_DIR = "/test/output30r/dir"
TEST_OUTPUT_300R_DIR = "/test/output300r/dir"


FIRST_FILE = "2021_04_06_19_25_00_30_3_0_995678_1_12_0.30rec"
SECOND_FILE = "2021_12_06_22_27_05_30_3_0_995577_1_12_0.30rec"
THIRD_FILE = "2000_01_06_19_29_59_30_3_0_995577_1_12_0.30rec"

FIRST_GROUP = "2021_04_06_19_25*"
SECOND_GROUP = "2021_12_06_22_25*"
THIRD_GROUP = "2000_01_06_19_25*"

FIRST_FINAL_FILE = Path("2021_04_06_19_29.59_*.300rec")
SECOND_FINAL_FILE = Path("2021_12_06_22_29.59_*.300rec")
THIRD_FINAL_FILE = Path("2000_01_06_19_29.59_*.300rec")


@pytest.fixture
def file_manipulator():
    return FileManipulator(
        input_dir=TEST_INPUT_DIR,
        output_30r=TEST_OUTPUT_30R_DIR,
        output_300r=TEST_OUTPUT_300R_DIR,
    )


@pytest.fixture
def file_name_list():
    return [FIRST_FILE, SECOND_FILE, THIRD_FILE]


@pytest.fixture
def file_path_list(file_name_list):
    return [Path(file) for file in file_name_list]


@pytest.fixture
def grouped_files():
    return {
        Path(FIRST_GROUP): [f"{FIRST_GROUP}/{FIRST_FILE}"],
        Path(SECOND_GROUP): [f"{SECOND_GROUP}/{SECOND_FILE}"],
        Path(THIRD_GROUP): [f"{THIRD_GROUP}/{THIRD_FILE}"],
    }


@pytest.fixture
def final_files():
    return [FIRST_FINAL_FILE, SECOND_FINAL_FILE, THIRD_FINAL_FILE]
