import numpy as np


class Util(object):
    def searchEvent(self, buffer):
        return

    def calculateMatchingCosts(self, timestampleft, timestampright, weightingfunction=1):
        timediff = timestampleft - timestampright
        if weightingfunction == 1:  # inverse linear
            return timediff
        elif weightingfunction == 2:  # inverse quadratic
            a = 1
            weight = 1 / (a * np.pow(timediff, 2) + 0.1)
            return weight
        elif weightingfunction == 3:
            mht = 10  # maximal considered hsitory events
            b = 1
            weight = mht * np.exp(-timediff / b)
            return weight
        else:
            return timediff
