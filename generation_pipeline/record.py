import wave
import sys

import pyaudio

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1 if sys.platform == 'darwin' else 2
RATE = 44100
RECORD_SECONDS = 5

def record():
    with wave.open('created_asset_files/output.wav', 'wb') as wf:
        p = pyaudio.PyAudio()
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)

        print('\n[INFO] Will record microphone for {secs} seconds'.format(secs = RECORD_SECONDS))
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True)

        print('[INFO] Now recording from microphone...')
        for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
            wf.writeframes(stream.read(CHUNK))
        print('[INFO] Completed recording.\n')

        stream.close()
        p.terminate()
