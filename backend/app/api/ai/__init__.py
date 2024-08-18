import os
import re
import numpy
import pathlib
import requests

API_URL = os.environ["HUGGING_FACE_API_URL"]
headers = {"Authorization": "Bearer " + os.environ["HUGGING_FACE_API_KEY"]}
PATH = os.environ["RESOURCE_PATH"]


# load FAQs from the external file
content = pathlib.Path(PATH).read_text(encoding="utf-8")

# initialize a dictionary object that will hold the faqs
knowledge_base = {}


def convert_faqs(content):
    """
    Convert FAQs text content to a python dictionary for efficient manipulation.
    The FAQ becomes the key and its given answer becomes the value
    """
    lines = content.split("\n")
    question = ""
    answer = ""

    for line in lines:
        if re.match(r"^\d+\.", line.strip()):
            if question and answer:
                knowledge_base[question.strip()] = answer.strip()
            question = line.strip()
            answer = ""
        else:
            answer += line + " "

    if question and answer:
        knowledge_base[question.strip()] = answer.strip()


# load processed FAQs
convert_faqs(content)


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


def get_best_matched_question(user_input):
    """Return the best matched question from the knowledge-base"""
    faqs = list(knowledge_base.keys())

    output = query(
        {
            "inputs": {
                "source_sentence": user_input,
                "sentences": faqs,
            },
        }
    )

    matched_question_index = numpy.argmax(output)

    return faqs[matched_question_index]


def fetch_bot_response(user_input):
    """Get the AI model response that best matches the user's question"""
    matched_question = get_best_matched_question(user_input)
    return knowledge_base[matched_question] if matched_question else "No response"
