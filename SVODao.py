import sqlite3
from config import db_name
from svo_file import Svo_file

class Svo_DB:
    def __init__(self):
        Svo_DB.execute(f'CREATE TABLE IF NOT EXISTS {db_name} (svo_name text, svo_date date, get_data bool, predict bool, analyze bool)')
    @staticmethod
    def execute(sql, param = None):
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        if param:
            cur.execute(sql, param)
        else:
            cur.execute(sql)
        res = cur.fetchall()
        conn.commit()
        conn.close()
        return res

    @staticmethod
    def insert_svo(svo: Svo_file):
        Svo_DB.execute(f"INSERT INTO {db_name} VALUES(?, ?, ?, ?, ?)", svo.get_data_for_insert())

    @staticmethod
    def update_svo(svo: Svo_file):    
        Svo_DB.execute(f"UPDATE {db_name} SET svo_date=?, get_data=?, predict=?, analyze=? where svo_name=?", svo.get_data_for_insert()[1:] + [svo.file_name])

    @staticmethod
    def get_svo_by_name(svo: Svo_file) -> Svo_file:
        res = Svo_DB.execute(f"SELECT * from {db_name} WHERE svo_name = ?", [svo.file_name])
        if res:
            return Svo_file.from_query(res[0])
        return None

    @staticmethod
    def get_all_svo():
        res = Svo_DB.execute(f"SELECT * FROM {db_name}")
        svos = []
        for row in res:
            svos.append(Svo_file.from_query(row))
        return svos

Svo_DB()