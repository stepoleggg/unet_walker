from svo_utils import svo_to_views_and_depths

def read_svo(path, callback = None):
    svo_to_views_and_depths(path, callback)
    return "ok"

if __name__ == "__main__":
    import sys
    read_svo(sys.argv[1])