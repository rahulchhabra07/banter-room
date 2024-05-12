import cv2
from threading import Thread
import pyaudio

from generation_pipeline.take_in_audio import take_in_audio
from generation_pipeline.transcription import transcription
from clean.generate_text_response import generate_text_response
from clean.generate_audio import generate_audio
from generation_pipeline.generate_video import generate_video

from video_streaming_pipeline.VideoGet import VideoGet
from video_streaming_pipeline.VideoShow import VideoShow
from video_streaming_pipeline.VideoRuntime import VideoRuntime
from video_streaming_pipeline.inference import Inference
from ffpyplayer.player import MediaPlayer



p = pyaudio.PyAudio()
CHUNK = 1024


## Definitions
class Agent:
    def __init__(self, person = None):
        self.person = person
        if self.person and self.person == "richard":
            print("Please wait while Mr. Feynman shows up...")
            vcap = cv2.VideoCapture("https://replicate.delivery/pbxt/1kmwcoNueRyOGCLazhDptBwRsHDpL6oA8Ht0M4lz5Y8oSydIA/result_voice.mp4")
            audio = MediaPlayer("https://replicate.delivery/pbxt/1kmwcoNueRyOGCLazhDptBwRsHDpL6oA8Ht0M4lz5Y8oSydIA/result_voice.mp4")

            while True:
                (grabbed, frame) = vcap.read()
                audio_frame, val = audio.get_frame()
                if grabbed:
                    cv2.imshow("Agent", frame)
                    cv2.waitKey(int(1000 / 30))
                else:
                    break
                if val != 'eof' and audio_frame is not None:
                    #audio
                    img, t = audio_frame
            # Inference(self.person)
        self.is_running = False
        self.new_run()

    
    def new_run(self):
        video_getter = VideoGet().start()
        fps_ms = video_getter.FPS_MS
        video_shower = VideoShow(video_getter.frame, video_getter.FPS_MS)


        while True:
            url = video_getter.inf.url
            video_getter.src = url
            grabbed = video_getter.grabbed
            frame = video_getter.frame
            # if not grabbed:
            #     frame = np.zeros((666, 1000, 3)).astype('uint8')
            cv2.imshow("Agent", frame)
            cv2.waitKey(fps_ms)
            # if not grabbed and video_getter.frames_inited:
            #     outter = video_getter.frames.shape[0]
            #     print(outter)
            #     for i in range(0, outter):
            #         frame = video_getter.frames[i]
            #         print(frame.shape)
            #         time.sleep(video_getter.FPS)
            #         cv2.imshow("Agent", frame)
            #         cv2.waitKey(fps_ms)
            # else:
            #     cv2.imshow("Agent", frame)
            #     cv2.waitKey(fps_ms)
          

def start_sequence():
    audio = take_in_audio()
    audio_transcription = transcription(audio)

    if "talk" in audio_transcription.lower():
        if "richard" in audio_transcription.lower():
            return "richard"

    return None


if __name__ == '__main__':
    person = start_sequence()
    agent = Agent(person)




# stream video
