import numpy as np
import pyzed.sl as sl
import math 
from config import bush_treshold, predict_path, average_frame_size
from data import read_from_json
import matplotlib.pyplot as plt
from matplotlib import gridspec
import datetime
from fpdf import FPDF

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

def render_report(file_name):
    report = read_from_json(f'{predict_path}\\{file_name}\\report.json')
    distances = np.array(report['distances'])
    probabilities = np.array(report['probabilities'])
    timestamps = np.array(report['timestamps'])
    remove_values = len(distances) % average_frame_size

    # считаем среднюю величину расстояния среди average_frame_size подряд идущих значений
    distances_average_per_sec = np.average(distances[:-remove_values].reshape(-1, average_frame_size), 
        weights=probabilities[:-remove_values].reshape(-1, average_frame_size), axis=1)
    timestamps = timestamps[:-remove_values:average_frame_size] / 1000

    fig, ax = plt.subplots()

    # A4 canvas
    fig_width_cm = 29.7                                # A4 page
    fig_height_cm = 21
    inches_per_cm = 1 / 2.54                         # Convert cm to inches
    fig_width = fig_width_cm * inches_per_cm         # width in inches
    fig_height = fig_height_cm * inches_per_cm       # height in inches
    fig_size = [fig_width, fig_height]

    plt.rc('text', usetex=False) # so that LaTeX is not needed when creating a PDF with PdfPages later on
    fig.set_size_inches(fig_size)
    fig.set_facecolor('#9999ff')
    gs = gridspec.GridSpec(29, 21, wspace=0.1, hspace=0.1)  

    plt.grid()
    ax.plot(timestamps, distances_average_per_sec)
    ax.set_title('Расстояние от вершин ДКР до Канатохода на протяжении участка записи')
    ax.legend(loc='upper left')
    ax.set_xlabel('Время, мc')
    ax.set_ylabel('Расстояние, м')
    ax.set_xlim(xmin=timestamps[0], xmax=timestamps[-1])

    manager = plt.get_current_fig_manager()
    manager.resize(*manager.window.maxsize())
    fig.tight_layout()
    fig.savefig(f'{predict_path}\\{file_name}\\plot.pdf',
            dpi=300,
            orientation='album')
    #plt.show()

    #timestamp = 1339521878.04
    #value = 
    value = datetime.date.fromtimestamp(timestamps[0])
    record_date_str = value.strftime('%d.%m.%Y')
    pdf = FPDF()
    #pdf.add_font('times-new-roman.ttf', uni = True)
    pdf.add_page()
    pdf.set_font("times", size=18)
    pdf.cell(200, 10, txt="Title", ln=1, align="C")
    pdf.set_font("times", size=14)
    pdf.cell(200, 10, txt=record_date_str, ln=1, align="C")
    pdf.output(f'{predict_path}\\{file_name}\\title.pdf')

if __name__ == "__main__":
    render_report("rec2018_07_21-8")