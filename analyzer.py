import numpy as np
import pyzed.sl as sl
import codecs, json 
from config import bush_treshold

def analyze_bush_depth(results, right_measure_path, frame_number) -> float:
    full_result = probs_to_full_result(results)
    all_measures = read_measures(right_measure_path, frame_number)
    not_bush_detected = full_result < bush_treshold
    all_measures[not_bush_detected] = 1000000
    return np.min(all_measures)


def read_measures(measure_path: str, frame_number):
    data = codecs.open(f'{measure_path}\\{frame_number}.json', 'r', encoding='utf-8').read() 
    data = np.array(json.loads(data))
    data[np.isnan(data)] = 1000000
    return data

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

#analyze_depth("", 1, "data\\predict\\rec2018_07_21-6\\right_measure")