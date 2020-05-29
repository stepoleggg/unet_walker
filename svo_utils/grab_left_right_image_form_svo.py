from config import data_dir
import pyzed.sl as sl
import os
from pathlib import PurePath

def main(filepath):

    print("Reading SVO file: {0}".format(filepath))
    file_name = PurePath(filepath).name[0:-4]
    filepath = data_dir + "\\" + file_name

    #init = sl.InitParameters(svo_input_filename=filepath, svo_real_time_mode=False)
    init = sl.InitParameters()
    init.set_from_svo_file(filepath)
    init.svo_real_time_mode = False  # Don't convert in realtime
    cam = sl.Camera()
    status = cam.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit()

    runtime = sl.RuntimeParameters()
    left = sl.Mat()
    right = sl.Mat()

    if not os.path.exists(f'{filepath}\\left'):
        os.makedirs(f'{filepath}\\left')
    if not os.path.exists(f'{filepath}\\right'):
        os.makedirs(f'{filepath}\\right')
    i = 0
    while True:
        err = cam.grab(runtime)
        if err == sl.ERROR_CODE.SUCCESS:
            cam.retrieve_image(left, sl.VIEW.LEFT)
            cam.retrieve_image(right, sl.VIEW.RIGHT)
            left.write(f'{filepath}\\left\\{i}.png')
            right.write(f'{filepath}\\right\\{i}.png')
        else:
            print(repr(err))
            break
        i+=1

    cam.close()
    print("\nFINISH")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Please specify path to .svo file.")
        exit()
    main(sys.argv[1])