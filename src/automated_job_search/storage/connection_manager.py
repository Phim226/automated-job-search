from typing import Any
from pathlib import Path
import sqlite3

class ConnectionManager:

    def __init__(self, database: str | Path) -> None:
        self.db = database

    def chain_query(self, query_list: list[str]) ->list[Any]:
        try:
            self._connect()
            for query in query_list:
                self.cursor.execute(query)
                self.connection.commit()

            result = self.cursor.fetchall()

        except sqlite3.Error as error:
            print(f"Error occured during database query: {error}")
            result = []

        finally:
            self._close()

        return result

    def query(self, query: str) -> list[Any]:
        return self.chain_query([query])

    def _connect(self) -> None:
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
