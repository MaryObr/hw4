import matplotlib
import pandas as pd

from flask import Flask
from flask import render_template
from flask import request
import matplotlib.pyplot as plt

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('main_fl.html')


age = []
place = []
gender = []
tvo = []
od = []
pet = []
teft = []
norm = []


@app.route('/anketa')
def process():
    return render_template('anketa.html')


@app.route('/process')
def stat():
    global age
    global place
    global gender
    global tvo
    global od
    global pet
    global teft
    global norm
    age.append(request.args['age'])
    place.append(request.args['place'])
    gender.append(request.args['exampleRadios'])
    tvo.append(request.args['tvo'])
    od.append(request.args['od'])
    pet.append(request.args['pet'])
    teft.append(request.args['teft'])
    norm.append(request.args['norm'])
    # создание пай-чарта
    h = sorted(age)
    df = pd.DataFrame({'age': h})
    plt.figure(figsize=(6, 6))
    df['age'].value_counts().plot(kind='pie')
    plt.title('Распределение анкетируемых по возрасту')
    plt.savefig("/home/MaryObridko/mysite/flask/static/age.jpg")
    q = {}
    for i in place:
        if not q.get(i):
            q[i] = 1
        else:
            q[i] += 1
    towns = sorted(q.keys(), key=lambda x: q[x])
    slog = []
    for i in [tvo, od, pet, teft, norm]:
        if i.count('2') > i.count("1"):
            slog.append("2")
        elif i.count("1") > i.count('2'):
            slog.append("1")
        else:
            slog.append("безразлично какой")
    return render_template("stats.html", count=len(tvo), max=h[-1], min=h[0],
                           city=towns[-1], tv=slog[0], od=slog[1], pet=slog[2], teft=slog[3], norm=slog[4])


if __name__ == '__main__':
    app.run()
