from model import unet
from data import testGenerator, saveResult
from analyzer import analyze_bush_depth
from config import weights_path, predict_path
from pathlib import PurePath
import os

def predict(file_name):
    # доступные классы
    # 'ground', 'tree', 'bush', 'tower', 'wire', 'copter', 'car', 'build'
    # для каких классов была обучена?
    channels = ['bush']

    # file_name - имя SVO папки, например: rec2018_07_21-6

    right_views_path = predict_path + "\\" + file_name + "\\right"
    right_measures_path = predict_path + "\\" + file_name + "\\right_measure"
    mask_path = predict_path + "\\" + file_name + "\\mask"

    if not os.path.exists(weights_path):
        print(f"Файл весов {weights_path} не существует!")
    else:
        frames_length = len(os.listdir(right_views_path))
        model = unet(len(channels), pretrained_weights = weights_path)
        testGene = testGenerator(right_views_path)
        for frame_number in range(frames_length):
            pred = []
            for _ in range(15):
                pred.append(next(testGene))
            results = model.predict_generator(iter(pred), 15, verbose=1)
            min_depth = analyze_bush_depth(results, right_measures_path, frame_number)
            #saveResult(mask_path, results, channels, frame_number)

if __name__ == "__main__":
    predict("rec2018_07_21-6")