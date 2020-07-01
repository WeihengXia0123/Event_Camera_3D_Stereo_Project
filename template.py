from src.CameraBuffer import CameraBuffer
from src.OutputController import OutputController

if __name__ == "__main__":
    filepath_left = 'C:/Users/7zieg/Downloads/BioVision/cam0/events.txt'
    filepath_right = 'C:/Users/7zieg/Downloads/BioVision/cam1/events.txt'
    max_y = 180
    max_x = 240
    max_disp = 50
    maxTimeSlot = 10
    timeRes = 1.0 ** -5
    cameraBuffer = CameraBuffer(max_x, max_y, filepath_left, filepath_right, max_disp, timeRes)
    cameraBuffer.prepareData()
    outputController = OutputController(max_x, max_y, max_disp, timeRes, maxTimeSlot, cameraBuffer)
    outputController.evaluateAll()


