import os
import openai
import argparse
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

def make_transcription_prompt(video_summary, topic, name="David", length="1", level_of_detail="expert"):
    prompt = "below is the summary of all the content in a video related to "
    prompt+=topic 
    prompt+="\n based on this content, provide a transcription for a "
    prompt+=length
    prompt+=" minute personal podcast episode for "
    prompt+=name
    prompt+=" that covers this material"
    prompt+=" and generate it at an appropriate level of detail for a "
    prompt+=level_of_detail
    prompt+=". make sure to include the name "
    prompt+=name
    prompt+=" in the transcript. "
    prompt+="\n\n"
    prompt+=video_summary
    prompt+=""
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