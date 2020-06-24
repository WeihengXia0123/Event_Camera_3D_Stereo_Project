import os
import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import convolve
# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
from scipy.ndimage import gaussian_filter
from scipy import ndimage
import cv2

filename_sub_left = 'sim_flying_room_stereo/cam0/events.txt'
filename_sub_right = 'sim_flying_room_stereo/cam1/events.txt'

max_x = 180
max_y =  240
buffer_right = np.empty((max_x, 0)).tolist()

maximumTimeDifference = 0.00005
wmi = np.zeros((max_x,max_y,240))
search_min = (np.zeros(240))

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
    for value in range(int(search_min[y_value]),len(buffer_right[y_value])):

        # Step1: check if we#re looking at future events
        if timestamp < buffer_right[y_value][value][0]:
            break
        # Step2: check if time diff is within time_max if not, start next search at this point to reduce runtime
        elif timestamp - buffer_right[y_value][value][0] > maximumTimeDifference:
            search_min[y_value] = int(value)

        ## Step3: check if same polarity and within the timedifference , disparity check is later
        elif pol == buffer_right[y_value][value][3] and timestamp - buffer_right[y_value][value][0] < maximumTimeDifference:
            foundEvents.append(buffer_right[y_value][value])
        else:
            continue
    return foundEvents

def calculateMatchingCosts(timestampleft, timestampright, weightingfunction = 1):
    timediff = timestampleft-timestampright
    if weightingfunction == 1: #inverse linear
        return timediff
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



#load Events from txt
events_left = np.genfromtxt(fname=filename_sub_left, delimiter=' ', dtype=np.float, skip_header=0)[:]
events_right =np.genfromtxt(fname=filename_sub_right, delimiter=' ', dtype=np.float, skip_header=0)[:]


#write Events into Buffer (datastructure list in a list, on list fpr each y-coordinate
for i in range(events_right.shape[0]):
    addtoBufferRight(events_right[i,:])

for i in range(events_left.shape[0]):
    #serch for events
    foundevents = []
    foundevents = searchEvent(events_left[i,:])

    #refresh weights
    #wmi = wmi - 1
    #wmi = wmi.clip(min=0)

    #look through all possible matches
    if not len(foundevents) == 0:
        for j in range(len(foundevents)):
            #calculate Matchingcosts and disparity
            costs = calculateMatchingCosts(events_left[i,0],foundevents[j][0])*10000
            disparity = int(abs(events_left[i][1]-foundevents[j][1]))
            #write into wmi
            wmi[int(events_left[i][2]),int(events_left[i][1]),disparity] = costs

        #every 1000? events refresh the weights and clip to zero, so no value under zero
        if i%1000 == 0:
            print("aaaaaaaaa")
            wmi = wmi-0.05
            wmi = wmi.clip(min=0)

            #average filtering on each disparity
            kernel = np.ones((5, 5), np.float32) / 25
            wmi_avg = np.zeros_like(wmi)
            for disp in range(240):
                wmi_avg[:, :, disp] = cv2.filter2D(wmi[:,:,disp],-1,kernel)
            #looking for the maximum but only for the first 20 disoparity level
            disp = np.argmax(wmi_avg[:,:,:20], 2)
            plt.imshow(disp, cmap = "gray")
            plt.show()

#tmp = gaussian_filter(wmi[:,:,:50], sigma=1)

#last wmi aggregation
kernel = np.ones((5,5),np.float32)/25

# Step3: apply an average filter on WMI on x-y plane
# kernel = np.ones((5,5),np.float32)/25
wmi_avg = np.zeros_like(wmi)
for disp in range(240):
    wmi_avg[:, :, disp] = cv2.filter2D(wmi[:, :, disp], -1, kernel)

disp = np.argmax(wmi_avg[:,:,:20],2)
plt.imshow(disp, cmap = "gray")
plt.show()







