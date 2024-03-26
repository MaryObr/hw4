import sqlite3
import pandas as pd
conn = sqlite3.connect("anekdotes.db", check_same_thread=False)
c = conn.cursor()


from flask import Flask
from flask import render_template
from flask import request
from flask import send_file
import matplotlib.pyplot as plt
from pymorphy2 import MorphAnalyzer

morph = MorphAnalyzer()

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('anek1.html')



@app.route('/process')
def search():
    try:
        word = request.args['T2']
        people = [word]
        try:
            apro = request.args['tvo']
        except KeyError:
            apro = 0
        try:
            w = request.args['exampleRadios']
            if w == "Прав":
                people = ['Ленин', 'Сталин', 'Хрущев', 'Брежнев', 'Горбачев', 'Ельцин', 'Путин', 'Медведев']
            elif w == "нац":
                people = ['русский', 'американец', 'француз', 'еврей', "чукча", 'грузин', 'хохол', 'эстонский парень',
                          'эстонец']
            elif w == "вова":
                people = ["Вовочка"]
            elif w == "блонд":
                people = ["Блондинка"]
            elif w == "штир":
                people = ["Штирлиц"]
            elif w == "семья":
                people = ["муж", "жена", 'отец', 'мать', 'сын', "дочь", 'тёща', 'зять', 'свекровь', 'золовка', 'брат',
                          'сестра']
        except KeyError:
            pass
        # записываем данные в файлик
        with open("stat.txt", 'a+', encoding='utf8') as f:
            if apro == 0:
                f.write("Все анекдоты")
                f.write("\n")
            else:
                f.write("Только приличные")
                f.write("\n")
            f.write(" ".join(people))
            f.write("\n")
        l = []
        for i in people:
            word = morph.parse(i)[0]
            lex = word.lexeme
            for j in lex:
                l.append(j.word)
        if apro == 1:
            query = """
            SELECT text_22
            FROM Anek22
            WHERE pril_22 = 0
            """
            df0 = pd.read_sql_query(query, con=conn)
            query1 = """
            SELECT text
            FROM Anek11
            WHERE pril = 0
            """
            df1 = pd.read_sql_query(query1, con=conn)
            query2 = """
            SELECT text_n
            FROM Nikulin
            WHERE pril_n = 0
            """
            df2 = pd.read_sql_query(query2, con=conn)
            data = [df0, df1, df2]
            df = pd.concat(data)
            final = []
            r = ["text_22"]
            for j in r:
                for q in list(df[j]):
                    for k in l:
                        if (k + " ") in str(q) and str(q) not in final:
                            final.append(str(q))
        else:
            query = """
            SELECT text_22
            FROM Anek22
            """
            df0 = pd.read_sql_query(query, con=conn)
            query1 = """
            SELECT text
            FROM Anek11
            """
            df1 = pd.read_sql_query(query1, con=conn)
            query2 = """
            SELECT text_n
            FROM Nikulin
            """
            df2 = pd.read_sql_query(query2, con=conn)
            data = [df0, df1, df2]
            df = pd.concat(data)
            final = []
            r = ["text_22", "text_n", "text"]
            for j in r:
                for q in list(df[j]):
                    for k in l:
                        if (k.lower() + " ") in str(q).lower():
                            we = str(q).replace("\n", "")
                            if we not in final:
                                final.append(we.replace(
                                    "100 лучших книг всех времен: www.100bestbooks.ru Юрий Никулин «Анекдоты от Никулина»",
                                    ""))
        if len(final) == 0:
            final = "К сожалению, анекдотов с этим персонажем нет, попробуйте найти другого"
        with open("/home/MaryObridko/flask/anek.txt", "w", encoding='utf8') as file:
            if type(final) != str:
                for i in final:
                    file.write(str(i))
                    file.write("______________________________________________")
                    file.write("\n")
            else:
                file.write(final)
                file.write("______________________________________________")
        return render_template("Anek2.html", anek=final)
    except KeyError:
        return render_template("Anek4.html")


@app.route('/stat')
def stats():
    with open("/home/MaryObridko/flask/stat.txt", 'r+', encoding='utf8') as f:
        p = f.readlines()
        pri = p[::2]
        names = p[1::2]
    ann = ""
    if pri.count("Все анекдоты\n") > pri.count("Только приличные\n"):
        ann = "все анекдоты"
    elif pri.count("Только приличные\n") > pri.count("Все анекдоты\n"):
        ann = "только приличные"
    else:
        ann = "оба варианта одинаково"
    df = pd.DataFrame({'pril': pri})
    plt.figure(figsize=(6, 8))
    df['pril'].value_counts().plot(kind='pie')
    plt.title('Выбор всех анекдотов или только приличных')
    plt.savefig("static/pril.jpg")
    # картинка для персонажей
    na = []
    for i in names:
        na.extend(i.split())
    pers = {}
    for i in na:
        if i not in pers.keys():
            pers[i] = 0
        else:
            pers[i] +=1
    leute = list(sorted(pers.keys(), key=lambda j: pers[j], reverse=True))
    num = []
    for i in leute[:5]:
        num.append(pers[i])
    plt.figure(figsize=(6, 6))
    plt.bar(leute[:5], num, color='darkorange')
    plt.title('5 самых популярных персонажей')
    plt.xlabel('Самые популярные персонажи')
    plt.ylabel('Количество запросов')
    plt.savefig("static/leute.jpg")
    return render_template("Anek3.html", pop=leute[0], lox=leute[-1], ane=ann)

@app.route('/return-files/')
def return_files_tut():
		return send_file('/home/MaryObridko/flask/anek.txt', as_attachment=True)



if __name__ == '__main__':
    app.run(debug=True)
# сделать карточки покрасивее
# разобраться с оглавлением, дать скачивать анекдоты
