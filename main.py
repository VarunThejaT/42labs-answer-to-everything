import os
import openai
import argparse
import dotenv
import json
import requests
from eleven import get_audio
from gpt import make_class_prompt, make_transcription_prompt, generate_transcription, generate_classes

dotenv.load_dotenv()

# openai.organization = "org-5hbFMeJaQuatIgOn4ilTaMwN"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Model.list()
url = "https://api.twelvelabs.io/v1.1"
API_KEY = os.getenv("TWELVE_LABS_API_KEY")

def classify_videos(index_id, sub_topic):
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
        "x-api-key": API_KEY
    }

    response = requests.post(CLASSIFY_BULK_URL, headers=headers, json=data)
    print (f'Status code: {response.status_code}')
    print(response.json())
    return response.json()["data"]

def summarize_video(video_id):
    payload = {
        "type": "chapter",
        "video_id": video_id,
    }
    headers = {
        "accept": "application/json",
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    url = "https://api.twelvelabs.io/v1.2/summarize"
    response = requests.post(url, json=payload, headers=headers)

    print(response.text)
    chapter_summaries = [x["chapter_summary"] for x in response.json()["chapters"]]
    return chapter_summaries

def main():
    with open('config.json', 'r') as f:
        data = json.load(f)
    # print(data)
    payload = data['data']["leadership"] #leadership should be an input argument
    topic = payload["topic_name"]
    index_id = payload["index_id"]
    number_of_categories = "5"
    level_of_detail = payload["skill_level"]
    length = "1"
    gpt_model = "gpt-4-0314"
    # get_12_summary(payload)
    # classes_json = generate_classes(topic, number_of_categories, gpt_model)
    # classes_json = json.loads(classes_json)
    selected_subtopic = payload["selected_sub_topics"]
    list_of_audio_file_locations = []
    for sub_topic in selected_subtopic:
        relevant_videos = classify_videos(index_id, sub_topic)
        if len(relevant_videos) == 0:
            continue
        video_summaries = []
        for video in relevant_videos:
            video_id = video["video_id"]
            video_summaries += summarize_video(video_id)
        print("video summaries: ", video_summaries)
        print(f"generating transcript for topic: {topic}, length: {length}, level of detail: {level_of_detail}")
        transcript = generate_transcription(",".join(video_summaries), topic, length, level_of_detail)

        print("generated")
        print(transcript)

        print("reading")
        audio = get_audio([transcript])
        # save the audio to local file
        # host in s3 or locally and provide the end point in audio_file_location
        audio_file_location = ""
    return list_of_audio_file_locations

if __name__ == "__main__":
    main()