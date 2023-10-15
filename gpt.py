import os
import openai
import argparse
import dotenv
dotenv.load_dotenv()

# openai.organization = "org-5hbFMeJaQuatIgOn4ilTaMwN"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Model.list()


def make_class_prompt(topic, number_of_categories):

    prompt = "What are " + number_of_categories + " categories of " + topic + " knowledge that a university student studying " + topic + " should understand. Make them mutually exclusive and comprehensive."
    prompt += """
Provide a JSON output according to the following instructions. Include nothing else

Here is the content from the site. The following parameters allow you to control how classification works:

classes: An array of objects containing the names and definitions of the entities or actions that the platform must identify. Each object is composed of the following fields:
name: A string representing the name you want to give this class.
prompts: An array of strings that specifies what the class contains. The platform uses the values you provide in this array to classify your videos.
Example of using a simple taxonomy system:

Example of using a hierarchical taxonomy system:

JSON

{
	"classes": [
		{
			"name": "Attractions",
			"prompts": [
				"Amusement and Theme Parks",
				"Bars and Restaurants"
			]
		},
		{
			"name": "Education",
			"prompts": [
				"Primary Education",
				"Secondary Education"
			]
		}
	]
}
"""
    return prompt

def make_transcription_prompt(video_summary, topic, subtopic, length="1", level_of_detail="expert"):
    prompt = f"""
        You are assigned as to write for a mini {length} minute podcast episode on {topic}. Follow the following steps:
        1. Read the video summaries below that explore {topic}
        2. Pay special attention to portions related to {subtopic}
        3. Write the dialogue for a {length} podcast episode that covers this material and generate it at an appropriate level of detail for a {level_of_detail} in the transcript.
        4. include necessary details or extensions, but only if useful for a {level_of_detail}
        5. respond with the dialogue for the podcast episode

        Video summaries:
        {video_summary}
    """
    return prompt

def generate_transcription(video_summary, topic, length="1", level_of_detail="beginner", model="gpt-4-0314"):

    prompt = make_transcription_prompt(video_summary, topic, length, level_of_detail)

    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )

    response_transcription = response["choices"][0]["message"]["content"]

    return(response_transcription)

def generate_classes(topic, number_of_categories="5", model="gpt-4-0314"):

    prompt = make_class_prompt(topic, number_of_categories)

    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )

    response_json = response["choices"][0]["message"]["content"]

    return(response_json)

# call open ai api and get completion for the following prompt
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", type=str, default="leadership", help="topic")
    parser.add_argument("--number_of_categories", type=str, default="5", help="number of categories")
    parser.add_argument("--model", type=str, default="gpt-4-0314", help="model")
    parser.add_argument("--summary_file", type=str, default="summary.txt", help="summary file")
    args = parser.parse_args()

    topic = args.topic
    number_of_categories = args.number_of_categories
    model = args.model
    summary_file = args.summary_file
    summary = open(summary_file, "r").read()

    # classes_json = generate_classes(topic, number_of_categories, model)

    # print(classes_json)

    transcript = generate_transcription(summary, topic, model=model)

    print(transcript)