
import pytest

from pre_commit_dbt.check_exposure_has_models import main

TESTS = (  # type: ignore
    (
        """
version: 2
exposures:
  - name: weekly_jaffle_metrics
    depends_on:
      - ref('fct_orders')
      - ref('dim_customers')
      - source('gsheets', 'goals')
    """,
        0,
        [],
    ),
    (
        """
version: 2
exposures:
  - name: weekly_jaffle_metrics
    depends_on:
    """,
        1,
        [],
    ),
    (
        """
version: 2
exposures:
  - name: weekly_jaffle_metrics
    """,
        1,
        [],
    ),
)

@pytest.mark.parametrize(("schema_yml", "expected_status_code", "ignore"), TESTS)
def test_check_column_desc_is_same(schema_yml, expected_status_code, ignore, tmpdir):
    yml_file = tmpdir.join("schema.yml")
    yml_file.write(schema_yml)
    input_args = [str(yml_file)]
    input_args.extend(ignore)
    status_code = main(input_args)
    assert status_code == expected_status_code