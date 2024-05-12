import os, io
import requests
import cv2
import base64
import PIL
import streamlit as st
from faster_whisper import WhisperModel
from audio_recorder_streamlit import audio_recorder
from octoai.util import to_file
from octoai.client import OctoAI
from response import generate_character_response
from schemas import Message
import time

st.set_page_config(layout="wide")

st.title("Quintelligence!")
octoai_client = OctoAI()


# audio_file = '/Users/shubhankar/Downloads/voice.mp3'
#
# with open(audio_file, "rb") as f:
#     audio_data = f.read()
#     b64 = base64.b64encode(audio_data).decode("utf-8")
#
# # HTML to embed the audio file using base64
# audio_html = f"""
# <audio controls autoplay>
#     <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
#     Your browser does not support the audio element.
# </audio>
# """
# Display the audio player
# st.markdown(audio_html, unsafe_allow_html=True)

whisper_model = WhisperModel("base", device="cpu", compute_type="int8", cpu_threads=int(os.cpu_count() / 2))

def speech_to_text(audio_chunk):
    segments, info = whisper_model.transcribe(audio_chunk, beam_size=5)
    speech_text = " ".join([segment.text for segment in segments])
    return speech_text


def base64_to_html_video(base64_string):
    # Convert base64 to HTML video tag source
    video_url = f"data:video/mp4;base64,{base64_string}"
    return f'<video width="100%" controls autoplay loop><source src="{video_url}" type="video/mp4"></video>'

def base64_to_html_audio(base64_string):
    # Convert base64 to HTML video tag source
    return f"""
    <audio autoplay>
    <source src="data:audio/mp3;base64,{base64_string}" type="audio/mp3">
    </audio>"""

def create_image(character_name):

    OCTOAI_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNkMjMzOTQ5In0.eyJzdWIiOiI4ZWEwNjllYS04MzA1LTQ4ODEtYWVhMi0wOGUyZjQwMmE4MzciLCJ0eXBlIjoidXNlckFjY2Vzc1Rva2VuIiwidGVuYW50SWQiOiIxNWFhNjI5Zi1iOGUyLTQ0YTMtYWJhYi1jZmRjNDYyNGMxZjUiLCJ1c2VySWQiOiIyOTRlMmMyOS03Zjc2LTQ1NWYtYTY1OS02MWNhYmMzYWIzYWIiLCJhcHBsaWNhdGlvbklkIjoiYTkyNmZlYmQtMjFlYS00ODdiLTg1ZjUtMzQ5NDA5N2VjODMzIiwicm9sZXMiOlsiRkVUQ0gtUk9MRVMtQlktQVBJIl0sInBlcm1pc3Npb25zIjpbIkZFVENILVBFUk1JU1NJT05TLUJZLUFQSSJdLCJhdWQiOiIzZDIzMzk0OS1hMmZiLTRhYjAtYjdlYy00NmY2MjU1YzUxMGUiLCJpc3MiOiJodHRwczovL2lkZW50aXR5Lm9jdG8uYWkiLCJpYXQiOjE3MTU0OTc5ODN9.rEBPFRftKfSvA2KeO_hlOsvqVv8f51OsfAutr5pwUcBjaJAWdBobOOguU8iyqBU-ox_0acnnyfdi7Rr2ZORkwWQDMGn-xU7Ai_3eM5WfH9RB45HwA8-HQSUc0Zq-HY2lH89nYRwc36E2WcWCvaB6i2UZHgBT98ANsMULmjgFS4uvww3SRK61ayvSFZUd9R0dvnMRbflBDITEwAgXOjhRp52IgDdaNtixDCnK5B4E3WDYl5VMbmWZ8cJG84wvixLpTCqW1VvxbPjgP3P3TXr9_X26qbKsTalLSTMsULXmb729L4RxFfsru6b-90P7a97UvSavyfdpL73_2ITEO6KCIQ"

    headers = {
        "Authorization": f"Bearer {OCTOAI_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "prompt": f"{character_name}, sitting in a well-lit environment talking on the laptop, with llamas grazing on a farm in the background",
        "negative_prompt": "Blurry photo, distortion, low-res, bad quality",
        "style_preset":"cinematic",
        "loras":{"add-detail": 1.0},
        "steps":30,
    }


    response = requests.post("https://image.octoai.run/generate/sdxl", headers=headers, json=payload)

    if response.status_code != 200:
        print(response.text)

    img_list = response.json()["images"]

    # It can also be helpful to run another generate method with
    # num_images = image_resp.removed_for_safety to get your desired total images
    # to_file(img_list[0], f"./assets/{character_name}.jpeg")

    img_bytes = base64.b64decode(img_list[0]["image_b64"])
    img = PIL.Image.open(io.BytesIO(img_bytes))
    img.load()
    img.save(f"./assets/{character_name}.jpeg")

    # response = requests.post(, headers=headers, json=payload)

    # if response.status_code != 200:
    #     print(response.text)

    # img_list = response.json()["images"]

    # for i, img_info in enumerate(img_list):
    #     img_bytes = base64.b64decode(img_info["image_b64"])
    #     img = PIL.Image.open(io.BytesIO(img_bytes))
    #     img.load()
    #     img.save(f"./assets/{character_name}.jpg")
    #     break

# Using containers for each row
top_row = st.container()
bottom_row = st.container()
footer_container = st.container()

# Placeholder references to keep the camera feeds
FRAME_WINDOW1 = None
FRAME_WINDOW2 = None

# Initialize session state for user selections if not already set
if 'user1' not in st.session_state:
    st.session_state.user1 = ''
if 'user2' not in st.session_state:
    st.session_state.user2 = ''


# Initialize session state for video states
if 'user1_video_state' not in st.session_state:
    st.session_state.user1_video_state = 'image'
if 'user2_video_state' not in st.session_state:
    st.session_state.user2_video_state = 'image'

with top_row:
    col1, col2 = st.columns(2)
    with col1:
        user1 = st.selectbox('Who do you wanna chat with?', ['', 'Dwayne Johnson', 'Elon Musk', 'Donald Trump', 'Mark Zuckerberg', 'Albert Einstein'], key='1a', on_change=lambda: setattr(st.session_state, 'user1', st.session_state['1a']))
        if user1 == '':
            FRAME_WINDOW2 = st.image("./assets/llama1.png", width=640)  # Default image
        else:
            if st.session_state.user1_video_state == 'image':
                if not os.path.exists(f"""./assets/{user1.lower().replace(' ', '_')}.jpeg"""):
                    create_image(user1.lower().replace(" ", "_"))
                FRAME_WINDOW2 = st.image(f"./assets/{user1.lower().replace(' ', '_')}.jpeg", width=640)
            else:
                video_html = base64_to_html_video(st.session_state.user1_video_data)
                st.markdown(video_html, unsafe_allow_html=True)
                print (st.session_state.user1_video_state)
                time.sleep(30)
                st.session_state.user1_video_state = 'image'
    with col2:
        user2 = st.selectbox('Who do you wanna chat with?', ['', 'Dwayne Johnson', 'Elon Musk', 'Donald Trump', 'Mark Zuckerberg', 'Albert Einstein'], key='2a', on_change=lambda: setattr(st.session_state, 'user2', st.session_state['2a']))
        if user2 == '':
            FRAME_WINDOW2 = st.image("./assets/llama2.png", width=640)  # Default image
        else:
            if st.session_state.user2_video_state == 'image':
                if not os.path.exists(f"./assets/{user2.lower().replace(' ', '_')}.jpeg"):
                    create_image(user2.lower().replace(' ', '_'))
                FRAME_WINDOW2 = st.image(f"./assets/{user2.lower().replace(' ', '_')}.jpeg", width=640)
            else:
                video_html = base64_to_html_video(st.session_state.user2_video_data)
                st.markdown(video_html, unsafe_allow_html=True)
                st.session_state.user2_video_state = 'image'

# Bottom row with one video feed centered
with bottom_row:
    col3 = st.columns([1,2,1])
    with col3[1]:
        FRAME_WINDOW3 = st.image([])
        desc3 = st.text('You (Human)')


with footer_container:
    audio_bytes = audio_recorder()
    if audio_bytes:
        # Write the audio bytes to a file
        with st.spinner("Transcribing..."):
            webm_file_path = "audio.mp3"
            with open(webm_file_path, "wb") as f:
                f.write(audio_bytes)
            # set current time
            current_time = time.time()
            transcript = speech_to_text(webm_file_path)
            # print time difference from current time
            print(f"Time taken for transcription: {time.time() - current_time}")
            message = [Message(role="user",content=transcript)] ## remove this - currently hardcoded for testing
            # message = [Message(role="user",content="What is your name man?")] ## remove this - currently hardcoded for testing
            if message:
                os.remove(webm_file_path)
                response = generate_character_response(message)
                print("response from character")
                print(response.text)
                #ToDo add text to response

                b64 = base64.b64encode(response.audio_bytes).decode("utf-8")
                md = f"""
                <audio controls autoplay>
                <source src="data:audio/wav;base64,{b64}" type="audio/wav">
                </audio>
                """
                x = st.markdown(md, unsafe_allow_html=True)
                time.sleep(15)
                x.empty()


camera = cv2.VideoCapture(0)

while True:
    ret, frame = camera.read()
    if not ret:
        break
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    FRAME_WINDOW3.image(frame)
