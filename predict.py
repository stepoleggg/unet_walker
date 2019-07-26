from model import *
from data import *

# доступные классы
# 'ground', 'tree', 'bush', 'tower', 'wire', 'copter', 'car', 'build'
# для каких классов была обучена?
channels = ['wires', 'copter']

model = unet(len(channels), pretrained_weights = 'wires_copter.hdf5')

testGene = testGenerator("data/walker/train/image/","data/walker/predict/")

results = model.predict_generator(testGene,20,verbose=1)
saveResult("data/walker/predict/",results, channels)