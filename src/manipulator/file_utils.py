import glob
import re
import shutil
from collections import defaultdict
from functools import partial
from pathlib import Path
from typing import Dict, List

from manipulator import get_settings, logger

INPUT_FILE_EXT = get_settings().input_file_ext
OUTPUT_30R_FILE_EXT = get_settings().output_30r_file_ext
OUTPUT_300R_FILE_EXT = get_settings().output_300r_file_ext


class FileManipulator:
    def __init__(self, input_dir: Path, output_30r: Path, output_300r: Path):
        self.input_dir = input_dir
        self.output_30r = output_30r
        self.output_300r = output_300r

    def files_by_extension(self, file_extension=INPUT_FILE_EXT):
        return glob.glob(f"{self.input_dir}/*{file_extension}")

    @staticmethod
    def _change_extension(file: str, file_extension: str):
        return Path(file).rename(Path(file).with_suffix(file_extension))

    def change_files_extension(
        self, files: List[str], file_extension: str = OUTPUT_30R_FILE_EXT
    ):
        return list(
            map(partial(self._change_extension, file_extension=file_extension), files)
        )

    def _move_file(self, file: Path):
        return Path(shutil.copy(file, f"{self.output_30r}/{file.name}"))

    @staticmethod
    def _delete_files(files: List[Path]):
        return list(map(lambda file: Path(file).unlink(), files))

    def move_to_dir(self, files: List[Path]) -> List[Path]:
        moved_files = list(map(self._move_file, files))
        self._delete_files(files)
        return moved_files

    @staticmethod
    def _groups(filename: str):
        # Find by pattern YYYY_mm_DD_HH_MM, where mm_DD_HH - repeatable part
        return re.findall("([0-9]{4}_([0-9]{2}_){3})([0-9]{2})", filename)[0]

    def _group_name_parts(self, file: Path, group_interval: int = 5):
        first, _, minutes = self._groups(filename=file.name)
        minute_group = (int(minutes) // group_interval) * group_interval
        return first, minute_group

    def group_files(self, files: List[Path]) -> Dict[str, List[Path]]:
        files_groups = defaultdict(list)

        for file in files:
            first, minute_group = self._group_name_parts(file)
            group_name = Path(f"{file.parent}/{first}{minute_group}*")
            if not group_name.exists():
                Path.mkdir(group_name, parents=True, exist_ok=True)

            files_groups[group_name].append(f"{group_name}/{file.name}")

            shutil.copy(file, group_name)
            self._delete_files([file])

        return files_groups

    def _group_final_filepath(
        self, group: str, final_extension: str = OUTPUT_300R_FILE_EXT
    ) -> Path:
        first_part, minutes = re.findall("(.+)([0-9]{2})\\*", str(group))[0]
        new_first_part = first_part.replace(str(self.output_30r), str(self.output_300r))
        return Path(f"{new_first_part}{int(minutes) + 4.59}_*{final_extension}")

    @staticmethod
    def _group_content(group_files: List[Path]):
        content = ""
        for file in group_files:
            # Here we can open each file in the new tread and read them faster.
            # Especially if they are quite large
            with open(file) as fp:
                content += fp.read()
        return content

    def concatenate_content(self, files_groups: Dict[str, List[Path]]):
        final_files = []
        for group in files_groups:
            final_file = self._group_final_filepath(group)
            content = self._group_content(files_groups[group])

            with open(final_file, "w") as fp:
                fp.write(content)

            final_files.append(final_file)
        return final_files

    def process(self):
        input_files = self.files_by_extension()
        logger.debug(f"Files in input dir {input_files}")

        files_new_ext = self.change_files_extension(input_files)
        logger.debug(f"Files with new extension: {files_new_ext}")

        files_in_new_dir = self.move_to_dir(files_new_ext)
        logger.debug(f"Files {files_in_new_dir} were successfully moved")

        files_groups = self.group_files(files_in_new_dir)
        logger.debug(f"Files groups: {files_groups}")

        final_files = self.concatenate_content(files_groups)
        logger.debug(f"Final files (with content from all group files): {final_files}")

        files_input_ext = self.change_files_extension(final_files, INPUT_FILE_EXT)
        logger.debug(f"Final files (with input extension): {files_input_ext}")
