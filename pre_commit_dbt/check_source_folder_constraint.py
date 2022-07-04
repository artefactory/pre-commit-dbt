import argparse
from pathlib import Path
from typing import Optional
from typing import Sequence

from pre_commit_dbt.utils import add_filenames_args
from pre_commit_dbt.utils import get_source_path

def check_source_path(paths: Sequence[str], source_folder_path: str) -> int:
    """
    Checks if sources are defined in the folder specified by the user
    Arguments:
        paths: a sequence of paths
        source_folder_path: string that represents the specified folder's path
    Returns:
        A status code (0 if the sources are placed in the correct folder and 1 otherwise)
    """   
    status_code = 0
    ymls = [Path(path) for path in paths]

    source_paths = get_source_path(ymls)
    misplaced_sources = {source_path for source_path in source_paths if source_folder_path in str(source_path)}
    for misplaced_source in misplaced_sources:
         status_code = 1
         print(
             f"{misplaced_source}: "
             f"is in the directory passed as argument for the hook",
         )
    return status_code

def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    add_filenames_args(parser)
    parser.add_argument(
        "--source-folder",
        required=True,
        help="Directory in which sources should not be defined.",
    )
    args = parser.parse_args(argv)
    return check_source_path(args.filenames, source_folder_path=args.source_folder)

if __name__ == "__main__":
    exit(main())
