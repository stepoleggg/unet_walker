from model import *
from data import *

# доступные классы
# 'ground', 'tree', 'bush', 'tower', 'wire', 'copter', 'car', 'build'
# для каких классов была обучена?
channels = ['wires', 'copter']
weights_path = 'weights/wires_copter.hdf5'
test_path = 'data/test/'
predict_path = 'data/predict/'

model = unet(len(channels), pretrained_weights = weights_path)

testGene = testGenerator(test_path, predict_path)

results = model.predict_generator(testGene, 20, verbose=1)
saveResult(predict_path, results, channels)