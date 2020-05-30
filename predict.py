from model import unet
from data import testGenerator, saveResult
from analyzer import analyze_depth
from config import weights_path, test_path, predict_path
import os

def predict():
    # доступные классы
    # 'ground', 'tree', 'bush', 'tower', 'wire', 'copter', 'car', 'build'
    # для каких классов была обучена?
    channels = ['bush']

    if not os.path.exists(weights_path):
        print(f"Файл весов {weights_path} не существует!")
    else:
        frames_length = len(os.listdir(test_path))
        model = unet(len(channels), pretrained_weights = weights_path)
        testGene = testGenerator(test_path)
        for frame_number in range(frames_length):
            pred = []
            for _ in range(15):
                pred.append(next(testGene))
            results = model.predict_generator(iter(pred), 15, verbose=1)
            analyze_depth(results, frame_number)
            #saveResult(predict_path, results, channels, f"{i}_predict.png")

if __name__ == "__main__":
    predict()