from pathlib import Path
import logging


def get_logger(name):
    return logging.getLogger(name)


def get_project_root():
    return Path(__file__).resolve().parents[2]


def get_logs_directory():
    path = get_project_root() / "logs"
    path.mkdir(exist_ok=True)
    return path
