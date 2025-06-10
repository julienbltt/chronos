#!/usr/bin/env python

"""Main file for documents manager application.
"""
from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path
import tkinter as tk

import utils.config as configmanager
import utils.logger as logger

import modules.app as app

__author__ = "Julien Balderiotti"
__copyright__ = "Copyright 2024, BLT Corporation"
__credits__ = ["Julien Balderiotti"]
__license__ = "GPL-3.0"
__version__ = "0.1"
__maintainer__ = "Julien Balderiotti"
__email__ = "julien.balderiotti@ik.me"
__status__ = "development" # or production

ROOT_PATH = Path(__file__).parent.resolve()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    # Add arguments here
    args = parser.parse_args(argv)

    # Load the configuration
    config = configmanager.load()

    # Configure the logging
    app_logger = logger.setup(alias="app", file_path=ROOT_PATH.joinpath("logs/app.log"), level="INFO")
    if config["DEFAULT"]["debug"] == "true":
        debug_logger = logger.setup(alias="debug", file_path=ROOT_PATH.joinpath("logs/debug.log"), level="DEBUG")

    # Display configuration loaded
    app_logger.info(f"Configuration loaded: {dict(config.items('DEFAULT'))}")

    # Implement behaviour here
    root_app = tk.Tk()
    app.ChronosApp(root_app, ROOT_PATH / "assets" / "chronos_icon.png")
    root_app.mainloop()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())