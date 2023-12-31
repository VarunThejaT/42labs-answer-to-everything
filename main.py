import os
import openai
import argparse
import dotenv
import json
import hashlib
import requests
from eleven import get_audio
from elevenlabs import save
from gpt import make_class_prompt, make_transcription_prompt, generate_transcription, generate_classes
from deep_translator import GoogleTranslator

dotenv.load_dotenv()

# openai.organization = "org-5hbFMeJaQuatIgOn4ilTaMwN"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Model.list()
url = "https://api.twelvelabs.io/v1.1"
API_KEY = os.getenv("TWELVE_LABS_API_KEY")
API_KEY_2 = os.getenv("TWELVE_LABS_API_KEY_HEART_HEALTH")

def get_video_index_api_key(topic):
    if topic in ["leadership", "meditation"]:
        return API_KEY
    else:
        return API_KEY_2
    
def classify_videos(index_id, sub_topic, api_key):
    CLASSIFY_BULK_URL = f"{url}/classify/bulk"

    data =  {
    "options": ["conversation", "text_in_video"],
    "index_id": index_id,
    "classes": [{"name": sub_topic,
        "prompts": [
            sub_topic,
        ]}]
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "x-api-key": api_key
    }

    response = requests.post(CLASSIFY_BULK_URL, headers=headers, json=data)
    print (f'Status code: {response.status_code}')
    print(response.json())
    return response.json()["data"]

def summarize_video(video_id, api_key):
    payload = {
        "type": "chapter",
        "video_id": video_id,
    }
    headers = {
        "accept": "application/json",
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }

    url = "https://api.twelvelabs.io/v1.2/summarize"
    response = requests.post(url, json=payload, headers=headers)

    print(response.text)
    chapter_summaries = [x["chapter_summary"] for x in response.json()["chapters"]]
    return chapter_summaries

def main(config_file_name="leadership_config.json", topic_name="meditation", language_override=None):
    with open(config_file_name, 'r') as f:
        data = json.load(f)
    # print(data)
    payload = data['data'][topic_name] #leadership should be an input argument
    topic = payload["topic_name"]
    index_id = payload["index_id"]
    selected_language = language_override if language_override else payload["language_preferences"]
    number_of_categories = "5"
    level_of_detail = payload["skill_level"]
    length = "1"
    gpt_model = "gpt-4-0314"
    video_api_key = get_video_index_api_key(topic)
    # get_12_summary(payload)
    # classes_json = generate_classes(topic, number_of_categories, gpt_model)
    # classes_json = json.loads(classes_json)
    selected_subtopic = payload["selected_sub_topics"]
    list_of_audio_file_locations = []
    for sub_topic in selected_subtopic:
        relevant_videos = classify_videos(index_id, sub_topic, video_api_key)
        print(f"found {len(relevant_videos)} relevant videos for topic: {topic}, subtopic: {sub_topic}")
        if len(relevant_videos) == 0:
            continue
        for video in relevant_videos:
            video_id = video["video_id"]
            video_summary = summarize_video(video_id, video_api_key)
            print(f"generating transcript for topic: {topic}, length: {length}, level of detail: {level_of_detail} for video: {video_id}")
            transcript = generate_transcription(",".join(video_summary), topic, length, level_of_detail)

            print("generated")
            print(transcript)

            print("translating..")
            if(selected_language != "en"):
                transcript = GoogleTranslator(source='auto', target=selected_language).translate(transcript)  

            print("generating audio")
            audio = get_audio(transcript)
            transcript_hash = hashlib.md5(transcript.encode('utf-8')).hexdigest()
            audio_file_location = f"{topic}_{sub_topic}_{video_id}_{selected_language}_{transcript_hash}.mp3"
            list_of_audio_file_locations.append(audio_file_location)
            save(audio, audio_file_location)

    return list_of_audio_file_locations

if __name__ == "__main__":
    for language in ["en", "ko"]:
        print(f"generating audio for {language}..")
        # meditation_audio_files = main("meditation_config.json", "meditation", language)
        # leadership_audio_files = main("leadership_config.json", "leadership", language)
        heart_health_audio_files = main("heart_health_config.json", "heart_health", language)


