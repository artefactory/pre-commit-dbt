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

''''
Tests the check-source-folder-constraint hook
 Arguments:
     schema_yml: source content
     expected_status_code: status code that should be returned by the test for the current test case
     source_path: path of the yaml file where the source is defined
     undesired_path: path/name of the folder where we don't want the source to be defined
 Returns:
     A status code (0 if the sources are not placed in the specified folder and 1 otherwise)
'''
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
