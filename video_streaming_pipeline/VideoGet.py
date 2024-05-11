from threading import Thread
import cv2
import numpy as np
import time
from ffpyplayer.player import MediaPlayer
from video_streaming_pipeline.inference import Inference

def black_frame():
    return np.zeros((666, 1000, 3)).astype('uint8')

class VideoGet:
    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread.
    """

    def __init__(self, src=0):
        self.src = src
        self.stream = cv2.VideoCapture()
        self.listen_stream = cv2.VideoCapture("assets/richard-feynman.mp4")
        self.listen_stream.set(cv2.CAP_PROP_BUFFERSIZE, 2)

        self.curr_listen_frame = 0

        width  = int(self.listen_stream.get(cv2.CAP_PROP_FRAME_WIDTH))  # float `widt
        height = int(self.listen_stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.frame_count = int(self.listen_stream.get(7))

        self.listen_frames = np.zeros((self.frame_count, height, width, 3)).astype('uint8')

        for idx in range(0, self.frame_count):
            (grabbed, frame) = self.listen_stream.read()
            if grabbed:
                self.listen_frames[idx] = frame

        self.grabbed = False
        self.frame = self.listen_frames[0]
        self.curr_listen_frame += 1
        self.stopped = False
        self.audio_stream = MediaPlayer("")

        self.inf = Inference()

        self.FPS = 1/30
        self.FPS_MS = int(self.FPS * 1000)




    def start(self):    
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        self.inf.start()
        idx = 0
        while not self.stopped:
            if not self.grabbed:
                # self.frame = black_frame()
                self.curr_listen_frame = self.curr_listen_frame % self.frame_count 
                self.frame = self.listen_frames[self.curr_listen_frame]
                self.curr_listen_frame += 1
                time.sleep(self.FPS)
                if self.src != 0:
                    self.audio_stream = MediaPlayer(self.src)
                    self.stream = cv2.VideoCapture(self.src)
                    self.stream.set(cv2.CAP_PROP_BUFFERSIZE, 2)
                    self.grabbed = True
            else:
                (self.grabbed, self.frame) = self.stream.read()
                # self.frames[self.idx] = self.frame
                audio_frame, val = self.audio_stream.get_frame()
                if val != 'eof' and audio_frame is not None:
                    #audio
                    img, t = audio_frame
                if not self.grabbed:
                    self.src = 0
                    # self.frame = black_frame()
                    self.curr_listen_frame = self.curr_listen_frame % self.frame_count 
                    self.frame = self.listen_frames[self.curr_listen_frame]
                    self.curr_listen_frame += 1
                    self.inf.start()
                time.sleep(self.FPS)

    def stop(self):
        self.stopped = True