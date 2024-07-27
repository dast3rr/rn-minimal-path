from flask import Flask, render_template, request

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from get_distances import get_path
from forms.first_method import FirstMethodForm

app = Flask(__name__)
app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

@app.route('/')
def index():
    return render_template('index.html', title="Главная")


@app.route('/about')
def about():
    return render_template('about.html', title="О нас")


@app.route('/first_method', methods=['GET', 'POST'])
def first_method():
    azs_list = []
    with open('points.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            azs_list.append(line.strip())
    

    form = FirstMethodForm()
    form.set_choices(azs_list)
    if request.method == 'POST':
        print(form.azs.data)
    return render_template('first_method.html', title="Первый метод", npzs=['a', 'b'], azs_list=azs_list, form=form)


@app.route('/first_method_result', methods=['GET', 'POST'])
def first_method_result():
    points = []
    print(request.form['first_choice'])
    return render_template('first_method_result.html', title="Результаты первого")


@app.route('/second_method')
def second_method():
    return render_template('second_method.html', title="Второй метод")


if __name__ == "__main__":
    app.run(debug=True)