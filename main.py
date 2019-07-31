from model import *
from data import *

data_gen_args = dict(rotation_range=0.2,
                    width_shift_range=0.05,
                    height_shift_range=0.05,
                    shear_range=0.05,
                    zoom_range=0.05,
                    horizontal_flip=True,
                    fill_mode='nearest')

# доступные классы
# 'ground', 'tree', 'bush', 'tower', 'wires', 'copter', 'car', 'build'
channels = ['wires']
#претренированные веса:
pretrained_weights_path = 'weights/wires_256_4.hdf5'
#сохранить в веса:
weights_path = 'weights/wires_256_4.hdf5'

train_path = 'data/train/'

myGene = trainGenerator(2, train_path, 'left', 'depth', 'mask', channels, data_gen_args, save_to_dir = None)

model = unet(len(channels), pretrained_weights = pretrained_weights_path)

model_checkpoint = ModelCheckpoint(weights_path, monitor='loss',verbose=1, save_best_only=True)
model.fit_generator(myGene,steps_per_epoch=288,epochs=1000,callbacks=[model_checkpoint])