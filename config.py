import configparser

config = configparser.ConfigParser()
config.read('config.ini')
data_dir = config['DEFAULT']['data_dir']
db_name = config['DEFAULT']['db_name']
weights_path = config['DEFAULT']['weights_path']
predict_path = config['DEFAULT']['predict_path']
train_path = config['DEFAULT']['predict_path']
bush_treshold = float(config['DEFAULT']['bush_treshold'])