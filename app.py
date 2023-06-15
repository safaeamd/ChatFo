from flask import Flask, render_template, request, jsonify
import gradio as gr
import openai
 
app = Flask(__name__)
app.static_folder = 'static'  # Set the static folder for serving static files

# Initialize the OpenAI API client
openai.api_key = "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"

def chatbot_interface(question):
    # Code for interacting with the ChatGPT model and generating the exam
    # Replace this with your actual implementation
    # Example placeholder code
    response = openai.Completion.create(
        engine="text-davinci-003",  # Replace with the actual GPT model name
        prompt=question,
        max_tokens=100,
        n=1,
        stop=None,
    )

    exam = response.choices[0].text.strip()
    return examw

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/process_question", methods=["POST"])
def process_question():
    question = request.form["question"]
    exam = chatbot_interface(question)
    return jsonify({'exam': exam})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
