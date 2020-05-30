from config import data_dir
import pyzed.sl as sl
import os
from pathlib import PurePath

def main(filepath):

    print("Reading SVO file: {0} for views and depths".format(filepath))

    init = sl.InitParameters()
    init.set_from_svo_file(filepath)
    init.svo_real_time_mode = False  # Don't convert in realtime
    init.enable_right_side_measure = True
    cam = sl.Camera()
    status = cam.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit()

    runtime = sl.RuntimeParameters()
    right = sl.Mat()
    right_depth = sl.Mat()

    file_name = PurePath(filepath).name[0:-4]
    filepath = data_dir + "\\" + file_name

    if not os.path.exists(f'{filepath}\\right'):
        os.makedirs(f'{filepath}\\right')
    if not os.path.exists(f'{filepath}\\right_depth'):
        os.makedirs(f'{filepath}\\right_depth')
    i = 0
    while True:
        err = cam.grab(runtime)
        if err == sl.ERROR_CODE.SUCCESS:
            cam.retrieve_image(right, sl.VIEW.RIGHT)
            cam.retrieve_image(right_depth, sl.VIEW.DEPTH_RIGHT)
            right.write(f'{filepath}\\right\\{i}.png')
            right_depth.write(f'{filepath}\\right_depth\\{i}.png')
        else:
            print(repr(err))
            break
        i+=1

    cam.close()
    print("Views and depths saved")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Please specify path to .svo file.")
        exit()
    main(sys.argv[1])