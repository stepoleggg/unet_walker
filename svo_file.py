from pathlib import PurePath
from config import data_dir, svo_dir
from datetime import datetime
import os 
import time

class Svo_file:
    def __init__(self, svo_path):
        self.file_name = PurePath(svo_path).name
        self.svo_path = os.path.join(svo_dir, self.file_name)
        self.svo_data_dir = data_dir + "\\" + PurePath(svo_path).name[0:-4]
        self.svo_dir_name = PurePath(svo_path).name[0:-4]
        self.svo_dada_left = self.svo_data_dir + "\\" + "left"
        self.svo_dada_right = self.svo_data_dir + "\\" + "right"
        self.svo_dada_depth = self.svo_data_dir + "\\" + "depth"
        self.predict = False
        self.get_data = False
        self.date = datetime.now()
        self.analyze = False
    
    def get_data_for_insert(self):
        return [self.file_name, self.date, self.get_data, self.predict, self.analyze]

    @classmethod
    def from_query(cls, data):
        svo = cls(os.path.join(svo_dir, data[0]))
        svo.predict = bool(data[3])
        svo.get_data = bool(data[2])
        svo.date = datetime.fromtimestamp(time.mktime(time.strptime(data[1].split(".")[0], "%Y-%m-%d %H:%M:%S")))
        #svo.date = date.fromisoformat(data[1])
        svo.analyze = bool(data[4])
        return svo

    def __str__(self):
        return f"{self.file_name} predict {self.predict} get_data {self.get_data} analyze {self.analyze}"


    @staticmethod
    def is_unique(svos, svo):
        for sv in svos:
            if sv.file_name == svo.file_name:
                return (sv, False)
        return (svo, True)

