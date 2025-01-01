# -*- coding: utf-8 -*-
import os
import tomllib
from pathlib import Path
from typing import Optional
from snowflake.snowpark import Session


SNOWFLAKE_CONFIG_FILE_PATH: Path = Path('/root/.config/snowflake/config.toml')

def _get_snowflake_config(config_fl_path: Path = SNOWFLAKE_CONFIG_FILE_PATH) -> dict:
    if config_fl_path.exists():
        with config_fl_path.open('rb') as config_fl:
            return tomllib.load(config_fl)
    else:
        raise EnvironmentError('snowflake config file not found at provided path: {config_fl_path}')
    

def get_default_connection_credentials(config: Optional[dict] = None) -> dict[str, str]:
    if config is None: config = _get_snowflake_config()
    default_conn: str = config['default_connection_name']
    if default_conn in (conns := config['connections']):
        return conns[default_conn]
    else:
        raise ValueError('provided default connection {default_conn} not found in config connections: {conns}')


def container_session(creds: Optional[dict] = None) -> Session:
    if creds is None: creds = get_default_connection_credentials()
    return Session.builder.configs(creds).create()


if __name__ == '__main__':
    print(container_session())