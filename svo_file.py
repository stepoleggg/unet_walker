from pathlib import PurePath
from config import data_dir
class Svo_file:
    def __init__(self, svo_path):
        self.svo_path = svo_path
        self.file_name = PurePath(svo_path).name
        self.svo_data_dir = data_dir + "\\" + PurePath(svo_path).name[0:-4]
        self.svo_dada_left = self.svo_data_dir + "\\" + "left"
        self.svo_dada_right = self.svo_data_dir + "\\" + "right"
        self.svo_dada_depth = self.svo_data_dir + "\\" + "depth"    