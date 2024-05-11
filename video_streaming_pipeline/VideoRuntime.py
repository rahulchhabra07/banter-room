from threading import Thread
import cv2
from video_streaming_pipeline.VideoGet import VideoGet
from video_streaming_pipeline.VideoShow import VideoShow

class VideoRuntime:
    """
    Class that continuously shows a frame using a dedicated thread.
    """

    def __init__(self):
        self.stopped = False
        self.src = 0

    def start(self):
        Thread(target=self.run, args=()).start()
        return self

    def run(self):
        video_getter = VideoGet().start()
        video_shower = VideoShow()
        frame = video_getter.frame
        video_shower.frame = frame
        video_shower.start()

        while not self.stopped:
            video_getter.src = self.src
            frame = video_getter.frame
            video_shower.frame = frame

    def stop(self):
        self.stopped = True