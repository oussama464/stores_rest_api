import sqlite3
import pathlib
from flask_sqlalchemy import SQLAlchemy

DB_PATH = pathlib.Path(__file__).parent.parent.joinpath("data.db")


db: SQLAlchemy = SQLAlchemy()


class SQLite:
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        self.connection = sqlite3.connect(self.file_name)

    def __enter__(self):
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.commit()
        self.connection.close()
