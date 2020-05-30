from svo_utils import svo_to_views_and_depths

def read_svo(path):
    svo_to_views_and_depths(path)

if __name__ == "__main__":
    import sys
    read_svo(sys.argv[1])