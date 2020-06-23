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







# %% Plot
# img_size = (180,240)

# # Brightness incremet image (Balance of event polarities)
# img = np.zeros(img_size, np.int)
# num_events = 2350000
# print("numevents = ", num_events)
# for i in range(num_events):
#     #timestamp[i]
#     img[y0[i],x1[i]] += (2*p1[i]-1)

# fig = plt.figure()
# fig.suptitle('Balance of event polarities')
# #plt.imshow(img, cmap='gray')
# maxabsval = np.amax(np.abs(img))
# plt.imshow(img, cmap='seismic_r', clim=(-maxabsval,maxabsval))
# plt.colorbar()
# plt.show()