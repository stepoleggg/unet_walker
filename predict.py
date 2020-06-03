from model import unet
from data import testGenerator, saveResult
from analyzer import analyze_bush_depth
from config import weights_path, predict_path
from pathlib import PurePath
from data import save_to_json
import os

def predict(file_name, callback = None):
    # доступные классы
    # 'ground', 'tree', 'bush', 'tower', 'wire', 'copter', 'car', 'build'
    # для каких классов была обучена?
    channels = ['bush']

    # file_name - имя SVO папки, например: rec2018_07_21-6
    root_path = predict_path + "\\" + file_name
    right_views_path = root_path + "\\right"
    right_views_marked_path = root_path + "\\right_marked"
    right_measures_path = root_path + "\\right_measure"
    mask_path = root_path + "\\mask"
    analyzed_result_path = root_path + "\\report.json"

    distances = []
    timestamps = []
    frame_numbers = []
    coordinates = []
    probabilities = []

    if not os.path.exists(weights_path):
        print(f"Файл весов {weights_path} не существует!")
    if not os.path.exists(right_views_marked_path):
        os.makedirs(right_views_marked_path)
    if not os.path.exists(right_measures_path):
        os.makedirs(right_measures_path)
    if not os.path.exists(mask_path):
        os.makedirs(mask_path)

    else:
        frames_length = len(os.listdir(right_views_path))
        model = unet(len(channels), pretrained_weights = weights_path)
        testGene = testGenerator(right_views_path)
        proc, dif = float(frames_length) / 10
        for frame_number in range(frames_length):
            pred = []
            if callback is not None:
                callback.emit(f"Файлов обработано {frame_number}")
            for _ in range(15):
                pred.append(next(testGene))
            results = model.predict_generator(iter(pred), 15, verbose=1)
            # расчет минимальной дистанции до ДКР, получение времени съемки, координат наиболее близкого пикселя 
            min_depth, time_milliseconds, coordinate, probability = analyze_bush_depth(results, right_measures_path, frame_number)
            # запись результирующих данных
            distances.append(min_depth)
            timestamps.append(time_milliseconds)
            frame_numbers.append(frame_number)
            coordinates.append(coordinate)
            probabilities.append(probability)
            print(f'{frame_number+1}/{frames_length} completed')
            if callback:
                if float(frame_number)/frames_length >= proc:
                    proc += dif
                    callback.emit(f"{int(proc)*100}% готово")
            # сохранение распознанного и помеченного кадров
            saveResult(mask_path, results, channels, frame_number, coordinate, right_views_path, right_views_marked_path)
        # сохранение результатов анализа
        analyzed_data = {'distances': distances, 'timestamps': timestamps, 'frame_numbers': frame_numbers, 'coordinates': coordinates, 'probabilities': probabilities}
        save_to_json(analyzed_data, analyzed_result_path)
    return "ok"    

if __name__ == "__main__":
    predict("rec2018_07_21-8")