import configparser

config = configparser.ConfigParser()
config.read('config.ini')
data_dir = config['DEFAULT']['data_dir']
db_name = config['DEFAULT']['db_name']
weights_path = config['DEFAULT']['weights_path']
test_path = config['DEFAULT']['test_path']
predict_path = config['DEFAULT']['predict_path']