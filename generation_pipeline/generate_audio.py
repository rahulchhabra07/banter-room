from elevenlabslib import *
from elevenlabslib.helpers import *
from dotenv import load_dotenv
import os
import soundfile as sf
import pyaudio
import wave

import requests


load_dotenv()

# user = ElevenLabsUser(os.getenv("ELEVENLABS_API_KEY"))
# # voice = user.get_voices_by_name("feynman")[0]  # This is a list because multiple voices can have the same name

def generate_audio(text, wav_file = "output.wav"):
    # voice.play_preview(playInBackground=False)


    # generated_audio = voice.generate_and_play_audio(text, playInBackground=False)
    # generated_audio = voice.generate_audio("This is a test.", stability=0.4)
    # generated_audio = voice.generate_audio(text, stability=0.4)


    headers = {
        'accept': 'audio/mpeg',
        'xi-api-key': os.getenv('ELEVENLABS_API_KEY'),
        'Content-Type': 'application/json',
    }

    params = {
        'optimize_streaming_latency': '0',
    }

    json_data = {
        'text': text,
        'model_id': 'eleven_monolingual_v1',
        'voice_settings': {
            'stability': 0.4,
            'similarity_boost': 0.4,
        },
    }

    response = requests.post(
        'https://api.elevenlabs.io/v1/text-to-speech/Zm0rfnJGFy5t9H9CI45S',
        params=params,
        headers=headers,
        json=json_data,
    )

    # print(response.content)

    if response.headers.get('content-type') == 'audio/mpeg':
    # Save the content as an MP3 file
        with open('output.mp3', 'wb') as f:
            f.write(response.content)
        print("File saved successfully as audio.mp3")
    else:
        print("Invalid content type. Expected audio/mpeg.")

    print ("now converting to wav")
    mp3_file = "output.mp3"
    data, samplerate = sf.read(mp3_file)
    sf.write(wav_file, data, samplerate)
    print ("converted to wav")

    # save_audio_bytes(generated_audio[0], "result.wav", outputFormat="wav")
    # save_audio_bytes(generated_audio[0], "result.wav", outputFormat="wav")

    # for historyItem in user.get_history_items():
    #     if historyItem.text == "Test.":
    #         # The first items are the newest, so we can stop as soon as we find one.
    #         historyItem.delete()
    #         break
