import numpy as np
from CameraBuffer import CameraBuffer
from scipy import signal
from Util import *
from matplotlib import pyplot as plt


class OutputController(object):
    def __init__(self, maxX, maxY, max_disp, timeRes, maxTimeSlot, cameraBuffer: CameraBuffer):
        self.maxX = maxX
        self.maxY = maxY
        self.max_disp = max_disp
        self.timeResolution = timeRes
        self.cameraBuffer = cameraBuffer
        self.maxTimeSlot = maxTimeSlot
        self.WMI = np.zeros((maxY, maxX, max_disp))

    def refreshWMI(self, referenceEvent, candidateEvent: list):
        for e in candidateEvent:
            dt = abs(referenceEvent[0] - e[0]) / self.timeResolution
            cost = Util.calculateMatchingCosts(dt, self.maxTimeSlot)
            disp = int(abs(referenceEvent[1] - e[1]))
            self.WMI[referenceEvent[2], referenceEvent[1], disp] = cost

    def applyFilter(self, filter2d):
        for i in range(self.max_disp):
            self.WMI[:, :, i] = signal.convolve2d(self.WMI[:, :, i], filter2d, boundary='symm', mode='same', fillvalue=0)

    def evaluateAll(self):
        print("Process Start:")
        print(str(self.cameraBuffer.leftBuffer.shape[0]) + "event(s) in total.")
        filterAvg = np.ones((3, 3), dtype=np.float) / 9
        for i in range(self.cameraBuffer.leftBuffer.shape[0]):
            candidateEvent = self.cameraBuffer.searchCorrespondingEventsOnRight(self.cameraBuffer.leftBuffer[i])
            self.refreshWMI(self.cameraBuffer.leftBuffer[i], candidateEvent)
            if i % 500 == 0:
                print(i)
                self.applyFilter(filterAvg)
                res = np.argmax(self.WMI, 2)
                plt.imshow(res, cmap="gray")
                plt.show()


