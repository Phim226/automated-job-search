from typing import Any
from pathlib import Path
import sqlite3

class ConnectionManager:

    def __init__(self, database: str | Path) -> None:
        self.db = database

    def chain_query(self, query_list: list[str]) ->list[Any]:
        current_query = ""
        try:
            self._connect()
            for query in query_list:
                current_query = query
                self.cursor.execute(query)

            self.connection.commit()

            result = self.cursor.fetchall()

        except sqlite3.Error:
            self.connection.rollback()
            print(f"Query: {current_query}")
            raise

        finally:
            self._close()

        return result

    def query(self, query: str) -> list[Any]:
        return self.chain_query([query])

    def _connect(self) -> None:
        self.connection = sqlite3.connect(self.db)
        self.cursor = self.connection.cursor()


    def _close(self) -> None:
        if self.connection:
                self.cursor.close()
                self.connection.close()
