from svo_utils import grab_left_right_image_form_svo, pcl_viewer, svo_depth_to_pcd

def read_svo(path):
    grab_left_right_image_form_svo(path)
    d = svo_depth_to_pcd(path)
    
    print('View pcd file? [y/n]')
    user_cmd = input()
    if user_cmd == 'y':
        pcl_viewer(d)

if __name__ == "__main__":
    import sys
    read_svo(sys.argv[1])