https://maryobridko.pythonanywhere.com/

Проект - сайт-выдача анекдотов по вводу персонажа. Сайт состоит из трех страниц и одной "аварийной")

Первая страница - объяснение возможностей сайта и анкета. Пользователь может выбрать персонажа из одной из популярных групп или ввести самому. 
Так же есть возможность убрать из выдачи неприличные анекдоты - они размечены машинкой на базе 100 заведомо неприличных анекдотов, 100 точно приличных и 150 размеченных мною.

В целом, анекдоты краулерами взяты с двух сайтов: 
https://colab.research.google.com/corgiredirector?site=https%3A%2F%2Fwww.anekdot.ru%2Frelease%2Fanekdot%2Fday%2F2020-02-06%2F 
и 
https://colab.research.google.com/corgiredirector?site=https%3A%2F%2Fanekdoty.ru%2F
а также книги анекдотов Юрия Никулина.

Я отбирала анекдоты из разделов с персонажами, а так же nlp поиском имен собственных, конкретныз названий национальностей.
Анекдоты были собраны в датасет, размечены на приличность. По пользовательскому запросу собираются все формы парадигмы слова,  в выдачу собираются все анекдоты, где есть хотя бы одна.

Вторая страница сайта - выдача анекдотов по запросу в виде карточек. Так же на этой странице можно скачать выдачу и перейти на статистику.
Третья страница - столбцовая диаграмма 5 самых популярных персонажей, pie chart соотношения цензурируемых и нет запросов. Также на странице информация о самом популярном и непопулярном
персонажах, о том, что чаще выбирают пользователи - все анекдоты или только приличные.
