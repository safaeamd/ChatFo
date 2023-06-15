import gradio as gr
import requests
import json
import openai
import re

from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools

# Define your OpenAI API key and endpoint
API_KEY = "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"
API_ENDPOINT = "https://api.openai.com/v1/engines/whisper/betas/0.3.0/completions"


def generate_form(text, n):
    openai.api_key = API_KEY
    content = text + f""" The quiz should contain {n} questions with multiple choice answers in the same format as the following, and in the end write finished : 
        Title of quiz : "quiz on ..." 
    Question 1 : ....
        a.  
        b.  
        c.
        d.
    Question 2 : ....
        a. 
        b. 
        c. 
        d. 
    """

    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": content}])
    response = completion.choices[0].message.content

    # Parsing the result
    Title = re.findall(r'Quiz on (.*?)\n', response)
    questions = re.findall(r'Question \d+: (.*?)\n', response)

    a_answers = re.findall(r'a\.(.*?)\n', response)
    b_answers = re.findall(r'b\.(.*?)\n', response)
    c_answers = re.findall(r'c\.(.*?)\n', response)
    d_answers = re.findall(r'd\.(.*?)\n', response)

    q = []

    for i in range(n):
        q.append({
            "createItem": {
                "item": {
                    "title": questions[i],
                    "questionItem": {
                        "question": {
                            "required": True,
                            "choiceQuestion": {
                                "type": "RADIO",
                                "options": [
                                    {"value": a_answers[i]},
                                    {"value": b_answers[i]},
                                    {"value": c_answers[i]},
                                    {"value": d_answers[i]}
                                ],
                                "shuffle": True
                            }
                        }
                    },
                },
                "location": {
                    "index": i
                }
            }
        })

    SCOPES = "https://www.googleapis.com/auth/forms.body"
    DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

    store = file.Storage('token.json')
    creds = None
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('key.json', SCOPES)
        creds = tools.run_flow(flow, store)

    form_service = discovery.build('forms', 'v1', http=creds.authorize(Http()), discoveryServiceUrl=DISCOVERY_DOC,
                                   static_discovery=False)

    # Request body for creating a form
    NEW_FORM = {
        "info": {
            "title": Title[0],
        }
    }

    # Request body to add a multiple-choice question
    NEW_QUESTION = {
        "requests": q
    }

    # Creates the initial form
    result = form_service.forms().create(body=NEW_FORM).execute()

    # Adds the question to the form
    question_setting = form_service.forms().batchUpdate(formId=result["formId"], body=NEW_QUESTION).execute()

    # Prints the result to show the question has been added
    get_result = form_service.forms().get(formId=result["formId"]).execute()
    return get_result["responderUri"]


def main(transcription, n):
    link = generate_form(transcription, n)
    return link


iface = gr.Interface(
    fn=main,
    inputs=["text", "number"],
    outputs="text",
    title="Text ChatGPT To Quiz Form",
    description="Generate a quiz form from text",
    examples=[["Enter the text for the quiz questions", 10]]
)

if __name__ == "__main__":
    iface.launch(share=True)
