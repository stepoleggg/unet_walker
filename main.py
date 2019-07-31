from model import unet, ModelCheckpoint
from data import trainGenerator

# доступные классы
# 'ground', 'tree', 'bush', 'tower', 'wires', 'copter', 'car', 'build'
channels = ['wires']
#претренированные веса:
pretrained_weights_path = ''
#сохранить в веса:
weights_path = 'weights/wires_256_4.hdf5'

train_path = 'data/train/'

myGene = trainGenerator(channels)
model = unet(len(channels), pretrained_weights = pretrained_weights_path)

model_checkpoint = ModelCheckpoint(weights_path, monitor='loss', verbose=1, save_best_only=True)
model.fit_generator(myGene, steps_per_epoch=10, epochs=2, callbacks=[model_checkpoint])