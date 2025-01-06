# -*- coding: utf-8 -*-
import os
import tomllib
from pathlib import Path
from typing import Optional, Literal, Any
from snowflake.snowpark import Session


SnowflakeConfig = dict[str, Any]

SnowflakeConnCreds = dict[str, str]

SNOWFLAKE_CONFIG_FILE_PATH: Path = Path("/root/.config/snowflake/config.toml")


def is_dev_container() -> bool:
    return os.getenv("IS_DEV_CONTAINER") == "True"


def _get_snowflake_config(
    config_fl_path: Path = SNOWFLAKE_CONFIG_FILE_PATH,
) -> SnowflakeConfig:
    if config_fl_path.exists():
        config_str: str = config_fl_path.read_text()
        return tomllib.loads(config_str)
    else:
        raise FileNotFoundError(
            f"snowflake config file not found at provided path: {config_fl_path}"
        )


def get_connection_credentials(conn_name: Optional[str] = None) -> SnowflakeConnCreds:
    config = _get_snowflake_config()
    if conn_name is None:
        if "default_connection_name" in config:
            conn_name = config["default_connection_name"]
        else:
            raise ValueError(
                f"No connection name given, and none set as default in snow cli config."
            )
    if conn_name in (conns := config["connections"]):
        creds: SnowflakeConnCreds = conns[conn_name]
        return creds
    else:
        raise ValueError(
            f"Connection {conn_name} not found in config connections: {conns.keys()}"
        )


def snow_cli_session(conn_name: Optional[str] = None) -> Session:
    creds = get_connection_credentials(conn_name)
    session: Session = Session.builder.configs(creds).create()
    return session


if __name__ == "__main__":
    if SNOWFLAKE_CONFIG_FILE_PATH.exists():
        print("Found snowflake cli configuration:\n")
        print(SNOWFLAKE_CONFIG_FILE_PATH.read_text())
    else:
        Warning("No snowflake cli configuration found")
