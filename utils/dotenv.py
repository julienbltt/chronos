"""
Utils file for manage the environment variables.
"""
from __future__ import annotations

import os
from pathlib import Path

# Using : os.getenv(<env>)

def load(filepath: Path | str = '.env') -> None:
    with open(file=filepath) as envfile:
        for line in envfile:
            if line.startswith('#') or not line.strip():
                continue
            key, value = line.strip().split('=', 1)
            os.environ[key] = value