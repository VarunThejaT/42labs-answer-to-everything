import os
import elevenlabs
import argparse
from elevenlabs import Voice, VoiceSettings, generate, play, save
from elevenlabs import set_api_key

import dotenv

dotenv.load_dotenv()
set_api_key(os.getenv("ELEVEN_LABS_API_KEY"))

def get_audio(text):
    return generate(
            text=text,
            model="eleven_multilingual_v2",
            voice=Voice(
                voice_id='EXAVITQu4vr4xnSDxMaL',
                settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True)
            )
        )

import soundfile as sf
from io import BytesIO
# call open ai api and get completion for the following prompt
if __name__ == "__main__":
    audio = get_audio("""Welcome to today's podcast episode, where we'll be discussing the fascinating world of procrastination. Have you ever found yourself pushing tasks to the side, only to panic and rush to complete them last minute? Well, you're not alone!
In a recent TED talk, we learned about something called the "procrastinator's dilemma." In this talk, the speaker dives deep into the inner workings of a procrastinator's brain and highlights the conflict between our rational decision-maker and the instant gratification monkey. Sure, procrastination can sometimes lead to short-term bursts of productivity, but it can also cause long-term unhappiness and regrets.
One notable concept introduced in this talk is the idea of the "dark playground." This is where procrastinators engage in enjoyable activities when they really should be tackling important tasks. The speaker also discusses the different types of procrastination: the somewhat amusing, deadline-based kind, as well as the not-so-funny long-term procrastination where life goals can be left unfulfilled.
The key takeaway from this insightful talk? It's crucial for us to overcome our instant gratification monkey, establish deadlines, and take control of our time management. By doing so, we can pursue our dreams and lead more fulfilling lives.
So, next time you find yourself procrastinating, remember, you have the power to break free from the dark playground and make progress towards your goals. Until next time, happy goal-crushing!""")
    audio_file_location = f"sample.mp3"

    save(audio, audio_file_location)