"""
utils file for manage application logging.
"""
from __future__ import annotations

import logging
from logging import handlers
from pathlib import Path

def setup(alias: str = __file__, file_path: Path | str = "app.log", level: str | int = logging.DEBUG) -> logging.Logger:
    """
    Create a new logger with standard configuration for the majority project.
    :param level: the level of log.
    :param alias: the logger alias.
    :param file_path: the access path to the recorder work file.
    :return: a manipulable logger object.
    """
    # Ensure the file_path is a Path object.
    if isinstance(file_path, str):
        file_path = Path(file_path)
         
    # Ensure the directory exists.
    if not file_path.parent.exists():
        file_path.parent.mkdir(parents=True, exist_ok=True)

    # Create logger.
    logger = logging.getLogger(alias)
    logger.setLevel(level)

    # Create time rotating file handler and set level to debug.
    handler = handlers.TimedRotatingFileHandler(
        filename=file_path,
        when='D',  # Files are rotated.
        interval=1,  # Every day.
        backupCount=31,  # For one month.
        encoding='utf-8',  # Use ASCII encoding.
        utc=True  # Use utc timestamp.
    )
    handler.setLevel(level)

    # Create formatter
    formatter = logging.Formatter(
        fmt="%(process)d %(asctime)s %(levelname)-8s In:%(module)s|%(lineno)d : %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z"
    )

    # Add formatter to handler
    handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(handler)

    return logger  # Return logger object.

def get(alias: str) -> logging.Logger:
    """
    Get a logger instance.
    :param alias: the logger alias.
    :return: a manipulable logger object.
    """
    return logging.getLogger(alias)
