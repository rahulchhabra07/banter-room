import datetime
import os

import httpx

from deepgram import DeepgramClient, FileSource, PrerecordedOptions

dg = DeepgramClient(api_key=os.getenv("DEEPGRAM_API_KEY"))

def speech_to_text_deepgram(audio_file_path: str):
    try:
        with open(audio_file_path, "rb") as f:
            audio_data = f.read()
        
        payload: FileSource = {
                "buffer": audio_data,
            }

        options: PrerecordedOptions = PrerecordedOptions(
                model="nova-2",
                smart_format=True,
                utterances=True,
                punctuate=True,
                diarize=True,
            )
        
        before = datetime.now()
        response = dg.listen.prerecorded.v("1").transcribe_file(
            payload, options, timeout=httpx.Timeout(300.0, connect=10.0)
        )
        after = datetime.now()

        print(response.to_json(indent=4))
        print("")
        difference = after - before
        print(f"time: {difference.seconds}")

    except Exception as e:
        print(f"Exception: {e}")

speech_to_text_deepgram("intermediate/richard_feynman.wav")