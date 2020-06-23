import os
# import cv2
import numpy as np
from matplotlib import pyplot as plt

# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

def extract_data(filename):
    infile = open(filename, 'r')
    timestamp = []
    x = []
    y = []
    pol = []
    for line in infile:
        words = line.split()
        # words[0]: t, words[1]: x
        timestamp.append(float(words[0]))
        x.append(int(words[1]))
        y.append(int(words[2]))
        pol.append(int(words[3]))
    infile.close()
    return timestamp, x, y, pol

filename_sub_left = 'sim_flying_room_stereo/cam0/events.txt'
filename_sub_right = 'sim_flying_room_stereo/cam1/events.txt'

timestamp_l, x_l, y_l, pol_l = extract_data(filename_sub_left)
timestamp_r, x_r, y_r, pol_R = extract_data(filename_sub_right)