from typing import Any
import sqlite3

class ConnectionManager:

    def __init__(self, database: str) -> None:
        self.db = database
        try:
            self.connection = sqlite3.connect(database)
            self.cursor = self.connection.cursor()
            print(f"Successfully connected to {database}")

        except sqlite3.Error as error:
            print(f"Error occured during database connection: {error}")
            self.close()

    def query(self, query: str) -> list[Any]:
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()

        except sqlite3.Error as error:
            print(f"Error occured during database query: {error}")
            return []

    def close(self) -> None:
        if self.connection:
                self.cursor.close()
                self.connection.close()
                print(f"Connection to {self.db} closed")
