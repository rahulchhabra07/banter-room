from schemas import CharacterResponse, get_character_by_name


def generate_video(character_response: CharacterResponse) -> CharacterResponse:
    # TODO: Use wav2lip to generate video from audio and character face
    character = get_character_by_name(character_response.name)
    reference_video_file = character.reference_video
    audio_file = character.get_compact_name() + ".wav"

    # TODO: instead of the reference file, gernerate the lip synced video and return that instead
    with open(reference_video_file, "rb") as f:
        reference_video_bytes = f.read()
        character_response.video_bytes = reference_video_bytes

    return character_response
