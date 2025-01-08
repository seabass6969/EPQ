import os
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def mainPage():
    return render_template(os.path.join('index.html', ""))

if __name__ == "__main__": 
    app.run(debug=True)
