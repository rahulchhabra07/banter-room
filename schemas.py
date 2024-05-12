from typing import Literal, Optional

from pydantic import BaseModel


class Character(BaseModel):
    name: str
    voice_id: str
    reference_video: str

    def get_compact_name(self) -> str:
        return self.name.lower().replace(" ", "_")

characters = [
    Character(
        name="Richard Feynman",
        # TODO: Change voice_id to the correct one
        voice_id="x03GbtOlt6LpiBmkYH0A",
        reference_video="assets/richard_feynman.mp4"
    ),
    Character(
        name="Dwayne Johnson",
        # TODO: Change voice_id to the correct one
        voice_id="zeeGOq4wDKjCp0xQmwXC",
        reference_video="assets/dwayne_johnson.mp4"
    ),
]

character_names = [character.name for character in characters]

def get_character_by_name(name: str) -> Character:
    for character in characters:
        if character.name == name:
            return character
    raise ValueError(f"Character with name {name} not found")

class CharacterResponse(BaseModel):
    name: str
    text: str
    audio_bytes: Optional[bytes] = None
    video_bytes: Optional[bytes] = None
