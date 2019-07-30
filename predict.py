from model import *
from data import *

# доступные классы
# 'ground', 'tree', 'bush', 'tower', 'wire', 'copter', 'car', 'build'
# для каких классов была обучена?
channels = ['copter', 'wire']
weights_path = 'weights/wire_copter_256_2.hdf5'
test_path = 'data/test/left'
predict_path = 'data/predict/'
num = 2

model = unet(len(channels), pretrained_weights = weights_path)

testGene = testGenerator(test_path, predict_path)

results = model.predict_generator(testGene, num*15, verbose=1)
saveResult(predict_path, results, channels)