import numpy as np
from CameraBuffer import CameraBuffer
from scipy import signal
from Util import *
from matplotlib import pyplot as plt
import cv2
import bisect


class OutputController(object):
    def __init__(self, maxX, maxY, max_disp, timeRes, maxTimeSlot, cameraBuffer: CameraBuffer):
        self.maxX = maxX
        self.maxY = maxY
        self.max_disp = max_disp
        self.timeResolution = timeRes
        self.cameraBuffer = cameraBuffer
        self.maxTimeSlot = maxTimeSlot
        self.WMI = np.zeros((maxY, maxX, max_disp))
        self.output = cv2.VideoWriter("output.avi",  cv2.VideoWriter_fourcc(*'DIVX'), 5, (maxX, maxY))


    def refreshWMI(self, referenceEvent, candidateEvent: list):
        #print("event from the left Buffer: {}".format(referenceEvent))
        for e in candidateEvent:
            dt = abs(referenceEvent[0] - e[0]) / self.timeResolution
            cost = Util.calculateMatchingCosts(dt, self.maxTimeSlot)
            #print("possible events for matching: {} \n matching costs: {}".format(
            #    e, cost))
            disp = int(abs(referenceEvent[1] - e[1]))
            self.WMI[int(referenceEvent[2]), int(referenceEvent[1]), disp] = cost

    def applyFilter(self, filter2d):
        for i in range(self.max_disp):
            self.WMI[:, :, i] = signal.convolve2d(self.WMI[:, :, i], filter2d, boundary='symm', mode='same', fillvalue=0)

    def evaluateAll(self):
        print("Process Start:")
        print(self.cameraBuffer.leftBuffer.shape[0])
        print(str(self.cameraBuffer.leftBuffer.shape[0]) + "event(s) in total.")
        filterAvg = np.ones((3, 3), dtype=np.float) / 9
        #filtergauss = cv2.getGaussianKernel(3, 1.5)*cv2.getGaussianKernel(3, 1.5).transpose()
        print("filterfiltergauss: {}".format(filterAvg))
        for i in range(self.cameraBuffer.leftBuffer.shape[0]):
        #for i in range(1098723,1098724):
            candidateEvent = self.cameraBuffer.searchCorrespondingEventsOnRight(self.cameraBuffer.leftBuffer[i])
            self.refreshWMI(self.cameraBuffer.leftBuffer[i], candidateEvent)

            if i % 10000 == 0:
                #print("i: {}".format(i))
                self.applyFilter(filterAvg)
                res = np.argmax(self.WMI[:,:,:], 2)
                print(np.amax(self.WMI))
                plt.imshow(res, cmap="binary")
                title = str(i) + ".png"
                plt.savefig(title)
                plt.show()

            if i% 100== 0:
                self.WMI = np.subtract(self.WMI, 9)
                self.WMI = self.WMI.clip(min=0)

            #if i % 1000 == 0:
            #    res = np.argmax(self.WMI, 2)*10
            #    self.output.write(res)


        self.output.release()
