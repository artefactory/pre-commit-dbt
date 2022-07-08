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
from pre_commit_dbt.utils import JsonOpenError

def get_macro_name(macros_ref):
    return map(lambda x:x.split(".")[-1], macros_ref) 

def get_macros_in_models(manifest):
    """
    Gets macros listed in the "depends_on" key of the "nodes" key in the manifest
    Arguments:
        manifest: manifest file 
    Returns:
        macros: list of macros
    """
    macros = []
    nodes = manifest.get("nodes", {})
    for key,value in nodes.items() :
            macros_ref_in_models = value.get("depends_on",{}).get("macros",{})
            macro_ref_name = get_macro_name(macros_ref_in_models) 
            macros.extend(macro_ref_name)
    return macros

def is_referenced(paths: Sequence[str], manifest: Dict[str, Any]) -> int:
    status_code = 0
    sqls = get_macro_sqls(paths, manifest)
    filenames = set(sqls.keys())

    # get manifest macros that pre-commit found as changed
    macros = list(get_macros(manifest, filenames))
    referenced_macros = get_macros_in_models(manifest)

    macros_not_referenced = [x for x in macros if x.macro_name not in referenced_macros]
    for macro in macros_not_referenced:
        status_code = 1
        print(f'The macro {macro.macro_name} was not referenced in any model.')
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

     return is_referenced(paths=args.filenames, manifest=manifest)

if __name__ == "__main__":
     exit(main())

    
