import argparse
from typing import Any
from typing import Dict
from typing import Optional
from typing import Sequence

from pre_commit_dbt.utils import add_filenames_args
from pre_commit_dbt.utils import add_manifest_args
from pre_commit_dbt.utils import get_json
from pre_commit_dbt.utils import get_macro_sqls
from pre_commit_dbt.utils import get_macros
from pre_commit_dbt.utils import get_macros_names_in_models
from pre_commit_dbt.utils import get_unreferenced_macros
from pre_commit_dbt.utils import JsonOpenError


def macros_have_reference(paths: Sequence[str], manifest: Dict[str, Any]) -> int:
    status_code = 0
    sqls = get_macro_sqls(paths, manifest)
    filenames = set(sqls.keys())

    # get manifest macros that pre-commit found as changed
    macros = list(get_macros(manifest, filenames))
    referenced_macros = get_macros_names_in_models(manifest)

    unreferenced_macros = get_unreferenced_macros(macro, referenced_macros)

    for macro in unreferenced_macros:
        status_code = 1
        print(f'The macro {macro.macro_name} was not referenced in any model.')
    return status_code


def main(argv: Optional[Sequence[str]] = None) -> int:
     parser = argparse.ArgumentParser()
     add_filenames_args(parser)
     
     add_manifest_args(parser)
     args = parser.parse_args(argv)

     try:
         manifest = get_json(args.manifest)
     except JsonOpenError as e:
         print(f"Unable to load manifest file ({e})")
         return 1

     return macros_have_reference(paths=args.filenames, manifest=manifest)

if __name__ == "__main__":
     exit(main())

    
