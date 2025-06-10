"""
Module file for manage task saving.
"""
from pathlib import Path
import csv

import utils.logger as logger
debug_logger = logger.get('debug')


ROOT_PATH = Path(__file__).parent.parent.resolve()
VAR_DIRECTORY_PATH = ROOT_PATH / "var"


def load_data(db_path: Path | str) -> tuple:
    if not db_path.parent.exists():
        db_path.parent.mkdir(parents=True, exist_ok=True)

    data = []
    columns = []

    if db_path.exists():
        try:
            with open(db_path, mode='r', newline='', encoding='utf-8') as db_file:
                dict_reader = csv.DictReader(db_file)
                columns = dict_reader.fieldnames
                for row in dict_reader:
                    data.append(row)
        except Exception as e:
            debug_logger.error(f"Failed to load data: {e}")
    else:
        debug_logger.error("File doesn't exist.")

    return columns, data

def write_data(data: dict, db_file: Path | str) -> None:
    if not db_file.parent.exists():
        db_file.parent.mkdir(parents=True, exist_ok=True)

    with open(db_file, mode='w', newline='', encoding='utf-8') as db_file:
        spam_writer = csv.writer(db_file, delimiter=',', quotechar='"')
        spam_writer.writerow(["Name", "Date", "Begin", "End", "Delay"])
        spam_writer.writerow(data.values())

def add_data(data: dict, db_file: Path | str) -> None:
    if not db_file.parent.exists():
        db_file.parent.mkdir(parents=True, exist_ok=True)

    if not db_file.exists():
        with open(db_file, mode='w', newline='', encoding='utf-8') as db_file:
            spam_writer = csv.writer(db_file, delimiter=',', quotechar='"')
            spam_writer.writerow(["Name", "Date", "Begin", "End", "Delay"])

    with open(db_file, "a+", encoding="utf-8", newline='') as file:
        spam_writer = csv.writer(file, delimiter=',', quotechar='"')
        spam_writer.writerow(data.values())
