
import pyzed.sl as sl
import os

def main(filepath):

    print("Reading SVO file: {0}".format(filepath))

    init = sl.InitParameters(svo_input_filename=filepath, svo_real_time_mode=False)
    cam = sl.Camera()
    status = cam.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit()

    runtime = sl.RuntimeParameters()
    left = sl.Mat()
    right = sl.Mat()

    if not os.path.exists(f'{filepath[0:-4]}/left'):
        os.makedirs(f'{filepath[0:-4]}/left')
    if not os.path.exists(f'{filepath[0:-4]}/right'):
        os.makedirs(f'{filepath[0:-4]}/right')
    i = 0
    while True:
        err = cam.grab(runtime)
        if err == sl.ERROR_CODE.SUCCESS:
            cam.retrieve_image(left, sl.VIEW.VIEW_LEFT)
            #cam.retrieve_image(right, sl.VIEW.VIEW_RIGHT)
            left.write(f'{filepath[0:-4]}/left/{i}.png')
            #right.write(f'{filepath[0:-4]}/right/{i}.png')
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