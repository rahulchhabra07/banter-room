from generation_pipeline.generate_text_response import generate_text_response
from generation_pipeline.generate_audio import generate_audio
from generation_pipeline.generate_video import generate_video
from generation_pipeline.take_in_audio import take_in_audio
from generation_pipeline.transcription import transcription
from threading import Thread

class Inference:
    def __init__(self, person=None):
       self.stopped = False 
       self.url = 0
       self.paused = False
       self.person = person
       self.intro_run()

    def start(self):
        if not self.paused:
            self.url = 0
            self.paused = True
            Thread(target=self.run, args=()).start()
            return self

    def intro_run(self):
        if self.person == "richard":
            out = generate_video("richard-intro.wav")
            print(out)

    def run(self):
        self.url = 0
        audio = take_in_audio()
        audio_transcription = transcription(audio)
        text = generate_text_response(audio_transcription)
        generate_audio(text)
        self.url = generate_video()
        self.paused = False
