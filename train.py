from model import unet, ModelCheckpoint
from data import trainGenerator
from config import weights_path, train_path
import os

def train():
    # доступные классы
    # 'ground', 'tree', 'bush', 'tower', 'wires', 'copter', 'car', 'build'
    channels = ['bush']
    #претренированные веса:
    pretrained_weights_path = weights_path
    #сохранить в веса:
    save_weights_path = weights_path

    if not os.path.exists('weights'):
        os.makedirs('weights')

    myGene = trainGenerator(channels)
    model = unet(len(channels), pretrained_weights = pretrained_weights_path)

    model_checkpoint = ModelCheckpoint(save_weights_path, monitor='loss', verbose=1, save_best_only=True)
    model.fit_generator(myGene, steps_per_epoch=600, epochs=1000, callbacks=[model_checkpoint])

if __name__ == "__main__":
    train()