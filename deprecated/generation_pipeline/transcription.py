import whisper
import time

def transcription(audio):

    start_time = time.time()

    model = whisper.load_model("base")
    result = model.transcribe(audio)

    end_time = time.time()
    execution_time = end_time - start_time

    print("Execution time:", execution_time, "seconds")

    out = result["text"]
    print('[INFO] Audio transcription:', out)
    return out
