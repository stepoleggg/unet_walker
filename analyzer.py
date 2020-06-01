import numpy as np
import pyzed.sl as sl
import codecs, json
import math 
from config import bush_treshold

def analyze_bush_depth(results, right_measure_path, frame_number) -> float:
    full_result = probs_to_full_result(results)
    sucsess, all_measures, time = read_measures(right_measure_path, frame_number)
    if not sucsess:
        return None, None
    not_bush_detected = full_result < bush_treshold
    all_measures[not_bush_detected] = math.inf
    min_measure = np.min(all_measures)
    if min_measure == math.inf:
        return None, time
    else:
        return min_measure, time


def read_measures(measure_path: str, frame_number):
    data = codecs.open(f'{measure_path}\\{frame_number}.json', 'r', encoding='utf-8').read() 
    try:
        # Получение данных
        json_data = json.loads(data)
        print("ok")
        measures_data = np.array(json_data['measures'])
        time_data = json_data['time']
        # Замена значений -Infinite, NaN на Infinite
        infinite_data = np.isfinite(measures_data)
        np.bitwise_not(infinite_data, out=infinite_data)
        measures_data[infinite_data] = math.inf
        return True, measures_data, time_data
    except:
        print(f'Ошибка парсинга json: {measure_path}\\{frame_number}.json')
        return False, None, None

def probs_to_full_result(imgs: list) -> np.ndarray:
    """
    Собирает изображение из прямоугольников (256,256,1), на вход подается list прямоугольников
    Проход идет слева на право
    """
    new_image = np.zeros((720, 1280,))
    k = 0
    for i in range(0,3):
        for j in range(0,5):
            img = imgs[k]
            if i==2:
                new_image[i*256-48:(i+1)*256-48,j*256:(j+1)*256] = img[:,:,0]
            else:
                new_image[i*256:(i+1)*256,j*256:(j+1)*256] = img[:,:,0]
            k+=1
    return new_image