import argparse
from pathlib import Path
from typing import Optional
from typing import Sequence
import logging

from pre_commit_dbt.utils import add_filenames_args
from pre_commit_dbt.utils import get_source_path


def check_source_path(paths: Sequence[str], folder_name: Sequence[str]) -> int:
    status_code = 0
    ymls = [Path(path) for path in paths]

    # if user added schema but did not rerun
    schemas = get_source_path(ymls)
    return schemas

def main(argv: Optional[Sequence[str]] = None) -> int:
    logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    add_filenames_args(parser)
    parser.add_argument(
        "--folder-name",
        nargs="+",
        required=True,
        help="Folder in which sources should be defined.",
    )

    args = parser.parse_args(argv)
    logging.debug(check_source_path(args.filenames, folder_name=args.folder_name))
    return 0


if __name__ == "__main__":
    exit(main())
