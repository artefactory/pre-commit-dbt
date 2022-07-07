import pytest
import os

from pre_commit_dbt.check_source_folder_constraint import main

TESTS = (  # type: ignore
    (
        """
version: 2

sources:
-   name: jaffle_shop
    tables:
      - name: orders
      - name: customers
    """,
        0,
        "/models/sources.yml",
        "sources",
    ),
    (
        """
version: 2

sources:
-   name: jaffle_shop
    tables:
      - name: orders
      - name: customers
    """,
        1,
        "/models/sources.yml",
        "models",
    ),
)

@pytest.mark.parametrize(("schema_yml", "expected_status_code", "source_path", "undesired_path"), TESTS)
def test_check_source_folder_constraint(schema_yml, expected_status_code, source_path, undesired_path, tmpdir):
    source_dir=tmpdir.mkdir(source_path[:source_path.rfind(os.sep)]) # source_path[:source_path.rfind(os.sep)] would return the path without the names of the yaml file
    yml_file = source_dir.join(source_path[source_path.rfind(os.sep):]) # source_path[source_path.rfind(os.sep):] would return the name of the yaml file
    yml_file.write(schema_yml)
    result = main(
        argv=[
            str(yml_file),
            "--source-folder",
            str(tmpdir.join(undesired_path)),
        ],
    )
    assert result == expected_status_code
