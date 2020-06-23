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

def create_Buffer(x_list,y_list,t_list,p_list):
    buffer=[]
    for i in range(180):
        buffer.append([None])
    for i, y in enumerate(y_list):
        # print(buffer[y][0])
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

# %%
