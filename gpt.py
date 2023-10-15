import os
import openai
import argparse
# openai.organization = "org-5hbFMeJaQuatIgOn4ilTaMwN"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Model.list()


def make_prompt(topic, number_of_categories):

    prompt = "What are " + number_of_categories + "basic categories of" + topic + "knowledge that a university student studying " + topic + " should understand. Make them mutually exclusive and comprehensive."
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

def generate_classes(topic, number_of_categories="4", model="gpt-4-0314"):

    prompt = make_prompt(topic, number_of_categories)

    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )

    response_json = response["choices"][0]["message"]["content"]

    return(response_json)

# call open ai api and get completion for the following prompt
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", type=str, default="machine learning", help="topic")
    parser.add_argument("--number_of_categories", type=str, default="4", help="number of categories")
    parser.add_argument("--model", type=str, default="gpt-4-0314", help="model")
    args = parser.parse_args()

    topic = args.topic
    number_of_categories = args.number_of_categories
    model = args.model

    generate_classes(topic, number_of_categories, model)
