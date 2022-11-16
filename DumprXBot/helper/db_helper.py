from psycopg2 import DatabaseError, connect

from DumprXBot import CONTENT_FORMATS, DB_URL, LOGGER
from DumprXBot.helper.text_helper import bold, mono


class DbManager:
    def __init__(self) -> None:
        self.error = False
        self.connect()

    def connect(self):
        try:
            self.conn = connect(DB_URL)
            self.cur = self.conn.cursor()
        except DatabaseError as error:
            LOGGER.error(f"Error in DB connection: {error}")
            self.error = True

    def disconnect(self):
        self.cur.close()
        self.conn.close()

    def db_init(self):
        if self.error:
            return
        sql = """
        CREATE TABLE IF NOT EXISTS dumpr (
            contype text
        );
        """
        self.cur.execute(sql)
        self.conn.commit()
        LOGGER.info("Database Initiated")
        self.db_load()

    def db_load(self):
        self.cur.execute("SELECT contype FROM dumpr;")
        ctypes = self.cur.fetchall()
        if ctypes:
            for ctype in ctypes:
                CONTENT_FORMATS.append(ctype[0])
            LOGGER.info("Content data has been loaded from Database")
        self.disconnect()

    def addcon(self, cont: str):
        if self.error:
            return "Error in DB_URL connection, check logs for details"
        self.cur.execute(f"INSERT INTO dumpr (contype) VALUES (%s)", (cont,))
        self.conn.commit()
        self.disconnect()
        return f"Successfully added {mono(f'{cont}')} to {bold('Content formats!')}"

    def rmcon(self, cont: str):
        if self.error:
            return "Error in DB_URL connection, check logs for details"
        self.cur.execute("DELETE FROM dumpr WHERE contype = %s", (cont,))
        self.conn.commit()
        self.disconnect()
        return (
            f"Successfully removed  {mono(f'{cont}')} from {bold('Content formats!')}"
        )


if DB_URL is not None:
    DbManager().db_init()
