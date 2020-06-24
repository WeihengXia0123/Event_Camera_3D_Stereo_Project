# %%-*- coding: utf-8 -*-
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import


# %% Read a file of events and write another file with a subset of them
camera_left = 'data/cam0/events.txt'
camera_right = 'data/cam1/events.txt'

height = 180
width = 240
disp_max = 10
time_max = 0.01
# %% Read file with a subset of events
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
    return timestamp,x,y,pol
    
t0, x0, y0, p0 = extract_data(camera_left)
t1, x1, y1, p1 = extract_data(camera_right)

# def load_data(filename):
#     lines = np.loadtxt(camera_left, dtype=(float))
#     ts = lines[:,0]
#     x = lines[:,1]
#     y = lines[:,2]
#     p = lines[:,3]
    
#     return ts,x,y,p

# t0,x0,y0,p0 = load_data(camera_left)
# t1,x1,y1,p1 = load_data(camera_right)

# %%Remapping of spike to [-1,+1]
for i in range(len(p0)):
    if(p0[i] == 0):
        p0[i] = -1
    else:
        p0[i] = 1
        
for i in range(len(p1)):
    if(p1[i] == 0):
        p1[i] = -1
    else:
        p1[i] = 1

# %%Check data length
print(len(t0))
print(len(t1))

print(np.amin(p0)) # check if polarity is -1, +1
print(np.amin(p1))

# %% Create a buffer for events
class item:
    def __init__(self,x,t,p):
        self.x = x
        self.t = t
        self.p = p

def create_Buffer(x_list, y_list, t_list, p_list):
    buffer=[]
    for i in range(180):
        buffer.append([None])
        
    for i, y in enumerate(y_list):
        if buffer[y][0] == None:
            buffer[y][0] = item(x_list[i], t_list[i], p_list[i])
        else:
            buffer[y].append(item(x_list[i], t_list[i], p_list[i]))
            
    print("data length: ", i+1)
    return buffer

buffer_left = create_Buffer(x0,y0,t0,p0)
buffer_right = create_Buffer(x1,y1,t1,p1)

print("buffer_left height: ", len(buffer_left))
print("buffer_left[y0] size: ", len(buffer_left[0]))

print("buffer_right height: ", len(buffer_right))
print("buffer_right[y0] size: ", len(buffer_right[0]))

# %% Matching: search events
def search_events(t,x,y,p):
    global buffer_right
    found_events = []
    
    # Search in buffer_right[y], for x within disp_max
    for i in range(len(buffer_right[y])):
        # Step1: check if past events
        if(buffer_right[y][i].t > t):
            # print("break")
            break; # since buffer is sorted in t
        # Step2: check if time diff is within time_max
        if((t-buffer_right[y][i].t) > time_max):
            continue;
        # Step3: check if same polarity
        if(buffer_right[y][i].p == p):
            # Step4: check if it's within disparity range
            if(abs(buffer_right[y][i].x-x) <= disp_max):
                found_events.append(buffer_right[y][i])
    # if(len(found_events)!=0):
        # print("Found events count: ", len(found_events))
    return found_events

# found_events = search_events(t0[7000],x0[7000],y0[7000],p0[7000])
# print(len(found_events))

# %% Weighting: insert WMI
wmi = np.zeros((height, width, disp_max))

def calculateMatchingCosts(timestampleft, timestampright, weightingfunction = 1):
    timediff = timestampleft-timestampright
    if weightingfunction == 1: #inverse linear
        # print(time_max-timediff)
        return time_max-timediff
    
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

def insertWMI(t,x,y,p):
    global wmi
    
    # Step1: Search for events
    found_events = search_events(t,x,y,p)
    # print("len ", len(found_events))
    for i in range(len(found_events)):
        # Step2: Calculate Matching Cost
        weight = calculateMatchingCosts(t, found_events[i].t, 1)
        # Step3: Insert into WMI
        disp = abs(x-found_events[i].x)
        wmi[int(y), int(x), disp-1] = weight

# %% Main loop
# loop through all left camera events
disp_map = []

for i in range(len(t0)):
    # Step0: update WMI
    insertWMI(t0[i], x0[i], y0[i],p0[i])
    
    if i%5000 == 0:
        # Step1: weight decay
        wmi = wmi*0.7
        
        # Step2: clean weights under threshold
        #wmi[wmi<threhold] = 0
            
        # Step3: apply an average filter on WMI on x-y plane
        kernel = np.ones((5,5),np.float32)/25
        for disp_value in range(disp_max):
            wmi[:,:,disp_value] = cv2.filter2D(wmi[:,:,disp_value],-1,kernel)
            # wmi_avg[disp_] = cv2.filter2D(wmi[:,:,disp_],-1,kernel)
        
        # Step4: find maxima
        disp_map = np.amax(wmi, axis=2)
        plt.imshow(disp_map, cmap = "gist_gray")
        plt.show()
        
# insertWMI(t0[7000], x0[7000], y0[7000],p0[7000])
# disp_map = np.amax(wmi, axis=2)
# plt.imshow(disp_map, cmap = "gist_gray")
# plt.show()

disp = np.argmax(wmi,2)
print(np.amax(wmi))
print(np.amin(wmi))
print(disp.shape)
print(disp)
    
# %%
# a = np.zeros((2,3,4))
# a[0,0,0] = 5
# a[0,1,0] = 8
# a[0,2,0] = 6
# print(a)
# print(np.amax(a, axis=1))

    
