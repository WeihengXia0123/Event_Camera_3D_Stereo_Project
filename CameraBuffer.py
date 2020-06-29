from Util import *

class CameraBuffer(object):
    def __init__(self, maxX, maxY, pathToLeft, pathToRight, max_disp, timeRes):
        self.maxX = maxX
        self.maxY = maxY
        self.pathLeft = pathToLeft
        self.pathRight = pathToRight
        self.timeResolution = timeRes
        self.maxTimeSlot = 10
        self.maxdT = self.maxTimeSlot * self.timeResolution
        self.maxDisp = max_disp
        # leftBuffer n x 4 ndarray
        self.leftBuffer = None
        self.rightBuffer = np.empty((maxY, 0)).tolist()
        self.rightBufferSearchBegin = np.zeros(maxY)
        return

    def prepareData(self):
        self.leftBuffer = np.genfromtxt(fname=self.pathLeft, delimiter=' ', dtype=np.float, skip_header=0)[:]
        events_right = np.genfromtxt(fname=self.pathRight, delimiter=' ', dtype=np.float, skip_header=0)[:]
        for e in events_right:
            #bisect.insort(self.rightBuffer[int(e[2])],[e[0], int(e[1]), int(e[3])])
            self.rightBuffer[int(e[2])].append([e[0], int(e[1]), int(e[3])])

    def sortRightBuffer(self):
        for i in range(self.maxY):
            self.rightBuffer[i] = sorted(self.rightBuffer[i], key=lambda x: x[0])

    def searchCorrespondingEventsOnRight(self, data: np.ndarray) -> list:
        currentTime = data[0]
        y = int(data[2])
        p = int(data[3])
        res = []
        maxdT = self.maxTimeSlot * self.timeResolution
        for i in range(0, int(len(self.rightBuffer[y]))):
            # Check if compare to future events
            #print("timestamp right: {}".format(self.rightBuffer[y][i][0]))
            if currentTime > self.rightBuffer[y][i][0]: ##not working because of some unsorted events despite sorting
                continue
            # Update search begin TODO delete unused events
            elif self.rightBuffer[y][i][0]- currentTime > maxdT:
                #self.rightBuffer[y].remove([i])
                #self.rightBufferSearchBegin[y] = int(i)
                continue
            # Check disparity
            elif abs(data[1] - self.rightBuffer[y][i][1]) > (self.maxDisp - 1):
                continue
            # check if polarity is the same
            elif p == self.rightBuffer[y][i][2]:
                res.append(self.rightBuffer[y][i])
        return res

