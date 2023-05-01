import random
import string
import json
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)


#Connect to DB later, in memory for now
shortnedURLs = {}


def generateShortURL():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(6))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        shortURL = generateShortURL()
        shortnedURLs[shortURL] = url
        print(shortnedURLs)
        with open('shortnedURLs.json', 'w') as f:
            json.dump(shortnedURLs, f)
        return f"Shortned URL: {request.url_root}{shortURL}"
    return render_template('index.html')


@app.route('/<shortURL>')
def redirectShortURL(shortURL):
    longURL = shortnedURLs.get(shortURL)
    if longURL:
        return redirect(longURL, code=302)
    else:
        return f"URL doesn't exist", 404


if __name__ == '__main__':
    with open('shortnedURLs.json', 'r') as f:
        shortnedURLs = json.load(f)
    app.run(debug=True)



