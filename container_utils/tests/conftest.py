import pytest
from pathlib import Path


@pytest.fixture(scope='package')
def config_fl_path() -> Path:
    return Path(__file__).parent / 'test_config.toml'


@pytest.fixture(scope='package')
def expected_config() -> dict:
    return {'default_connection_name': 'test_default', 'cli': {'logs': {'save_logs': True, 'path': '/a/path', 'level': 'info'}}, 'connections': {'test_default': {'account': 'test_account', 'user': 'test_user', 'password': 'test_pass', 'database': 'test_database', 'warehouse': 'test_wh', 'role': 'test_role'}}}
