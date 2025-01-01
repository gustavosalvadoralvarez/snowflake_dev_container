import os
import tomllib
from pathlib import Path


SNOWFLAKE_CONFIG_FILE_PATH: Path = Path('/root/.config/snowflake/config.toml')


def _get_snowflake_config(config_fl_path: Path = SNOWFLAKE_CONFIG_FILE_PATH) -> dict:
    if config_fl_path.exists():
        with SNOWFLAKE_CONFIG_FILE_PATH.open('rb') as config_fl:
            config: dict = tomllib.load(config_fl)
            return config
    else:
        raise EnvironmentError(f'snowflake config file not found at path: {config_fl_path}') 
    

def default_connection() -> dict[str, str]:
    snowflake_config: dict = _get_snowflake_config()
    conn_name: str = snowflake_config['default_connection_name']
    if conn_name in (conns := snowflake_config['connections']): 
        return conns[conn_name]
    else:
         raise ValueError(f'default connection {conn_name} not found in provided connections: {conns}')



if __name__ == '__main__':

    print(_get_snowflake_config())
