from pathlib import Path

import mock
import pytest

from manipulator.file_processor import FileManipulator
from tests.conftest import (
    FIRST_FILE,
    FIRST_FINAL_FILE,
    FIRST_GROUP,
    SECOND_FILE,
    SECOND_FINAL_FILE,
    SECOND_GROUP,
    THIRD_FILE,
    THIRD_FINAL_FILE,
    THIRD_GROUP,
)


@mock.patch.object(FileManipulator, "_change_extension")
def test_change_files_extension(
    mock_change_extension, file_manipulator, file_name_list
):
    file_manipulator.change_files_extension(file_name_list)
    assert mock_change_extension.called is True


@mock.patch.object(FileManipulator, "_move_file")
@mock.patch.object(FileManipulator, "_delete_files")
def test_move_to_dir(
    mock_move_file, mock_delete_files, file_manipulator, file_path_list
):
    file_manipulator.move_to_dir(file_path_list)
    assert mock_move_file.called is True
    assert mock_delete_files.called is True


@pytest.mark.parametrize(
    "input_string, output_string",
    [
        (
            FIRST_FILE,
            ("2021_04_06_19_", "19_", "25"),
        ),
        (
            SECOND_FILE,
            ("2021_12_06_22_", "22_", "27"),
        ),
        (
            THIRD_FILE,
            ("2000_01_06_19_", "19_", "29"),
        ),
    ],
)
def test__groups(file_manipulator, input_string, output_string):
    assert file_manipulator._groups(input_string) == output_string


@pytest.mark.parametrize(
    "input_file, first, minute_group",
    [
        (
            Path(FIRST_FILE),
            "2021_04_06_19_",
            25,
        ),
        (
            Path(SECOND_FILE),
            "2021_12_06_22_",
            25,
        ),
        (
            Path(THIRD_FILE),
            "2000_01_06_19_",
            25,
        ),
    ],
)
def test__group_name_parts(file_manipulator, input_file, first, minute_group):
    assert file_manipulator._group_name_parts(input_file) == (first, minute_group)


@mock.patch("shutil.copy")
@mock.patch.object(Path, "mkdir")
@mock.patch.object(FileManipulator, "_delete_files")
def test_group_files(
    copy_mock,
    mkdir_mock,
    mock_delete_files,
    file_manipulator,
    file_path_list,
    grouped_files,
):
    actual_result = dict(file_manipulator.group_files(file_path_list))
    assert actual_result == grouped_files

    assert copy_mock.called is True
    assert mkdir_mock.called is True
    assert mock_delete_files.called is True


@pytest.mark.parametrize(
    "group, result",
    [
        (
            FIRST_GROUP,
            FIRST_FINAL_FILE,
        ),
        (
            SECOND_GROUP,
            SECOND_FINAL_FILE,
        ),
        (
            THIRD_GROUP,
            THIRD_FINAL_FILE,
        ),
    ],
)
def test__group_final_filepath(group, result, file_manipulator):
    assert file_manipulator._group_final_filepath(group) == result


@mock.patch.object(FileManipulator, "_group_content")
@mock.patch.object(FileManipulator, "_write_content_to_file")
def test_concatenate_content(
    group_content_mock,
    write_content_to_file_mock,
    file_manipulator,
    grouped_files,
    final_files,
):
    actual_result = sorted(file_manipulator.concatenate_content(grouped_files))
    assert actual_result == sorted(final_files)
    assert group_content_mock.called is True
    assert write_content_to_file_mock.called is True
