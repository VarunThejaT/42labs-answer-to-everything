# video_id = 652b1e2a43e8c47e4eb480c9
# video_id = 652af12743e8c47e4eb48056

import requests
import dotenv
import os

dotenv.load_dotenv()
API_KEY = os.getenv("TWELVE_LABS_API_KEY")


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

rv = summarize_video("652af12743e8c47e4eb48056")
print(rv)
