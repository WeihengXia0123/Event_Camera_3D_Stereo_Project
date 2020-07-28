from src.CameraBuffer import CameraBuffer
from src.OutputController import OutputController
import os

# filename_sub_left = 'berlinale/cam0/events.txt'
# filename_sub_right = 'berlinale/cam1/events.txt'
filename_sub_left = 'sim_flying_room_stereo/cam0/events.txt'
filename_sub_right = 'sim_flying_room_stereo/cam1/events.txt'

max_y = 180
max_x = 240
max_disparity = 30
time_resolution = 0.0001
maximum_timeslot = 1000
save_path = "result_drone_2/"
if not os.path.exists(save_path):
        os.makedirs(save_path)

a = CameraBuffer(max_x,max_y,filename_sub_left,filename_sub_right,max_disparity, time_resolution)
a.prepareData()
if False:
    print("Right Buffer y-value = 0: {} ....".format(a.rightBuffer[0][:5]))
    print("Right Buffer y-value = 1: {} ...".format(a.rightBuffer[1][:5]))
    print("Right Buffer y-value = 2: {} ...".format(a.rightBuffer[2][:5]))
b = OutputController(max_x, max_y, max_disparity, time_resolution, maximum_timeslot, a)
b.evaluateAll()

