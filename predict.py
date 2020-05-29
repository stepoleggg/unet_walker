from model import unet
from data import testGenerator, saveResult
import os
from config import weights_path, test_path, predict_path

def predict():
    # доступные классы
    # 'ground', 'tree', 'bush', 'tower', 'wire', 'copter', 'car', 'build'
    # для каких классов была обучена?
    channels = ['wires', 'copter', 'bush']

    if not os.path.exists(weights_path):
        print(f"Файл весов {weights_path} не существует!")
    else:
        num = len(os.listdir(test_path))
        model = unet(len(channels), pretrained_weights = weights_path)

        testGene = testGenerator(test_path)

        results = model.predict_generator(testGene, num*15, verbose=1)
        saveResult(predict_path, results, channels)

if __name__ == "__main__":
    predict()