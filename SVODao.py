import sqlite3
from config import db_name

class Svo_DB:
    @staticmethod
    def execute(sql, param):
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute(sqlite3, param)
        res = cur.fetchall()
        conn.commit()
        conn.close()
        return res