import numpy as np
import pyzed.sl as sl
import math 
from config import bush_treshold, predict_path, average_frame_size, lap_height, max_d_on_table, max_bush_height
from data import read_from_json
import matplotlib.pyplot as plt
from matplotlib import gridspec
import datetime
from fpdf import FPDF
import os
from PyPDF2 import PdfFileMerger

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
    # получение данных
    report = read_from_json(f'{predict_path}\\{file_name}\\report.json')
    distances = np.array(report['distances'])
    probabilities = np.array(report['probabilities'])
    timestamps = np.array(report['timestamps'])

    if not os.path.exists(f'{predict_path}\\{file_name}\\temp'):
        os.makedirs(f'{predict_path}\\{file_name}\\temp')

    # титульный лист
    value = datetime.date.fromtimestamp(timestamps[0]/1000)
    record_date_str = value.strftime('%d.%m.%Y')
    pdf = FPDF()
    pdf.add_font('times-new-roman', '', 'fonts\\times-new-roman.ttf', uni = True)
    pdf.add_font('times-new-roman-bold', '', 'fonts\\times-new-roman-bold.ttf', uni = True)
    pdf.add_page()
    pdf.set_font("times-new-roman", size=18)
    pdf.cell(200, 50, txt="", ln = 1, align="C")
    pdf.set_font("times-new-roman-bold", size=20)
    pdf.cell(200, 10, txt="ОТЧЁТ", ln=1, align="C")
    pdf.set_font("times-new-roman", size=16)
    pdf.cell(200, 10, txt="О высоте древесно-кустарной растительности", ln=1, align="C")
    pdf.cell(200, 10, txt="под линией электропередач", ln=1, align="C")
    pdf.cell(200, 50, txt="", ln=1, align="C")
    pdf.cell(200, 10, txt="Участок: _______________", ln=1, align="C")
    pdf.cell(200, 10, txt=f"Дата измерений: {record_date_str}", ln=1, align="C")
    pdf.cell(200, 50, txt="", ln=1, align="C")
    pdf.set_font("times-new-roman", size=14)
    pdf.cell(150, 20, txt=f"Исполнитель: ", ln=1, align="R")
    pdf.cell(150, 20, txt=f"Заказчик: ", ln=1, align="R")
    pdf.cell(200, 15, txt="", ln=1, align="C")
    pdf.cell(200, 10, txt=f"Екатеринбург, {datetime.datetime.now().year}", ln=1, align="C")
    pdf.output(f'{predict_path}\\{file_name}\\temp\\title.pdf')

    # расчет средней величины расстояния среди average_frame_size подряд идущих значений
    remove_values = len(distances) % average_frame_size
    distances_average_per_sec = np.average(distances[:-remove_values].reshape(-1, average_frame_size), 
        weights=probabilities[:-remove_values].reshape(-1, average_frame_size), axis=1)
    timestamps = timestamps[:-remove_values:average_frame_size] / 1000

    # cохранение графика
    fig, ax = plt.subplots()
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
    min_dist = np.zeros(len(distances_average_per_sec))
    min_dist[:] = lap_height - max_bush_height
    ax.plot(timestamps, distances_average_per_sec)
    ax.plot(timestamps, min_dist)
    ax.set_title('Расстояние от вершин ДКР до Канатохода на протяжении участка записи')
    ax.legend(['Расстояние', f'Минимально допустимое расстояние при высоте ЛЭП {lap_height} м'], loc='upper left')
    ax.set_xlabel('Время, с')
    ax.set_ylabel('Расстояние, м')
    ax.set_xlim(xmin=timestamps[0], xmax=timestamps[-1])

    manager = plt.get_current_fig_manager()
    manager.resize(*manager.window.maxsize())
    fig.tight_layout()
    fig.savefig(f'{predict_path}\\{file_name}\\temp\\plot.pdf',
            dpi=300,
            orientation='album')

    pdfs = [f'{predict_path}\\{file_name}\\temp\\title.pdf', f'{predict_path}\\{file_name}\\temp\\plot.pdf']

    # сохранение таблиц с данными
    tables_n = len(timestamps) // max_d_on_table
    if tables_n * max_d_on_table < len(timestamps):
        tables_n += 1
    if tables_n == 0:
        pdfs.append(f'{predict_path}\\{file_name}\\temp\\0.pdf')
        save_table_n(file_name, timestamps, distances_average_per_sec, 0)
    for i in range(tables_n):
        pdfs.append(f'{predict_path}\\{file_name}\\temp\\{i}.pdf')
        if i == tables_n - 1:
            save_table_n(file_name, timestamps[i*max_d_on_table:], distances_average_per_sec[i*max_d_on_table:], i)
        else:
            save_table_n(file_name, timestamps[i*max_d_on_table:(i+1)*max_d_on_table], distances_average_per_sec[i*max_d_on_table:(i+1)*max_d_on_table], i)

    # сохранение изображений с высокой ДКР
    pdf = FPDF()
    pdf.add_font('times-new-roman', '', 'fonts\\times-new-roman.ttf', uni = True)
    pdf.add_font('times-new-roman-bold', '', 'fonts\\times-new-roman-bold.ttf', uni = True)
    pdf.add_page()
    pdf.set_font("times-new-roman-bold", size=16)
    pdf.cell(200, 10, txt="Точки с наиболее высокой растительностью", ln=1, align="C")

    #pdf.add_page()
    #pdf.image(image,x,y,w,h)

    merger = PdfFileMerger()
    for pdf in pdfs:
        merger.append(pdf)
    merger.write(f'{predict_path}\\{file_name}\\report.pdf')
    merger.close()

def save_table_n(file_name, timestamps, distances, n):
    # таблица
    fig, ax = plt.subplots()
    fig_width_cm = 21                                # A4 page
    fig_height_cm = 29.7
    inches_per_cm = 1 / 2.54                         # Convert cm to inches
    fig_width = fig_width_cm * inches_per_cm         # width in inches
    fig_height = fig_height_cm * inches_per_cm       # height in inches
    fig_size = [fig_width, fig_height]
    plt.rc('text', usetex=False) # so that LaTeX is not needed when creating a PDF with PdfPages later on
    fig.set_size_inches(fig_size)
    fig.set_facecolor('#9999ff')
    gs = gridspec.GridSpec(29, 21, wspace=0.1, hspace=0.1)  
    table_data = []
    colors = []
    for i in range(len(timestamps)):
        value = datetime.datetime.fromtimestamp(timestamps[i])
        time_str = value.strftime('%H:%M:%S')
        bush_height = round(float(lap_height) - float(distances[i]), 2)
        if bush_height < 0:
            bush_height = 0
        if bush_height > max_bush_height:
            colors.append(["w", "w", "w", "red"])
        elif bush_height > max_bush_height * 0.8:
            colors.append(["w", "w", "w", "yellow"])
        else:
            colors.append(["w", "w", "w", "w"])
        table_data.append([n*max_d_on_table + 1 + i, time_str, round(distances[i], 2), bush_height])
    table = ax.table(cellText=table_data, loc='center', colLabels=['№ Измерения', 'Время записи', 'Рассттояние ЛЭП-ДКР, м', 'Высота ДКР, м'], cellColours = colors)
    table.set_fontsize(14)
    table.scale(1,2)
    ax.axis('off')    
    fig.savefig(f'{predict_path}\\{file_name}\\temp\\{n}.pdf',
            dpi=300,
            orientation='portrait')

if __name__ == "__main__":
    render_report("rec2018_07_21-8")