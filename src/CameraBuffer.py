from src.Util import *

class CameraBuffer(object):
    def __init__(self, maxX, maxY, pathToLeft, pathToRight, max_disp, timeRes):
        self.maxX = maxX
        self.maxY = maxY
        self.pathLeft = pathToLeft
        self.pathRight = pathToRight
        self.timeResolution = timeRes
        self.maxTimeSlot = 1
        self.maxdT = self.maxTimeSlot * self.timeResolution
        self.maxDisp = max_disp
        # leftBuffer n x 4 ndarray
        self.leftBuffer = None
        self.rightBuffer = None
        self.rightBufferSearchBegin = np.zeros(maxY)
        return

    def prepareData(self):
        self.rightBuffer = [[]] * self.maxY
        self.leftBuffer = np.genfromtxt(fname=self.pathLeft, delimiter=' ', dtype=np.float, skip_header=0)[:]
        events_right = np.genfromtxt(fname=self.pathRight, delimiter=' ', dtype=np.float, skip_header=0)[:]
        for e in events_right:
            self.rightBuffer[int(e[2])].append([e[0], int(e[1]), int(e[3])])

    def searchCorrespondingEventsOnRight(self, data: np.ndarray) -> list:
        currentTime = data[0]
        y = int(data[2])
        p = int(data[3])
        res = []
        maxdT = self.maxTimeSlot * self.timeResolution
        for i in range(int(self.rightBufferSearchBegin[y]), int(len(self.rightBuffer[y]))):
            if currentTime < self.rightBuffer[y][i][0]:
                break
            # Update search begin TODO delete unused events
            elif currentTime-self.rightBuffer[y][i][0] > maxdT:
                self.rightBufferSearchBegin[y] = int(i)  # to reduce computation , set search start
                continue
            # Check disparity
            elif abs(data[1] - self.rightBuffer[y][i][1]) > (self.maxDisp - 1):
                continue
            # check if polarity is the same
            elif p == self.rightBuffer[y][i][2]:
                res.append(self.rightBuffer[y][i])
        return res

    # Use Hashtable to store the events
    def prepareData_dict(self):
        self.leftBuffer = np.genfromtxt(fname=self.pathLeft, delimiter=' ', dtype=np.float, skip_header=0)[:]
        events_right = np.genfromtxt(fname=self.pathRight, delimiter=' ', dtype=np.float, skip_header=0)[:]
        self.rightBuffer = [{}] * self.maxY
        for e in events_right:
            x = int(e[1])
            y = int(e[2])
            if x in self.rightBuffer[y].keys():
                self.rightBuffer[y][x].append([e[0], int(e[3])])
            else:
                self.rightBuffer[y][x] = []
                self.rightBuffer[y][x].append([e[0], int(e[3])])


    def searchCorrespondingEventsOnRight_dict(self, data: np.ndarray) -> list:
        currentTime = data[0]
        x = int(data[1])
        y = int(data[2])
        p = int(data[3])
        res = []
        maxdT = self.maxTimeSlot * self.timeResolution
        # Only search event around x
        for i in range(-self.maxDisp, self.maxDisp):
            if x + i in self.rightBuffer[y].keys():
                for j in range(len(self.rightBuffer[y][x + i])):
                    if currentTime < self.rightBuffer[y][x + i][j][0]:
                        break
                    elif currentTime - self.rightBuffer[y][x + i][j][0] > maxdT:
                        self.rightBufferSearchBegin[y] = int(i)  # to reduce computation , set search start
                        continue
                    # check if polarity is the same
                    elif p == self.rightBuffer[y][x + i][j][1]:
                        # (timestamp, x, p)
                        res.append([self.rightBuffer[y][x + i][j][0], x + i, self.rightBuffer[y][x + i][j][1]])
        return res




