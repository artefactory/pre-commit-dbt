import pytest

from pre_commit_dbt.check_exposure_has_owner import main


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
      - ref('stg_orders')
      
    owner:
      email: data@jaffleshop.com
    """,
        1,
        [],
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
      - ref('stg_orders')
      
    owner:
      name: Charbel
      email: data@jaffleshop.com
    """,
        0,
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
