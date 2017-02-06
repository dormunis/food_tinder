from flask import Flask, render_template

app = Flask("FoodTinder")


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')