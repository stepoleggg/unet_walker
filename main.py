from model import unet, ModelCheckpoint
from data import trainGenerator
import os

# доступные классы
# 'ground', 'tree', 'bush', 'tower', 'wires', 'copter', 'car', 'build'
channels = ['wires', 'copter', 'bush']
#претренированные веса:
pretrained_weights_path = 'hfhfh'
#сохранить в веса:
weights_path = 'weights/weights_new.hdf5'
#путь к тренировочному датасету
train_path = 'data/train/'

if not os.path.exists('weights'):
    os.makedirs('weights')

myGene = trainGenerator(channels)
model = unet(len(channels), pretrained_weights = pretrained_weights_path)

model_checkpoint = ModelCheckpoint(weights_path, monitor='loss', verbose=1, save_best_only=True)
model.fit_generator(myGene, steps_per_epoch=10, epochs=2, callbacks=[model_checkpoint])