import cv2
import numpy as np
from matplotlib import pyplot as plt
from CameraBuffer import CameraBuffer
from OutputController import OutputController

filename_sub_left = 'data/berlinale/cam0/events.txt'
filename_sub_right = 'data/berlinale/cam1/events.txt'
#filename_sub_left = 'sim_flying_room_stereo\cam0\events.txt'
#filename_sub_right = 'sim_flying_room_stereo\cam1\events.txt'
max_y = 180
max_x = 240
max_disparity = 240
time_resolution = 0.000000001
maximum_timeslot = 10
a = CameraBuffer(max_x,max_y,filename_sub_left,filename_sub_right,max_disparity, time_resolution)
a.prepareData()
b = OutputController(max_x, max_y, max_disparity, time_resolution, maximum_timeslot, a)
b.evaluateAll()

