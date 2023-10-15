import requests
import json
import dotenv
import os

dotenv.load_dotenv()

url = "https://api.twelvelabs.io/v1.1"
API_KEY = os.getenv("TWELVE_LABS_API_KEY")

user_input = {
    "topic" : "leadership",
    "skill" : "beginner"
}

skills = ["beginner", "intermediate", "advanced"]

def get_subtopics(topic):
    with open('config.json', 'r') as f:
        data = json.load(f)
    return data.data[topic]

# The user sends us back selected sub topics 

def get_12_summary(topic_payload):
    
    subtopics = topic_payload["selected_sub_topics"] #TODO: replace with user selected subtopics instead
    index = topic_payload["index_id"]

    # create query from selected subtopics
    query = "give me a summary for " + ", ".join(subtopics) + " in " + topic_payload["topic_name"]

    payload = {
        "search_options": ["conversation", "text_in_video"],
        "group_by": "clip",
        "threshold": "low",
        "sort_option": "score",
        "operator": "or",
        "conversation_option": "semantic",
        "page_limit": 10,
        "query": query,
        "index_id": index
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }

    response = requests.post(url + "/search", json=payload, headers=headers)
    print(response.text)

def classify_videos(index_id):
    CLASSIFY_BULK_URL = f"{url}/classify/bulk"

    data =  {
    "options": ["conversation", "text_in_video"],
    "index_id": index_id,
    "classes": [
        {
        "name": "leadership",
        "prompts": [
            "leadership",
        ]
        }
    ]
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }

    response = requests.post(CLASSIFY_BULK_URL, headers=headers, json=data)
    print (f'Status code: {response.status_code}')
    print(response.json())

def main():
    with open('config.json', 'r') as f:
        data = json.load(f)
    # print(data)
    payload = data['data']["leadership"] #leadership should be an input argument
    # get_12_summary(payload)
    classify_videos(data['data']["leadership"]["index_id"])
    return None

if __name__ == "__main__":
    main()