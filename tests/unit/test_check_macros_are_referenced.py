import pytest

from pre_commit_dbt.check_macros_are_referenced import main


 # Input args, valid manifest, expected return value
TESTS = (
     (["macros/aa/with_referencing.sql"], True, 0),
     (["macros/aa/without_referencing_2.sql"], False, 1),
     (["macros/aa/without_referencing.sql"], True, 1),
 )

@pytest.mark.parametrize(
     ("input_args", "valid_manifest", "expected_status_code"), TESTS
 )
def test_check_macro_referencing(
     input_args, valid_manifest, expected_status_code, manifest_path_str
 ):
     if valid_manifest:
             input_args.extend(["--manifest", manifest_path_str])
     status_code = main(input_args)
     assert status_code == expected_status_code