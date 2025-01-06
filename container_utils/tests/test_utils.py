import pytest 
import os
import tomllib
from pathlib import Path
from typing import Any
from unittest.mock import mock_open, patch, MagicMock
from snowflake.snowpark import Session
from container_utils.utils import _get_snowflake_config
from container_utils import (
    is_dev_container,
    get_connection_credentials, 
    snow_cli_session
)


@pytest.mark.xfail
def test_testing() -> None:
    """THIS SHOULD FAIL"""
    assert True == False
    return None


def test__get_snowflake_config_happy_path(config_fl_path: Path, expected_config: dict[str, Any]) -> None:
    # WITH CREDENTIALS FILE AS INPUT
    actual = _get_snowflake_config(config_fl_path)
    assert expected_config ==  actual
    # READING FROM DEFAULT CRED FILE PATH
    mock_data: str = config_fl_path.read_text()
    with patch("pathlib.Path.read_text", return_value=mock_data) as mocked_file:
        with patch("pathlib.Path.exists", return_value=True):
            config = _get_snowflake_config()
            assert config == expected_config

def test__get_snowflake_config_unhappy_path(config_fl_path: Path, expected_config: dict[str, Any]) -> None:
    with patch("pathlib.Path.exists", return_value=False):
        with pytest.raises(FileNotFoundError):
            _get_snowflake_config()



def test_is_dev_container() -> None:
    os.environ["IS_DEV_CONTAINER"] = "True"
    assert is_dev_container()
    os.environ["IS_DEV_CONTAINER"] = "Any other string"
    assert not is_dev_container()


def test_get_connection_credentials_happy_path(config_fl_path: Path, expected_config: dict) -> None:
    conn_name = 'test_conn'
    expected = expected_config['connections'][conn_name]
    mock_data = config_fl_path.read_text()
    # WITH CONNECTION NAME AS INPUT
    with patch("pathlib.Path.read_text", return_value=mock_data):
        with patch("pathlib.Path.exists", return_value=True):
            actual = get_connection_credentials(conn_name)
            assert actual == expected
    # RETRIEVING DEFAULT CONNECTION NAME FROM CONFIG
    expected = expected_config['connections']['test_default']
    with patch("pathlib.Path.read_text", return_value=mock_data):
        with patch("pathlib.Path.exists", return_value=True):
            actual = get_connection_credentials()
            assert actual == expected


def test_get_connection_credentials_unhappy_path(config_fl_path: Path) -> None:
    with pytest.raises(ValueError):
        get_connection_credentials('not a connection')
    # WITHOUT DEFAULT CONFIG
    mock_data = '\n'.join(config_fl_path.read_text().split('\n')[-1:])
    with patch("pathlib.Path.read_text", return_value=mock_data):
        with patch("pathlib.Path.exists", return_value=True):
            with pytest.raises(ValueError):
                get_connection_credentials()


def test_snow_cli_session_happy_path(config_fl_path: Path, expected_config: dict) -> None:
    mock_data = config_fl_path.read_text()
    expected_creds = expected_config['connections']['test_default']
    with patch("pathlib.Path.read_text", return_value=mock_data):
        with patch("pathlib.Path.exists", return_value=True):
            with patch("container_utils.utils.Session") as mock_session:
                mock_builder = MagicMock()
                mock_session.builder = mock_builder
                mock_builder.configs.return_value.create.return_value = "__mocked__"
                actual = snow_cli_session()
                mock_builder.configs.assert_called_once_with(expected_creds)
                assert actual == "__mocked__"
    expected_creds = expected_config['connections']['test_conn']
    with patch("pathlib.Path.read_text", return_value=mock_data):
        with patch("pathlib.Path.exists", return_value=True):
            with patch("container_utils.utils.Session") as mock_session:
                mock_builder = MagicMock()
                mock_session.builder = mock_builder
                mock_builder.configs.return_value.create.return_value = "__mocked__"
                actual = snow_cli_session('test_conn')
                mock_builder.configs.assert_called_once_with(expected_creds)
                assert actual == "__mocked__"


def test_snow_cli_session_unhappy_path(config_fl_path: Path, expected_config: dict) -> None:
    mock_data = config_fl_path.read_text()
    expected_creds = expected_config['connections']['test_default']
    # NO CONFIG EXISTS
    with patch("pathlib.Path.exists", return_value=False):
        with pytest.raises(FileNotFoundError):
            actual = snow_cli_session()
    # NO DEFAULT CONN SET IN CONFIG
    with patch("pathlib.Path.read_text", return_value=mock_data):
        with patch("pathlib.Path.exists", return_value=True):
            with patch("container_utils.utils.Session") as mock_session:
                mock_builder = MagicMock()
                mock_session.builder = mock_builder
                mock_builder.configs.return_value.create.return_value = "__mocked__"
                actual = snow_cli_session('test_conn')
                mock_builder.configs.assert_called_once_with(expected_creds)
                assert actual == "__mocked__"