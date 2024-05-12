import soundfile as sf
from elevenlabs import save, stream
from elevenlabs.client import ElevenLabs
from schemas import CharacterResponse, characters, get_character_by_name
from dotenv import load_dotenv
import os
load_dotenv()

client = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY")
)

def generate_audio(character_response: CharacterResponse):
    character = get_character_by_name(character_response.name)
    audio_stream = client.generate(
        text=character_response.text,
        voice=character.voice_id,
        stream=True
        )
    bytearray_data = bytearray()
    for chunk in audio_stream:
        bytearray_data.extend(chunk)
    bytes_object = bytes(bytearray_data)
    # save(audio_stream, "intermediate/" + character.get_compact_name() + ".wav")
    character_response.audio_bytes = bytes_object
    return character_response


# cr = generate_audio(CharacterResponse(name="Dwayne Johnson", text="I'm Dwayne the rock Johnson"))
# print(cr.audio_bytes)