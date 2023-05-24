from flask import Flask, request, render_template, redirect, url_for
from aitextgen import aitextgen
import re

# Set up Flask app
app = Flask(__name__)

# Load pre-trained AI model
ai = aitextgen(model_folder=r"trained_model_twitterv5", to_gpu=False)

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/generate", methods=['POST', 'GET'])
def generate():
    if request.method == 'POST':
        # Get user input from form 
        prompt = request.form['textbox']
        subprompt = prompt + "."
        # Generate text using AI model
        text = ai.generate_one(prompt=subprompt, max_length=25, temperature=1, top_p=1)
        text2 = ai.generate_one(prompt=subprompt, max_length=25, temperature=1, top_p=1)
        text3 = ai.generate_one(prompt=subprompt, max_length=25, temperature=1, top_p=1)
        # Render results template with generated text
        return redirect(url_for('results', text=text, prompt=prompt, text2=text2, text3=text3))


@app.route('/results')
def results():
    text = request.args.get('text')
    text2 = request.args.get('text2')
    text3 = request.args.get('text3')
    prompt = request.args.get('prompt')
    text = re.sub(prompt + ". ", "", text)
    text2 = re.sub(prompt + ". ", "", text2)
    text3 = re.sub(prompt + ". ", "", text3)

    return render_template('results.html', text=text, text2=text2, text3=text3, prompt=prompt)

@app.route('/help_redirect')
def help_redirect():
    return render_template('video.html')

if __name__ == '__main__':
    app.run(debug=True)