from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # TODO: handle file upload and comparison
        pass

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
