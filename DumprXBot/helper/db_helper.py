from NoobStuffs.libformatter import HTML
from psycopg2 import DatabaseError, connect

from DumprXBot import CONFIGS, CONTENT_FORMATS, DB_URL, LOGGER


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
        sql = """
        CREATE TABLE IF NOT EXISTS dumpr_configs (
            config text,
            status boolean
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
        self.cur.execute("SELECT * FROM dumpr_configs;")
        confs = self.cur.fetchall()
        if confs:
            for con in confs:
                CONFIGS[con[0]] = con[1]
            LOGGER.info("Configs data has been loaded from Database")
        self.disconnect()

    def addcon(self, cont: str):
        if self.error:
            return "Error in DB_URL connection, check logs for details"
        self.cur.execute(f"INSERT INTO dumpr (contype) VALUES (%s)", (cont,))
        self.conn.commit()
        self.disconnect()
        return f"Successfully added {HTML.mono(f'{cont}')} to {HTML.bold('Content formats!')}"

    def rmcon(self, cont: str):
        if self.error:
            return "Error in DB_URL connection, check logs for details"
        self.cur.execute("DELETE FROM dumpr WHERE contype = %s", (cont,))
        self.conn.commit()
        self.disconnect()
        return f"Successfully removed  {HTML.mono(f'{cont}')} from {HTML.bold('Content formats!')}"

    def toggleconf(self, conf_name: str, conf_status: bool):
        if self.error:
            return "Error in DB_URL connection, check logs for details"
        if self.check_conf(conf_name):
            self.cur.execute(
                "UPDATE dumpr_configs SET status = %s WHERE config = %s",
                (conf_status, conf_name),
            )
            self.conn.commit()
            self.disconnect()
            return f"Successfully updated config - {HTML.bold(f'{conf_name}:')} {HTML.mono(f'{conf_status}')}"
        self.cur.execute(
            "INSERT INTO dumpr_configs (config, status) VALUES (%s, %s)",
            (conf_name, conf_status),
        )
        self.conn.commit()
        self.disconnect()
        return f"Successfully added new config - {HTML.bold(f'{conf_name}:')} {HTML.mono(f'{conf_status}')}"

    def check_conf(self, conf_name: str):
        if self.error:
            return "Error in DB_URL connection, check logs for details"
        self.cur.execute("SELECT * FROM dumpr_configs WHERE config = %s", (conf_name,))
        res = self.cur.fetchone()
        return res

    def rmconf(self, conf_name: str):
        if self.error:
            return "Error in DB_URL connection, check logs for details"
        self.cur.execute("DELETE FROM dumpr_configs WHERE config = %s ", (conf_name,))
        self.conn.commit()
        self.disconnect()
        return f"Successfully removed config - {HTML.bold(f'{conf_name}:')}"


if DB_URL is not None:
    DbManager().db_init()
