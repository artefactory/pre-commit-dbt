import argparse
import json
from pathlib import Path
from posixpath import split
from typing import Any
from typing import Dict
from typing import Optional
from typing import Sequence

from pre_commit_dbt.utils import add_filenames_args
from pre_commit_dbt.utils import add_manifest_args
from pre_commit_dbt.utils import get_filenames
from pre_commit_dbt.utils import get_json
from pre_commit_dbt.utils import get_macro_schemas
from pre_commit_dbt.utils import get_macro_sqls
from pre_commit_dbt.utils import get_macros
from pre_commit_dbt.utils import JsonOpenError


def has_reference(paths: Sequence[str], manifest: Dict[str, Any]) -> int:
    status_code = 0
    sqls = get_macro_sqls(paths, manifest)
    filenames = set(sqls.keys())
    nodes = manifest.get("nodes", {})

    # get manifest macros that pre-commit found as changed
    macros = get_macros(manifest, filenames)
    for macro in macros :
        macro_name = macro.macro_name
        found = False
        for key,value in nodes.items() :
            macros_as_declared_in_manifest = value.get("depends_on",{}).get("macros",{})
            macros_transformed_names = map(lambda x:x.split(".")[-1], macros_as_declared_in_manifest) # maps original list elements which have the following format macro.[project_name].[macro_name] to macro_name
            if macro_name in macros_transformed_names:
                found = True
                break
            else:
                continue
        if not found:
            print(f'The macro {macro_name} was not referenced in any model.')
            status_code = 1
    return status_code
    
def main(argv: Optional[Sequence[str]] = None) -> int :
     parser = argparse.ArgumentParser()
     add_filenames_args(parser)
     add_manifest_args(parser)
     args = parser.parse_args(argv)

     try:
         manifest = get_json(args.manifest)
     except JsonOpenError as e:
         print(f"Unable to load manifest file ({e})")
         return 1

     return has_reference(paths=args.filenames, manifest=manifest)

if __name__ == "__main__":
     exit(main())

# # Opening JSON file
# home_path=str(Path.home())
# manifest_path=f'{home_path}/Downloads/jaffle_shop-main/target/manifest.json'
# f = open(manifest_path)
# data = json.load(f)
# path_macro = [f'{home_path}/Downloads/jaffle_shop-main/macros/cents_to_dollars.sql']
# has_reference(path_macro, data)

    

