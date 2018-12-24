# -*- coding: utf-8 -*-
import socket
import socketserver
import copy
import time
import json
import os

with open('crash.json', encoding='utf-8') as file:
    conf = json.load(file)

CALC_NAME = conf["ip_address"]  # Адрес вычислителя
PORT_LISTEN = conf["PORT_LISTEN"]      # Порт который слушает вычислитель
READY_REQUEST = conf["READY_REQUEST"]   # Переиодичность в секуднах с которой посылается запрос 'ready' диспетчеру о готовности
CRASH_PERIOD = conf["CRASH_PERIOD"]     # Периодичность поломки вычислителя
HOW_LONG_CRASH = conf["HOW_LONG_CRASH"]    # На сколько в секундах ломается вычислтель
CALC_DURATION = conf["CALC_DURATION"]   # Длительность вычислений

NAME_SERVER = "localhost"   # Адрес сервера (Деспетчера)
PORT_SERVER = 22111

address_calc = (CALC_NAME, PORT_LISTEN)
address_server = (NAME_SERVER, PORT_SERVER)
READY_MESSAGE = f'("{CALC_NAME}", {PORT_LISTEN});"ready"'


# создаем Log файл при первом запуске
if os.path.isfile('crash.log') is not True:
    with open('crash.log', 'a', encoding='utf-8') as f_obj:
        string = f'{time.ctime()}: Первый запуск\n'
        f_obj.write(string)

# функция записи лога
def log_insert(log):
    with open('crash.log', 'a', encoding='utf-8') as f_obj:
        string = f'{time.ctime()}: {log}\n'
        f_obj.write(string)

class CalHandler(socketserver.BaseRequestHandler):

    def handle(self):
        sock = self.request[1]
        sock.sendto(b'ok', self.client_address)  # сначала отправляем ОК что значит мы получили запрос и приступаем к вычислению
        # log_insert(f' send: ок; client: {self.client_address}')
        time.sleep(CALC_DURATION)   # тут собственно проводим вычисления
        message = b'answer1'
        sock.sendto(message, self.client_address)
        # log_insert(f' send: answer1; client: {self.client_address}')
        print(f' send: answer1; client: {self.client_address}')

# функция отправки оповещеия диспетчера
def send_ready(address, message = READY_MESSAGE):
    message = str.encode(message)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(message, address)

# Запуск вычислителя
my_calc = socketserver.UDPServer(address_calc, CalHandler)
my_calc.timeout = 0.2  # использую метод handle_request и по этому таймауту отрубается и таким образом работает цикл
now = time.time()
now2 = copy.deepcopy(now)

# Вечный цикл ожидания запроса, и отправки запроса "ready" с заданной периодичностью
while True:
    period = time.time() - now
    period2 = time.time() - now2
    if period >= READY_REQUEST:
        now = time.time()
        send_ready(address_server)
    if period2 >= CRASH_PERIOD:
        now2 = time.time()
        # log_insert('***Server - crashed***')
        print(f'{time.ctime()}; ***calculator - crashed***')
        time.sleep(HOW_LONG_CRASH)
    try:
        my_calc.handle_request()
    except Exception as e:
        print(e)




