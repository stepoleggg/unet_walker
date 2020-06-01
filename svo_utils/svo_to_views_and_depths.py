from config import data_dir
import pyzed.sl as sl
import os
from pathlib import PurePath
from data import save_to_json

def main(filepath, callback = None):

    if callback:
        callback.emit("Reading SVO file: {0} for views and depths".format(filepath))
    print("Reading SVO file: {0} for views and depths".format(filepath))

    init = sl.InitParameters()
    init.set_from_svo_file(filepath)
    init.svo_real_time_mode = False  # Don't convert in realtime
    init.enable_right_side_measure = True
    init.coordinate_units = sl.UNIT.METER # Измерения в метрах

    cam = sl.Camera()
    status = cam.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit()

    runtime = sl.RuntimeParameters()

    right = sl.Mat()
    right_measure = sl.Mat()

    file_name = PurePath(filepath).name[0:-4]
    print(filepath)
    print(file_name)
    filepath = data_dir + "\\" + file_name

    if not os.path.exists(f'{filepath}\\right'):
        os.makedirs(f'{filepath}\\right')
    if not os.path.exists(f'{filepath}\\right_measure'):
        os.makedirs(f'{filepath}\\right_measure')
    i = 0
    while True:
        err = cam.grab(runtime)
        if err == sl.ERROR_CODE.SUCCESS:
            # Правое изображение
            cam.retrieve_image(right, sl.VIEW.RIGHT)
            # Правая глубина
            cam.retrieve_measure(right_measure, sl.MEASURE.DEPTH_RIGHT)
            # Время
            time = cam.get_timestamp(sl.TIME_REFERENCE.IMAGE)
            # Сохранение изображения
            right.write(f'{filepath}\\right\\{i}.png')
            # Сохранение измерений глубины и времени
            data = {'time': time.get_milliseconds(), 'measures': right_measure.get_data().tolist()}
            save_to_json(data, f'{filepath}\\right_measure\\{i}.json')
        else:
            print(repr(err))
            break
        i+=1

    cam.close()
    if callback:
        callback.emit("Views and depths saved")
    print("Views and depths saved")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Please specify path to .svo file.")
        exit()
    main(sys.argv[1])