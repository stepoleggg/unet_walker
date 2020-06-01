import numpy as np
import pyzed.sl as sl
import math 
from config import bush_treshold, predict_path, average_frame_size
from data import read_from_json
import matplotlib.pyplot as plt

def analyze_bush_depth(results, right_measure_path, frame_number):
    full_result = probs_to_full_result(results)
    sucsess, all_measures, time = read_measures(right_measure_path, frame_number)
    if not sucsess:
        return None, None, None, None
    not_bush_detected = full_result < bush_treshold
    all_measures[not_bush_detected] = math.inf
    min_measure = np.min(all_measures)
    if min_measure == math.inf:
        return None, time, None, None
    else:
        cords = np.argwhere(all_measures == min_measure)
        return min_measure, time, cords[0].tolist(), full_result[cords[0][0]][cords[0][1]]


def read_measures(measure_path: str, frame_number):
    try:
        # Получение данных
        json_data = read_from_json(f'{measure_path}\\{frame_number}.json')
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

def show_report(file_name):
    report = read_from_json(f'{predict_path}\\{file_name}\\report.json')
    distances = np.array(report['distances'])
    probabilities = np.array(report['probabilities'])
    distances_average_per_sec = []
    for i in range(len(distances)):
        av = np.average(distances[i:i+average_frame_size], weights=probabilities[i:i+average_frame_size])
        distances_average_per_sec.append(av)

    fig, ax = plt.subplots()

    plt.grid()
    ax.plot(report['timestamps'], distances)
    ax.plot(report['timestamps'], distances_average_per_sec)
    ax.set_title('Расстояние от вершин ДКР до Канатохода на протяжении участка записи')
    ax.legend(loc='upper left')
    ax.set_xlabel('Время, мc')
    ax.set_ylabel('Расстояние, м')
    ax.set_xlim(xmin=report['timestamps'][0], xmax=report['timestamps'][-1])

    manager = plt.get_current_fig_manager()
    manager.resize(*manager.window.maxsize())
    fig.tight_layout()
    fig.savefig(f'{predict_path}\\{file_name}\\plot.png')
    plt.show()

if __name__ == "__main__":
    show_report("rec2018_07_21-6")