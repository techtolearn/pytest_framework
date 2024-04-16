from datetime import datetime

import psycopg2


class DatabaseHelper:

    def __init__(self, host, username, password, dbname, port):
        self.host = host
        self.username = username
        self.password = password
        self.database = dbname
        self.port = port
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                username=self.username,
                password=self.password,
                database=self.database,
            )

            self.cursor = self.connection.cursor()
            print("Connected to the database.")
        except Exception as e:
            print(f"Error connecting to the database: {e}")

    def execute_query(self, query):
        self.connection()
        try:
            self.cursor.execute(query)
            self.connection.commit()
            print("Query executed successfully.")
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            self.connection.rollback()
            self.disconnect()

    def fetch_rows_with_column_names(self, query):
        rows_with_column_names = []
        rows = self.execute_query(query)
        # Fetch column names
        column_names = [desc[0] for desc in self.cursor.description]
        # Fetch rows
        for row in rows:
            # Create a dictionary for each row with column names as keys
            row_dict = dict(zip(column_names, rows))
            rows_with_column_names.append(row_dict)
        return rows_with_column_names

    def delete_query(self, query):
        self.connection()
        try:
            self.cursor.execute(query)
            self.connection.commit()
            print("Query executed successfully")
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
        finally:
            self.connection.rollback()
            self.disconnect()

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Disconnected from the database")

