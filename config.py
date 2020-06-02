import configparser

config = configparser.ConfigParser()
config.read('config.ini')
data_dir = config['DEFAULT']['data_dir']
db_name = config['DEFAULT']['db_name']
weights_path = config['DEFAULT']['weights_path']
predict_path = config['DEFAULT']['predict_path']
train_path = config['DEFAULT']['predict_path']
bush_treshold = float(config['DEFAULT']['bush_treshold'])
average_frame_size = int(config['DEFAULT']['average_frame_size'])
svo_dir = config['DEFAULT']['svo_dir']
lap_height = float(config['DEFAULT']['lap_height'])
max_d_on_table = int(config['DEFAULT']['max_d_on_table'])
max_bush_height = float(config['DEFAULT']['max_bush_height'])