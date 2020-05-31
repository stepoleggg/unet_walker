from data import read_measure
import numpy as np

def analyze_depth(results, frame_number, right_measure_path):
    measure = read_measure(right_measure_path, frame_number)
    print(measure)

#analyze_depth("", 1, "data\\predict\\rec2018_07_21-6\\right_measure")