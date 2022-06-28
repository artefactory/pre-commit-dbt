import pytest
import os

from pre_commit_dbt.check_exposure_folder_constraint import main

TESTS = (  # type: ignore
    (
        """
version: 2

exposures:
  
  - name: weekly_jaffle_metrics
    type: dashboard
    maturity: high
    url: https://bi.tool/dashboards/1
    description: >
      Did someone say "exponential growth"?
    
    depends_on:
      - ref('fct_orders')
      - ref('dim_customers')
      - source('gsheets', 'goals')
      
    owner:
      name: Claire from Data
      email: data@jaffleshop.com
    """,
        1,
        "/models/sources.yml",
        "sources",
    ),
    (
        """
version: 2

exposures:
  
  - name: weekly_jaffle_metrics
    type: dashboard
    maturity: high
    url: https://bi.tool/dashboards/1
    description: >
      Did someone say "exponential growth"?
    
    depends_on:
      - ref('fct_orders')
      - ref('dim_customers')
      - source('gsheets', 'goals')
      
    owner:
      name: Claire from Data
      email: data@jaffleshop.com
    """,
        0,
        "/models/sources.yml",
        "models",
    ),
)

@pytest.mark.parametrize(("schema_yml", "expected_status_code", "exposure_path", "desired_path"), TESTS)
def test_check_source_folder_constraint(schema_yml, expected_status_code, exposure_path, desired_path, tmpdir):
    exposure_dir=tmpdir.mkdir(exposure_path[:exposure_path.rfind(os.sep)]) # exposure_path[:exposure_path.rfind(os.sep)] would return the path without the names of the yaml file
    yml_file = exposure_dir.join(exposure_path[exposure_path.rfind(os.sep):]) # exposure_path[exposure_path.rfind(os.sep):] would return the name of the yaml file
    yml_file.write(schema_yml)
    result = main(
        argv=[
            str(yml_file),
            "--exposure-folder",
            str(tmpdir.join(desired_path)),
        ],
    )
    assert result == expected_status_code