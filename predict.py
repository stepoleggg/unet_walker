from model import *
from data import *

# доступные классы
# 'ground', 'tree', 'bush', 'tower', 'wire', 'copter', 'car', 'build'
# для каких классов была обучена?
channels = ['wires']

model = unet(len(channels), pretrained_weights = 'unet_walker3.hdf5')
model_checkpoint = ModelCheckpoint('unet_walker_wires.hdf5', monitor='loss',verbose=1, save_best_only=True)

testGene = testGenerator("data/walker/train/image/","data/walker/predict/")

results = model.predict_generator(testGene,20,verbose=1)
saveResult("data/walker/predict/",results, channels)