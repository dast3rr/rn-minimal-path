from flask import Flask, render_template

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from get_distances import get_path

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title="Главная")


@app.route('/about')
def about():
    return render_template('about.html', title="О нас")


@app.route('/first_method')
def first_method():
    return render_template('first_method.html', title="Первый метод")


@app.route('/second_method')
def second_method():
    return render_template('second_method.html', title="Второй метод")


if __name__ == "__main__":
    app.run(debug=True)