import os
import cv2
import numpy as np
from matplotlib import pyplot as plt



filename_sub_left = 'sim_flying_room_stereo/cam0/events.txt'
filename_sub_right = 'sim_flying_room_stereo/cam1/events.txt'

max_y = 180
max_x = 240
dis = 10
buffer_right = np.empty((180, 0)).tolist()
maximumTimeDifference = 0.0001
wmi = np.zeros((max_y, max_x, dis))
search_min = (np.zeros(180))


def addtoBufferRight(data):
    global buffer_right
    y = int(data[2])
    tmp = (data[0], int(data[1]),data[2], int(data[3]))
    buffer_right[y].append(tmp)


# Search in buffer_right[y], for x within disp_max
def searchEvent(data):
    timestamp = data[0]
    y_value = int(data[2])
    pol = int(data[3])
    foundEvents = []
    global search_min
    for x in range(int(search_min[y_value]),len(buffer_right[y_value])):
        # Step1: check if we#re looking at future events
        if timestamp < buffer_right[y_value][x][0]:
            break
        # Step2: check if time diff is within time_max, if not, start next search at this point to reduce runtime
        elif timestamp - buffer_right[y_value][x][0] > maximumTimeDifference:
            search_min[y_value] = int(x)
        # Step3: check disparity
        elif abs(data[1] - buffer_right[y_value][x][1]) > (dis - 1):
            continue
        # Step4: check if polarity is the same
        elif pol == buffer_right[y_value][x][3]:
            foundEvents.append(buffer_right[y_value][x])

    return foundEvents

def calculateMatchingCosts(timestampleft, timestampright, weightingfunction = 1):
    timediff = timestampleft-timestampright
    if weightingfunction == 1: #inverse linear
        #print(0.001-timediff)
        return 0.001-timediff
    elif weightingfunction == 2: #inverse quadratic
        a = 1
        weight = 1/(a*np.pow(timediff,2)+0.1)
        return weight
    elif weightingfunction == 3:
        mht = 10 #maximal considered hsitory events
        b = 1
        weight = mht * np.exp(-timediff/b)
        return weight
    else:
        return timediff

#load Events
events_left  = np.genfromtxt(fname=filename_sub_left, delimiter=' ', dtype=np.float, skip_header=0)[:]
events_right = np.genfromtxt(fname=filename_sub_right, delimiter=' ', dtype=np.float, skip_header=0)[:]
print("length of left cam data: ", len(events_left))

#write Events into Buffer
n = events_right.shape[0]
for i in range(n):
    addtoBufferRight(events_right[i,:])
n = events_left.shape[0]
for i in range(n):
    foundevents = searchEvent(events_left[i,:])

    # refresh weights
    #wmi = wmi - 0.1
    #wmia = wmi.clip(min=0)

    #look through all possible matches
    for j in range(len(foundevents)):
        costs = calculateMatchingCosts(events_left[i,0],foundevents[j][0])
        disparity = int(abs(events_left[i][1]-foundevents[j][1]))
        wmi[int(events_left[i][2]),int(events_left[i][1]),disparity-1] = costs

        #output of disparity map every 1000 events, refresh weighs
        if i % 1000 == 0:
            wmi = wmi - 0.00015
            wmi = wmi.clip(min=0)
        if i % 2000 == 0:
            ##average filtering on each disparity
            kernel = np.ones((2, 2), np.float32) / 4
            wmi_avg = np.zeros_like(wmi)
            for disp in range(10):
               wmi_avg[:, :, disp] = cv2.filter2D(wmi[:, :, disp], -1, kernel)
            ##looking for the maximum but only for the first 20 disoparity level
            disp = np.argmax(wmi_avg[:, :, :10], 2)
            plt.imshow(disp, cmap="gray")
            name = str(i) + "test.png"
            # plt.savefig(name)
            plt.show()


# Average filter on WMI on x-y plane
# kernel = np.ones((2,2),np.float32)/4
# wmi_avg = np.zeros_like(wmi)
# for d in range(dis):
#     wmi_avg[:, :, d] = cv2.filter2D(wmi[:, :, d], -1, kernel)

#plot disparity map
res = np.argmax(wmi, 2)
plt.imshow(res, cmap = "gray")
plt.show()








