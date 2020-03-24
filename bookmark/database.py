"""Database management"""

import psycopg2

from bookmark.config import DatabaseConfig


class DatabaseConnector:
    """Manage connection to a PostgreSQL database"""

    def __init__(self):
        self.con = None

    def initialize_connection(self, db_config: DatabaseConfig):
        try:
            self.con = psycopg2.connect(
                host=db_config.host,
                port=db_config.port,
                dbname=db_config.db_name,
                user=db_config.user,
                password=db_config.password,
                options=f'-c search_path={db_config.schema}'
            )
        except psycopg2.DatabaseError as ex:
            raise RuntimeError('Database error', ex)

    def close_connection(self):
        try:
            self.con.close()
        except Exception:
            raise RuntimeError('Database is now unavailable, please try again later')
