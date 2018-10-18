"""
== OpenWeatherMap ==
OpenWeatherMap — онлайн-сервис, который предоставляет бесплатный API
 для доступа к данным о текущей погоде, прогнозам, для web-сервисов
 и мобильных приложений. Архивные данные доступны только на коммерческой основе.
 В качестве источника данных используются официальные метеорологические службы
 данные из метеостанций аэропортов, и данные с частных метеостанций.
Необходимо решить следующие задачи:
== Получение APPID ==
    Чтобы получать данные о погоде необходимо получить бесплатный APPID.

    Предлагается 2 варианта (по желанию):
    - получить APPID вручную
    - автоматизировать процесс получения APPID,
    используя дополнительную библиотеку GRAB (pip install grab)
        Необходимо зарегистрироваться на сайте openweathermap.org:
        https://home.openweathermap.org/users/sign_up
        Войти на сайт по ссылке:
        https://home.openweathermap.org/users/sign_in
        Свой ключ "вытащить" со страницы отсюда:
        https://home.openweathermap.org/api_keys

        Ключ имеет смысл сохранить в локальный файл, например, "app.id"

== Получение списка городов ==
    Список городов может быть получен по ссылке:
    http://bulk.openweathermap.org/sample/city.list.json.gz

    Далее снова есть несколько вариантов (по желанию):
    - скачать и распаковать список вручную
    - автоматизировать скачивание (ulrlib) и распаковку списка
     (воспользоваться модулем gzip
      или распаковать внешним архиватором, воспользовавшись модулем subprocess)

    Список достаточно большой. Представляет собой JSON-строки:
{"_id":707860,"name":"Hurzuf","country":"UA","coord":{"lon":34.283333,"lat":44.549999}}
{"_id":519188,"name":"Novinki","country":"RU","coord":{"lon":37.666668,"lat":55.683334}}


== Получение погоды ==
    На основе списка городов можно делать запрос к сервису по id города. И тут как раз понадобится APPID.
        By city ID
        Examples of API calls:
        http://api.openweathermap.org/data/2.5/weather?id=2172797&appid=b1b15e88fa797225412429c1c50c122a
    Для получения температуры по Цельсию:
    http://api.openweathermap.org/data/2.5/weather?id=520068&units=metric&appid=b1b15e88fa797225412429c1c50c122a
    Для запроса по нескольким городам сразу:
    http://api.openweathermap.org/data/2.5/group?id=524901,703448,2643743&units=metric&appid=b1b15e88fa797225412429c1c50c122a
    Данные о погоде выдаются в JSON-формате
    {"coord":{"lon":38.44,"lat":55.87},
    "weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04n"}],
    "base":"cmc stations","main":{"temp":280.03,"pressure":1006,"humidity":83,
    "temp_min":273.15,"temp_max":284.55},"wind":{"speed":3.08,"deg":265,"gust":7.2},
    "rain":{"3h":0.015},"clouds":{"all":76},"dt":1465156452,
    "sys":{"type":3,"id":57233,"message":0.0024,"country":"RU","sunrise":1465087473,
    "sunset":1465149961},"id":520068,"name":"Noginsk","cod":200}
== Сохранение данных в локальную БД ==
Программа должна позволять:
1. Создавать файл базы данных SQLite со следующей структурой данных
   (если файла базы данных не существует):
    Погода
        id_города           INTEGER PRIMARY KEY
        Город               VARCHAR(255)
        Дата                DATE
        Температура         INTEGER
        id_погоды           INTEGER                 # weather.id из JSON-данных
2. Выводить список стран из файла и предлагать пользователю выбрать страну
(ввиду того, что список городов и стран весьма велик
 имеет смысл запрашивать у пользователя имя города или страны
 и искать данные в списке доступных городов/стран (регуляркой))
3. Скачивать JSON (XML) файлы погоды в городах выбранной страны
4. Парсить последовательно каждый из файлов и добавлять данные о погоде в базу
   данных. Если данные для данного города и данного дня есть в базе - обновить
   температуру в существующей записи.
При повторном запуске скрипта:
- используется уже скачанный файл с городами;
- используется созданная база данных, новые данные добавляются и обновляются.
При работе с XML-файлами:
Доступ к данным в XML-файлах происходит через пространство имен:
<forecast ... xmlns="http://weather.yandex.ru/forecast ...>
Чтобы работать с пространствами имен удобно пользоваться такими функциями:
    # Получим пространство имен из первого тега:
    def gen_ns(tag):
        if tag.startswith('{'):
            ns, tag = tag.split('}')
            return ns[1:]
        else:
            return ''
    tree = ET.parse(f)
    root = tree.getroot()
    # Определим словарь с namespace
    namespaces = {'ns': gen_ns(root.tag)}
    # Ищем по дереву тегов
    for day in root.iterfind('ns:day', namespaces=namespaces):
        ...
"""
import json
import gzip
import urllib.request
import shutil
import os
import sqlite3
import tkinter
import time
from tkinter import RIGHT, BOTH, SE, END


# Constants
ROOT_SIZE = '760x500'
ROOT_TITLE = 'ПОГОДА'
BORDER = 10
CITY_URL = 'http://bulk.openweathermap.org/sample/city.list.json.gz'
ID = 'ad4a7fee99ae2c4be56dd6d0161975a0'
CURENT_DIR = os.getcwd()


class CityBase:

    def __init__(self):
        self.url = 'http://bulk.openweathermap.org/sample/city.list.json.gz'
        self._name_gz = 'city.gz'
        self._name_json = 'city.json'
        if os.name == 'posix':
            delimiter = '/'
        else:
            delimiter = '\\'
        self.full_name = os.getcwd() + delimiter + self._name_gz
        self.name_base_json = os.getcwd() + delimiter + self._name_json

    def is_downloaded(self):
        check = os.path.isfile(self.full_name)
        return check

    def check_size(self):                      # Возвращает TRUE если размер базы в интернете равен уже скаченной базе
        if self.is_downloaded():
            try:
                url = urllib.request.urlopen(self.url)
                size_url = int(url.getheader("Content-Length"))
                file_size = int(os.path.getsize(self.full_name))
                if size_url == file_size:
                    return True
                else:
                    return False
            except Exception:
                print('Нет соединения с интернетом')

    def download_file(self):
        try:
            urllib.request.urlretrieve(self.url, self._name_gz)
            with urllib.request.urlopen(self.url) as response, open(self._name_gz, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
        except Exception:
            print('Нет соединения с инетом')

    def unzip_file(self):
        with gzip.open(self.full_name) as file_in:
            with open(self.name_base_json, 'wb') as file_out:
                shutil.copyfileobj(file_in, file_out)

    def _create_dict(self):
        file = open(self.name_base_json)
        city_dict = json.load(file)
        file.close()
        return city_dict

    def create_base(self):
        try:
            if self.is_downloaded() is not True or self.check_size() is not True:
                self.download_file()
                self.unzip_file()
                print('file download')
                return self._create_dict()
            else:
                return self._create_dict()
        except Exception:
            print('Нет соединения с...')


class SqlBase:

    def __init__(self):
        self._name = 'main.db'
        self._city_table = 'city_table'
        self.path = os.getcwd()
        if os.name == 'posix':
            delimiter = '/'
        else:
            delimiter = '\\'
        self._name_long = '{}{}www.artlebedev.ru.txt'.format(self.path, delimiter)
        self.url_name_country = 'https://www.artlebedev.ru/country-list/tab/'

    def create_sql(self, city_dict):
        check = os.path.isfile(os.getcwd() + '/' + self._name)
        if check is False:
            sql = sqlite3.connect(self._name)
            c = sql.cursor()
            c.execute('CREATE TABLE {} (id_города INTEGER PRIMARY KEY, '
                      'Город VARCHAR(128), '
                      'Страна VARCHAR(45))'.format(self._city_table))

            for city in city_dict:
                id_city = city['id']
                name = city['name']
                country = city['country']
                if country != '':
                    c.execute('INSERT INTO {} VALUES ({},  "{}", "{}")'.format(self._city_table, id_city, name, country))
            sql.commit()
            sql.close()

    # вот тут пишу функцию записи данных в базу....
    def weather_data(self, data, id_city, name, temp, id_weather):

        sql = sqlite3.connect(self._name)
        c = sql.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS weather '
                  '(data INTEGER, '
                  'id_city INTEGER, '
                  'name VARCHAR(128), '
                  'temp VARCHAR(45), '
                  'id_weather)')
        check = c.execute("SELECT * FROM weather WHERE data='{}' AND id_city='{}'".format(data, id_city))
        check = check.fetchall()

        if check:
            data = time.ctime(check[0][0])
            result_print = 'Дата: {} |ID: {} |Город: {} |Темература: {} |ID_погоды: {}'.format(data, check[0][1], check[0][2], check[0][3], check[0][4])
            sql.close()
            return result_print
        else:
            c.execute('INSERT INTO weather VALUES ({},  {}, "{}", {}, {})'.format(data, id_city, name, temp, id_weather))
            data = time.ctime(data)
            result_print = 'Дата: {} |ID: {} |Город: {} |Темература: {} |ID_погоды: {}'.format(data, id_city, name, temp, id_weather)
            sql.commit()
            sql.close()
            return result_print

    def get_weather_from_sql(self, id_city):

        sql = sqlite3.connect(self._name)
        c = sql.cursor()
        check = c.execute("SELECT * FROM weather WHERE id_city='{}' ORDER BY data DESC LIMIT 1 ".format(id_city))
        check = check.fetchall()

        if check:
            data = time.ctime(check[0][0])
            result_print = 'Дата: {} |ID: {} |Город: {} |Темература: {} |ID_погоды: {}'.format(data, check[0][1],
                                                                                               check[0][2], check[0][3],
                                                                                               check[0][4])
            sql.close()
            return result_print
        else:
            sql.close()
            return 'В базе нет данных по выбранному городу'

    def history(self, id_city):

        sql = sqlite3.connect(self._name)
        c = sql.cursor()
        check = c.execute("SELECT * FROM weather WHERE id_city='{}' ORDER BY data".format(id_city))
        check = check.fetchall()
        result_print=[]
        if check:
            for request in check:
                data = time.ctime(request[0])
                result_print.append('Дата: {} |ID: {} |Город: {} |Темература: {} |ID_погоды: {}'.format(data, request[1], request[2], request[3], request[4]))
            sql.close()
            return result_print
        else:
            sql.close()
            return 'В базе нет данных по выбранному городу'

    def country_list(self):

        sql = sqlite3.connect(self._name)
        c = sql.cursor()
        all_country = c.execute('SELECT DISTINCT Страна FROM {}'.format(self._city_table))
        all_country = all_country.fetchall()
        list_country = []
        for country in all_country:
            list_country.append(country[0])
        sql.close()
        return list_country

    def city_list(self, country):
        sql = sqlite3.connect(self._name)
        c = sql.cursor()
        list_city = []
        all_city = c.execute("SELECT * FROM {} WHERE Страна='{}' ORDER BY Город".format(self._city_table, country))
        all_city = all_city.fetchall()
        for city in all_city:
            list_city.append(city)
        sql.close()
        return list_city

    def full_name(self):

        if os.path.isfile(os.getcwd()+self._name_long) is not True:
            try:
                urllib.request.urlretrieve(self.url_name_country, self._name_long)
                with urllib.request.urlopen(self.url_name_country) as response, open(self._name_long, 'wb') as out_file:
                    shutil.copyfileobj(response, out_file)
            except Exception:
                print('Нет соединения с инетом')

        file = open(self._name_long)
        i = 0
        short = []
        long = []
        for line in file:
            i += 1
            buffer = line.split('\t')
            if i > 1:
                long.append(buffer[2])
                short.append(buffer[3])
        dict_country = dict(zip(short, long))
        return dict_country


    def sort_country(self):

        long_name_list = []
        country_dict = self.full_name()
        short_name_list = self.country_list()
        unknown_country = []
        for short in short_name_list:
            try:
                long_name_list.append(country_dict[short])
            except KeyError:
                unknown_country.append(short)
        long_name_list = sorted(long_name_list, key=str.lower)
        return long_name_list


class Gui(tkinter.Tk):

    def __init__(self, master=None):
        tkinter.Tk.__init__(self, master)
        self.title(ROOT_TITLE)
        self.geometry('{}{}'.format(ROOT_SIZE, self.get_center()))
        self.quit_button = tkinter.Button(self, text='Quit', command=self.quit)
        self.clear_button = tkinter.Button(self, text='Clear', command=self.clear)
        self.label_country = tkinter.Label(self, text='Country:', width=7, height=1)
        self.listbox_country = tkinter.Listbox(self)
        self.label_city = tkinter.Label(self, text='City:', width=4, height=1)
        self.listbox_city = tkinter.Listbox(self, width=30)
        self.choice_listbox = tkinter.Listbox(self, width=30)
        self.start_button = tkinter.Button(self, text='<<< start >>>', width=75, height=2, command=self.start)
        self.history_button = tkinter.Button(self, text='history', width=8, height=2, command=self.history)
        self.labelframe = tkinter.LabelFrame(self, text='result', width=900, height=200)
        self.result_frame = tkinter.Listbox(self.labelframe, width=88)
        self.del_button = tkinter.Button(self, text='<=', width=2, height=2, command=self.delete)
        self.choice_button = tkinter.Button(self, text='=>', width=2, height=2, command=self.add_city)
    # Создание объектов других классов
        self.city = CityBase()
        self.sql_base = SqlBase()
        self.country_dict = self.sql_base.full_name()
        city_dict = self.city.create_base()
        self.sql_base.create_sql(city_dict)
        self._country_list = self.sql_base.country_list()
        self._sort_country = self.sql_base.sort_country()
    # Внутренние константы
        self.added_city = []
        self._idx_country = 0
        self._idx_city = 0
        self.cities_dict = {}
        self.city_list = []
        self._short = ''
        self._choice_country = ''    # Это потом перезапишится при выполнения функции
        self._choice_city = ''
        self.choice_value = 0

        self.create_widget()
        self.listbox_country.bind("<<ListboxSelect>>", self.get_country)
        self.listbox_city.bind("<<ListboxSelect>>", self.choice_city)
        self.choice_listbox.bind("<<ListboxSelect>>", self.del_city)

    def start(self):

        list_choice = self.choice_listbox.get(0, END)
        for i in list_choice:
            name, id_city = i.split(';')
            url_weather = 'http://api.openweathermap.org/data/2.5/weather?id={}&units=metric&appid={}'.format(id_city, ID)
            try:
                with urllib.request.urlopen(url_weather) as buffer:
                    weather = json.load(buffer)
                    # Выдергиваем нужные значения (id_погоды, дата, температура) из словаря с сервера и раскладываем по переменным)
                    id_weather = weather['weather'][0]['id']
                    data_time = weather['dt']
                    temp = weather['main']['temp']
                result = self.sql_base.weather_data(data_time, id_city, name, temp, id_weather)
                self.result_frame.insert(END, result)
            except Exception:
                self.result_frame.insert(0, 'Нет соединения с интернетом')
                result = self.sql_base.get_weather_from_sql(id_city)
                self.result_frame.insert(END, result)


    def del_city(self, val):

        sender = val.widget
        try:
            self.choice_value = sender.curselection()[0]
        except IndexError:
            pass  # переключение между Listbox вызывает глюк с незнакомым индекосм списка, поэтому завернул в pass
        except UnboundLocalError:
            pass

    def delete(self):

            try:
                self.choice_listbox.delete(self.choice_value)
            except IndexError:
                pass

    def add_city(self):

        list_choice = self.choice_listbox.get(0, END)
        if self._choice_city not in list_choice:
            self.choice_listbox.insert(END, self._choice_city)

    def choice_city(self, val):

        sender = val.widget
        try:
            self._idx_city = sender.curselection()[0]
        except IndexError:
            print('переключение между Listbox')
        value = sender.get(self._idx_city)
        self._choice_city = value

    def get_country(self, val):

        sender = val.widget
        try:
            self._idx_country = sender.curselection()[0]
        except IndexError:
            print('переключение между Listbox')
        value = sender.get(self._idx_country)
        self._choice_country = value
        self._short = self._short_country(self._choice_country)
        self.get_cities(self._short)

    def get_cities(self, short):

        city_data = self.sql_base.city_list(short)
        self.cities_dict = city_data                  # Словарь с ID городов
        self.listbox_city.delete(0, END)
        for city in self.cities_dict:
            if city[1] != '' and city[1] != '-':
                id_city = str(city[0])
                name = city[1]
                self.listbox_city.insert(END, name + ';' + id_city)

    def _short_country(self, value):

        for short, long in self.country_dict.items():
            if long == value:
                return short

    def get_center(self):

        x = int((self.winfo_screenheight() - self.winfo_reqwidth()) / 2)
        y = int((self.winfo_screenheight() - self.winfo_reqheight()) / 2)
        return '+{}+{}'.format(x, y)

    def clear(self):
        self.result_frame.delete(0, END)

    def history(self):

        list_choice = self.choice_listbox.get(0, END)
        for i in list_choice:
            name, id_city = i.split(';')
            history = self.sql_base.history(id_city)
            for request in history:
                self.result_frame.insert(END, request)

    def create_widget(self):

        # Создаем кнопку QUIT
        self.quit_button.place(anchor=SE, relx=1, rely=1)

        # Создаем кнопку очистки Листбокса с результатом
        self.clear_button.place(anchor=tkinter.SW, relx=0, rely=1)

        # Рисуем лейбл над листбоксом
        self.label_country.place(x=BORDER)

        # Рисуем листбокс для стран и наполняем странами
        y_cord = self.label_country.winfo_reqheight()
        for index, country in enumerate(self._sort_country):
            self.listbox_country.insert(index, country)
        scroll_country = tkinter.Scrollbar(self.listbox_country, bg='white', command=self.listbox_country.yview)
        self.listbox_country.configure(yscrollcommand=scroll_country.set)
        scroll_country.place(relx=0.9, rely=0, height=self.listbox_country.winfo_reqheight())
        self.listbox_country.place(y=y_cord, x=BORDER)

        # Рисуем Лейбл с "City:"
        x_cord = self.listbox_country.winfo_reqwidth() + 2*BORDER
        self.label_city.place(x=x_cord)

        # Рисуем листбокс для городов
        x_cord = self.listbox_country.winfo_reqwidth()+2*BORDER
        y_cord = self.label_city.winfo_reqheight()
        scroll_city = tkinter.Scrollbar(self.listbox_city, bg='white', command=self.listbox_city.yview)
        self.listbox_city.configure(yscrollcommand=scroll_city.set)
        scroll_city.place(relx=0.94, rely=0, height=self.listbox_country.winfo_reqheight())
        self.listbox_city.place(x=x_cord, y=y_cord)

        # Рисуем кнопку выбора города
        x_cord = self.listbox_city.winfo_reqwidth() + self.listbox_country.winfo_reqwidth() + 3*BORDER
        y_cord = self.listbox_city.winfo_reqheight()/2
        self.choice_button.place(x=x_cord, y=y_cord)

        # Рисуем листбокс выбора города
        x_cord = x_cord + self.choice_button.winfo_reqwidth() + BORDER
        y_cord = self.label_city.winfo_reqheight()
        self.choice_listbox.place(x=x_cord, y=y_cord)

        # Рисуем кнопку START поиска погоды
        x_cord = BORDER
        y_cord = self.label_country.winfo_reqheight() + self.listbox_country.winfo_reqheight() + BORDER
        self.start_button.place(x=x_cord, y=y_cord)

        # Рисуем кнопку 'history'
        x_cord = self.start_button.winfo_reqwidth() + 2*BORDER
        self.history_button.place(x=x_cord, y=y_cord)

        # Рисуем рамку для результата
        x_cord = BORDER
        y_cord = y_cord + self.start_button.winfo_reqheight() + BORDER
        self.labelframe.place(x=x_cord, y=y_cord)

        # Листобкc ВЫВОДА РЕЗУЛЬТАТА
        scroll_result = tkinter.Scrollbar(self.result_frame, bg='white', command=self.result_frame.yview)
        self.result_frame.configure(yscrollcommand=scroll_result.set)
        scroll_result.place(relx=0.98, rely=0, height=self.result_frame.winfo_reqheight())
        self.result_frame.pack(fill=BOTH, padx=10, pady=10, side=RIGHT, expand=1)

        # Рисуем кнопку удаления города
        x_cord = self.listbox_city.winfo_reqwidth() + self.listbox_country.winfo_reqwidth() + 3 * BORDER
        y_cord = self.listbox_city.winfo_reqheight() - 3 * BORDER
        self.del_button.place(x=x_cord, y=y_cord)


root = Gui()
root.mainloop()
