import os
import elevenlabs
import argparse
from elevenlabs import Voice, VoiceSettings, generate, play
from elevenlabs import set_api_key

import dotenv

dotenv.load_dotenv()
set_api_key(os.getenv("ELEVEN_LABS_API_KEY"))

def get_audio(text_arr):
    audio_arr = []
    for text in text_arr:
        audio_arr.append(
            generate(
            text=text,
            voice=Voice(
                voice_id='EXAVITQu4vr4xnSDxMaL',
                settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True)
            )
        )
        )
        play(audio_arr[0])
        return audio_arr

# call open ai api and get completion for the following prompt
if __name__ == "__main__":
    get_audio(["Hello! My name is Bella."])
