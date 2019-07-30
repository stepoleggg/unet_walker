"""
vizualize pcd file
"""
import numpy as np
import open3d as o3d

def main(filepath):

    print("Reading PCD file: {0}".format(filepath))
    print("Load a pcd point cloud, print it, and render it")
    pcd = o3d.io.read_point_cloud(filepath)
    o3d.visualization.draw_geometries([pcd])

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Please specify path to .pcd file.")
        exit()
    main(sys.argv[1])