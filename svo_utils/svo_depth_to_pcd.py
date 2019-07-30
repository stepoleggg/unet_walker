"""
Read svo file and create png depth and pcd point cloud
"""
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
    mat = sl.Mat()

    path = f'{filepath[0:-4]}/depth'

    if not os.path.exists(path):
        os.makedirs(path)
    
    print("Start to save depth")

    i=0
    while True:
        err = cam.grab(runtime)
        if err == sl.ERROR_CODE.SUCCESS:
            cam.retrieve_image(mat, sl.VIEW.VIEW_DEPTH)
            saving_image(mat, i, path)
        else:
            break
        i+=1
    print('Depth saved')

    d = saving_point_cloud(cam, path)

    cam.close()

    print(f'FINISHED, all result in dir {path}')

    return d
    
def saving_image(mat, i, filepath):
    """
    Saving depth as png image
    """
    img = sl.ERROR_CODE.ERROR_CODE_FAILURE

    while img != sl.ERROR_CODE.SUCCESS:
        filepath = f'{filepath}/{i}.png'
        img = mat.write(filepath)

        if img == sl.ERROR_CODE.SUCCESS:
            break


def saving_point_cloud(cam, filepath):
    """
    Saving point cloud as x y z rgb ascii pcd
    """
    filepath = f'{filepath[0:-6]}/{filepath[0:-6]}_point_cloud.pcd'
    print(filepath)
    sl.save_camera_point_cloud_as(cam,
                                    sl.POINT_CLOUD_FORMAT.
                                    POINT_CLOUD_FORMAT_PCD_ASCII,
                                    filepath, True)
    return filepath


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Please specify path to .svo file.")
        exit()
    main(sys.argv[1])