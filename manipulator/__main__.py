import argparse
from pathlib import Path

from manipulator import logger
from manipulator.file_processor import FileManipulator


def main(args):
    logger.debug(f"Passed arguments: {args}")
    FileManipulator(args.input_dir, args.output_30r, args.output_300r).process()


class MultilineFormatter(argparse.HelpFormatter):
    """
    Basically inherits the behavior of class HelpFormatter.
    Overrides the methods to display help and description.
    """

    def _fill_text(self, text, width, indent):
        return "".join([indent + line.strip(" ") for line in text.splitlines(True)])

    def _split_lines(self, text, width):
        return [line.strip() for line in text.splitlines()]


class IsValidDirAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        dir_path = Path(values)
        if not (dir_path.is_dir() and dir_path.exists()):
            raise ValueError(f"Directory {values} does not exist")
        setattr(namespace, self.dest, values)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="File manipulator",
        usage="manipulator",
        description="An util for file manipulation.",
        formatter_class=MultilineFormatter,
    )

    parser.add_argument(
        "-i",
        "--input_dir",
        help="Input dir for file transformation",
        required=True,
        type=Path,
        action=IsValidDirAction,
    )
    parser.add_argument(
        "-o30",
        "--output_30r",
        help="Output dir for .30rec files",
        required=True,
        type=Path,
        action=IsValidDirAction,
    )
    parser.add_argument(
        "-o300",
        "--output_300r",
        help="Output dir for grouped files",
        required=True,
        type=Path,
        action=IsValidDirAction,
    )

    main(parser.parse_args())
