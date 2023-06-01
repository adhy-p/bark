from typing import Dict
import sqlite3


class DatabaseManager:
    """
    DatabaseManager is our own convenience class to make
    interacting with sqlite3 database easier
    """

    def __init__(self, db_path: str):
        self.connection = sqlite3.connect(db_path)

    def __del__(self):
        self.connection.close()

    def _execute(self, statement, values=None):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(statement, values or [])
            return cursor

    def create_table(self, table_name: str, columns: Dict[str, str]):
        """
        Create a new table in the database if it does not exist yet.
        """
        typed_cols = [f"{col} {type_}" for col, type_ in columns.items()]
        statement = f"""
            CREATE TABLE IF NOT EXISTS {table_name}
            ({", ".join(typed_cols)})
            """
        self._execute(statement)

    def add(self, table_name: str, entries: Dict[str, str]):
        """
        Add a new entry to the specified table.

        Parameters:
            table_name (str) : name of the table
            entries (dict) : map of {'column_name': 'value'}
        """
        placeholders = f"({', '.join('?' * len(entries))})"
        col_names = ", ".join(entries.keys())
        statement = f"""
            INSERT INTO {table_name}
            ({col_names})
            VALUES {placeholders}
            """
        col_values = tuple(entries.values())
        self._execute(statement, col_values)

    def delete(self, table_name: str, criteria: Dict[str, str]):
        """
        Delete entries from the specified table which matches
        the specified criteria.

        For example, if the criteria is {'id': 1, 'name': 'alice'},
        then all entries with id = 1 and name = alice will be deleted.

        Parameters:
            table_name (str) : name of the table
            criteria (dict) : conditions to be met
        """
        placeholders = [f'{col} = ?' for col in criteria.keys()]
        delete_criteria = " AND ".join(placeholders)
        statement = f"""
            DELETE FROM {table_name}
            WHERE {delete_criteria}
            """
        criteria_values = tuple(criteria.values())
        self._execute(statement, criteria_values)

    def select(self, table_name: str,
               criteria: Dict[str, str] = None,
               order_by: str = None):
        """
        Select entries from the specified table which matches
        the specified criteria and sort using the specified key.

        Parameters:
            table_name (str) : name of the table
        Optional parameters:
            criteria (dict) : conditions to be met
            order_by (str) : key used to sort the entries
        """
        statement = f"""
            SELECT * FROM {table_name}
            """
        criteria_values = None
        if criteria:
            placeholders = [f'{col} = ?' for col in criteria.keys()]
            delete_criteria = " AND ".join(placeholders)
            statement += f"WHERE {delete_criteria}"
            criteria_values = tuple(criteria.values())
        if order_by:
            statement += "ORDER BY {str}"
        return self._execute(statement, criteria_values)
