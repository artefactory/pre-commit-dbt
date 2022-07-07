import argparse
from pathlib import Path
from typing import Optional
from typing import Sequence

from pre_commit_dbt.utils import add_filenames_args
from pre_commit_dbt.utils import get_exposure_paths

def check_exposure_path(paths: Sequence[str], exposure_folder_path: str) -> int:
    """
    Checks if exposures are defined in the folder specified by the user
    Arguments:
        paths: a sequence of paths
        exposure_folder_path: string that represents the specified folder's path
    Returns:
        A status code (0 if the exposures are placed in the correct folder and 1 otherwise)
    """
    status_code = 0
    ymls = [Path(path) for path in paths]

    exposure_paths = get_exposure_paths(ymls)
    misplaced_exposures = {exposure.exposure_path for exposure in exposure_paths if exposure_folder_path not in str(exposure.exposure_path)}
    for misplaced_exposure in misplaced_exposures:
        status_code = 1
        print(
            f"{misplaced_exposure}: "
            f"is not in the directory passed as argument for the hook",
        )
    return status_code

def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    add_filenames_args(parser)
    parser.add_argument(
        "--exposure-folder",
        required=True,
        help="Directory in which exposures should be defined.",
    )
    args = parser.parse_args(argv)
    return check_exposure_path(args.filenames, exposure_folder_path=args.exposure_folder)

if __name__ == "__main__":
    exit(main())
