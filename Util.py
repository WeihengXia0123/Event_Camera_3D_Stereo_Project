import numpy as np
import bisect
from array2gif import write_gif


class Util(object):
    @staticmethod
    def searchEvent(buffer):
        return

    @staticmethod
    def calculateMatchingCosts(dt, maxDt, functionType=1):
        if functionType == 1:  # inverse linear
            return (abs(maxDt-dt))
        elif functionType == 2:  # inverse quadratic TODO
            a = 1
            weight = 1 / (a * np.pow(dt, 2) + 0.1)
            return weight
        elif functionType == 3:
            mht = 10  # maximal considered history events TODO
            b = 1
            weight = mht * np.exp(-dt / b)
            return weight

    @staticmethod
    def loadEvents(path):
        return np.genfromtxt(fname=path, delimiter=' ', dtype=np.float, skip_header=0)[:]

