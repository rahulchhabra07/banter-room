from dotenv import load_dotenv
import os
import requests


load_dotenv()




def generate_audio(text):




    params = {
        'optimize_streaming_latency': '0',
    }

    json_data = {
        "source_url": "https://myhost.com/image.jpg",
        "script": {
            "type": "text",
            "input": "Hello world!"
        }
    }

    response = requests.post(
        'https://api.elevenlabs.io/v1/text-to-speech/8B8ScIos6qDxjjY930Zx',
        params=params,
        headers=headers,
        json=json_data,
    )
    # print (response.content)
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
    wav_file = "output.wav"
    sf.write(wav_file, data, samplerate)
    print ("converted to wav")

    # save_audio_bytes(generated_audio[0], "result.wav", outputFormat="wav")
    # save_audio_bytes(generated_audio[0], "result.wav", outputFormat="wav")

    # for historyItem in user.get_history_items():
    #     if historyItem.text == "Test.":
    #         # The first items are the newest, so we can stop as soon as we find one.
    #         historyItem.delete()
    #         break
