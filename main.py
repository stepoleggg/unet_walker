from model import unet, ModelCheckpoint
from data import trainGenerator

# доступные классы
# 'ground', 'tree', 'bush', 'tower', 'wires', 'copter', 'car', 'build'
channels = ['wires', 'copter', 'bush']
#претренированные веса:
pretrained_weights_path = ''
#сохранить в веса:
weights_path = 'weights/wires_copter_bush.hdf5'

train_path = 'data/train/'

myGene = trainGenerator(channels)
model = unet(len(channels), pretrained_weights = pretrained_weights_path)

model_checkpoint = ModelCheckpoint(weights_path, monitor='loss', verbose=1, save_best_only=True)
model.fit_generator(myGene, steps_per_epoch=600, epochs=1000, callbacks=[model_checkpoint])