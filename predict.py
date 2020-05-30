from model import unet
from data import testGenerator, saveResult
from analyzer import analyze_depth
from config import weights_path, predict_path
from pathlib import PurePath
import os

def predict(filepath):
    # доступные классы
    # 'ground', 'tree', 'bush', 'tower', 'wire', 'copter', 'car', 'build'
    # для каких классов была обучена?
    channels = ['bush']

    file_name = PurePath(filepath).name[0:-4]
    right_views_path = predict_path + "\\" + file_name + "\\right"
    right_depths_path = predict_path + "\\" + file_name + "\\right_depth"
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
            analyze_depth(results, frame_number, right_depths_path)
            saveResult(mask_path, results, channels, frame_number)

if __name__ == "__main__":
    predict(input("Введите путь к папке с изображениями и глубинами:"))