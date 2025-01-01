import pytest 
from pathlib import Path
from container_utils.utils import _get_snowflake_config, get_default_connection_credentials


def test_testing() -> None:
    """THIS SHOULD FAIL"""
    assert True == False
    return None


def test__get_snowflake_config(config_fl_path: Path, expected_config: dict) -> None:
    actual = _get_snowflake_config(config_fl_path)
    assert expected_config ==  actual, 'Returns expected value with test file path input'
    with pytest.raises(EnvironmentError):
        inexistant_path = Path('/does/not/exist.toml')
        _get_snowflake_config(inexistant_path)

def test_get_default_connection(config_fl_path: Path, expected_config: dict) -> None:
    expected = expected_config['connections']['test_default']
    assert get_default_connection_credentials(_get_snowflake_config(config_fl_path)) == expected
