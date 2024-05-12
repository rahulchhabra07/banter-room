from threading import Thread
import cv2
import numpy as np

class VideoShow:
    """
    Class that continuously shows a frame using a dedicated thread.
    """

    def __init__(self, frame=None, fps_ms = int(1000 / 30)):
        self.frame = frame
        self.stopped = False
        self.FPS_MS = fps_ms

    def start(self):
        Thread(target=self.show, args=()).start()
        return self

    def show(self):
        cv2.imshow("Agent", self.frame)
        cv2.waitKey(self.FPS_MS)

    def stop(self):
        self.stopped = True