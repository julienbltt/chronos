"""
Utils file for manage configuration files.
"""
from __future__ import annotations

import configparser
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent.resolve()
CONFIGURATION_FILE_PATH = ROOT_PATH / "config/specifications.ini"
# DEFAULT SPECIFICATION
SPECIFICATION_STR = """
[DEFAULT]
Debug = true
"""


def load() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    if not config.read(CONFIGURATION_FILE_PATH):
        CONFIGURATION_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
        CONFIGURATION_FILE_PATH.touch()
        config.read_string(SPECIFICATION_STR)
        with open(CONFIGURATION_FILE_PATH, "w", encoding="ascii") as config_file:
            config.write(config_file)
        config.read(CONFIGURATION_FILE_PATH)
    return config
