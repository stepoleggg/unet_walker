from model import unet
from data import testGenerator, saveResult

# доступные классы
# 'ground', 'tree', 'bush', 'tower', 'wire', 'copter', 'car', 'build'
# для каких классов была обучена?
channels = ['wires', 'copter', 'bush']
weights_path = 'weights/wires_copter_bush.hdf5'
test_path = 'data/predict/left'
predict_path = 'data/predict/mask'
num = 9
model = unet(len(channels), pretrained_weights = weights_path)

testGene = testGenerator(test_path)

results = model.predict_generator(testGene, num*15, verbose=1)
saveResult(predict_path, results, channels)