import argparse

from gpt import generate_transcription
from eleven import get_audio

import json

# def persist_to_file(file_name):

#     def decorator(original_func):

#         try:
#             cache = json.load(open(file_name, 'r'))
#         except (IOError, ValueError):
#             cache = {}

#         def new_func(*args, **kwargs):
#             param = json.dumps(args) + json.dumps(kwargs)
#             if param not in cache:
#                 cache[param] = original_func(param)
#                 json.dump(cache, open(file_name, 'w'))
#             return cache[param]

#         return new_func

#     return decorator

# generate_transcription = persist_to_file(generate_transcription)
# get_audio = persist_to_file(get_audio)

def main(summary, topic, length="1", level_of_detail="beginner"):
    print(f"generating transcript for topic: {topic}, length: {length}, level of detail: {level_of_detail}")
    transcript = generate_transcription(summary, topic, length, level_of_detail)

    print("generated")
    print(transcript)

    print("reading")
    audio = get_audio([transcript])

    # #save audio to file
    # with open("audio.mp3", "wb") as f:
    #     f.write(audio)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", type=str, default="leadership", help="topic")
    parser.add_argument("--summary_file", type=str, default="summary.txt", help="summary file")
    parser.add_argument("--length", help="length of the podcast episode", default="1")
    parser.add_argument("--level_of_detail", help="level of detail of the podcast episode", default="beginner")
    args = parser.parse_args()

    main(args.summary_file, args.topic, args.length, args.level_of_detail)

