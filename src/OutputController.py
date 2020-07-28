from src.CameraBuffer import CameraBuffer
from scipy import signal
from src.Util import *
from matplotlib import pyplot as plt
import cv2


class OutputController(object):
    def __init__(self, maxX, maxY, max_disp, timeRes, maxTimeSlot, cameraBuffer: CameraBuffer):
        self.maxX = maxX
        self.maxY = maxY
        self.max_disp = max_disp
        self.timeResolution = timeRes
        self.cameraBuffer = cameraBuffer
        self.maxTimeSlot = maxTimeSlot
        self.WMI = np.zeros((maxY, maxX, max_disp))
        # self.output = cv2.VideoWriter("output.avi",  cv2.VideoWriter_fourcc(*'DIVX'), 5, (maxX, maxY))
        self.image_idx=0
        self.visual = np.zeros((self.maxY,self.maxX))

    def refreshWMI(self, referenceEvent, candidateEvent: list):
        #print("event from the left Buffer: {}".format(referenceEvent))#
        if True and len(candidateEvent) != 0 :
            tmp_e = candidateEvent[0]
            tmp_cost = 0

        for e in candidateEvent:
            dt = abs(referenceEvent[0] - e[0]) / self.timeResolution
            cost = Util.calculateMatchingCosts(dt, self.maxTimeSlot)
            #print("possible events for matching: {} \n matching costs: {}".format(
            #    e, cost))
            disp = int(abs(referenceEvent[1] - e[1]))
            self.WMI[int(referenceEvent[2]), int(referenceEvent[1]), disp] = cost
            if(tmp_cost < cost):
                tmp_cost = cost
                tmp_e = e
        if False and len(candidateEvent) != 0:
            self.visualizeMatching(referenceEvent,tmp_e)

    def applyFilter(self, filter2d):
        for i in range(self.max_disp):
            self.WMI[:, :, i] = signal.convolve2d(self.WMI[:, :, i], filter2d, boundary='symm', mode='same', fillvalue=0)

    def visualizeMatching(self, referenceEvents, matchingEvent):
            self.visual = np.subtract(self.visual, 1)
            self.visual = self.visual.clip(min=0)
            self.visual[int(referenceEvents[2]),int(referenceEvents[1])] = 19
            self.visual[int(referenceEvents[2]),int(matchingEvent[1])] = 19
            plt.imshow(self.visual, cmap="gist_ncar_r")
            plt.show()


    def evaluateAll(self):
        
        print("Process Start:")
        print(self.cameraBuffer.leftBuffer.shape[0])
        print(str(self.cameraBuffer.leftBuffer.shape[0]) + "event(s) in total.")
        filterAvg = np.ones((2, 2), dtype=np.float) / 4
        #filtergauss = cv2.getGaussianKernel(3, 1.5)*cv2.getGaussianKernel(3, 1.5).transpose()
        print("filter kernel: {}".format(filterAvg))
        for i in range(self.cameraBuffer.leftBuffer.shape[0]):
            candidateEvent = self.cameraBuffer.searchCorrespondingEventsOnRight(self.cameraBuffer.leftBuffer[i])
            self.refreshWMI(self.cameraBuffer.leftBuffer[i], candidateEvent)

            if i % 10000 == 0:
                #print("i: {}".format(i))
                self.applyFilter(filterAvg)
                res = np.argmax(self.WMI[:,:,:], 2)
                print(res)
                
                # Calculate Depth Map
                # DepthMap = 3*20/res
                # print("depth map: ", DepthMap)
                
                plt.imshow(res, cmap="brg") #res
                title = "result_simple/"+format(self.image_idx, '03d') + ".png" #str(i) + ".png"
                self.image_idx += 1
                plt.clim(0, 40)
                plt.colorbar()
                plt.savefig(title)
                # plt.close()
                plt.show()

            if i% 100== 0:
                self.WMI = np.subtract(self.WMI, 9)
                self.WMI = self.WMI.clip(min=0)

            #if i % 1000 == 0:
            #    res = np.argmax(self.WMI, 2)*10
            #    self.output.write(res)


        # self.output.release()
