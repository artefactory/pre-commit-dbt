import argparse
import json
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
    print(filenames)

    # get manifest macros that pre-commit found as changed
    macros = get_macros(manifest, filenames)
    for i in macros :
        print (i)

 
# Opening JSON file
with open('/Users/miriam.benallou/Downloads/jaffle_shop-main/target/manifest.json') as json_file:
    data = json.load(json_file)
    path_macro = ["/Users/miriam.benallou/Downloads/jaffle_shop-main/macros"]
    has_reference(path_macro, data)

