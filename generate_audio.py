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
    save(audio_stream, "intermediate/" + character.get_compact_name() + ".wav")
    character_response.audio_bytes = bytes(audio_stream)
    print ("in generate_audio")
    print (character_response.audio_bytes)
    return character_response
