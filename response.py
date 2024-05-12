
from generate_audio import generate_audio
from generate_text_response import generate_text_response
from generate_video import generate_video
from pydantic import BaseModel
from schemas import CharacterResponse, Message
from typing import List


def generate_character_response(messages: List[Message]) -> CharacterResponse:
    # check if the last message is a user message 
    message = messages[-1]
    if message.role != "user":
        return None
    # Get the character name and text response from LLM
    character_response = generate_text_response(input)

    # Generate audio from the text response
    generate_audio(character_response)

    # Generate video from the audio and character face
    character_response_with_video = generate_video(character_response)

    return character_response_with_video


response = generate_character_response("What has movies taught you?")
print(response.name)
print(response.text)
