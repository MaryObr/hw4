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



@app.route('/anketa')
def process():
    return render_template('anketa.html')



def info():
    age = request.args['age']
    place = request.args['place']
    gender = request.args['exampleRadios']
    tvo = request.args['tvo']
    od = request.args['od']
    pet = request.args['pet']
    teft = request.args['teft']
    norm = request.args['norm']
    with open("Data.txt", 'r+', encoding='utf8') as file:
        for i in (age, gender, tvo, od, pet, teft, norm, place):
            file.write(i)
            file.write("\n")
    return

@app.route('/process')
def stat():
    with open("Data.txt", 'r+', encoding='utf8') as file:
        age = []
        p = file.readlines()
        p = "".join(p)
        p = p.split("\n")
        for k in range(0, 100):
            i = k*8
            if i+1 < len(p):
                age.append(int(p[i]))
    # создание пай-чарта
    h = sorted(age)
    print(h)
    df = pd.DataFrame({'age': h})
    plt.figure(figsize=(6, 6))
    df['age'].value_counts().plot(kind='pie')
    plt.title('Распределение анкетируемых по возрасту')
    plt.savefig("/home/MaryObridko/mysite/flask/static/age.jpg")
    # определение ударений
    q = {}
    place = []
    with open("Data.txt", 'r+', encoding='utf8') as file:
        x = file.readlines()
        x = "".join(x)
        x = x.split("\n")
        for k in range(0, 100):
            i = 7 + (k * 8)
            if i < len(x):
                place.append(x[i])
    for i in place:
        if not q.get(i):
            q[i] = 1
        else:
            q[i] += 1
    towns = sorted(q.keys(), key=lambda x: q[x])
    slog = []
    od = []
    pet = []
    tvo = []
    teft = []
    norm = []
    with open("Data.txt", 'r+', encoding='utf8') as file:
        z = file.readlines()
        z = "".join(z)
        z = z.split("\n")
        for k in range(0, 100):
            i = 2 + (k*8)
            if i+4 < len(z):
                tvo.append(z[i])
                od.append(z[i+1])
                pet.append(z[i+2])
                teft.append(z[i+3])
                norm.append(z[i+4])
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
