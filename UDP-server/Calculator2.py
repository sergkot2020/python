# -*- coding: utf-8 -*-
import socket
import socketserver
import time
import json
import os

with open('calculator2.json', encoding='utf-8') as file:
    conf = json.load(file)

CALC_NAME = conf["ip_address"]
PORT_LISTEN = conf["PORT_LISTEN"]
READY_REQUEST = conf["READY_REQUEST"]  # Переиодичность в секуднах с которой посылается запрос диспетчеру о готовности
CALC_DURATION = conf["CALC_DURATION"]  # Длительность вычислений

READY_MESSAGE = f'("{CALC_NAME}", {PORT_LISTEN});"ready"'

# Адрес сервера (Деспетчера)
NAME_SERVER = "localhost"
PORT_SERVER = 22111
address_server = (NAME_SERVER, PORT_SERVER)
address_calc = (CALC_NAME, PORT_LISTEN)

# создаем Log файл при первом запуске
if os.path.isfile('calculator2.log') is not True:
    with open('calculator2.log', 'a', encoding='utf-8') as f_obj:
        string = f'{time.ctime()}: Первый запуск\n'
        f_obj.write(string)

# функция записи лога
def log_insert(log):
    with open('calculator2.log', 'a', encoding='utf-8') as f_obj:
        string = f'{time.ctime()}: {log}\n'
        f_obj.write(string)

class CalHandler(socketserver.BaseRequestHandler):

    def handle(self):
        sock = self.request[1]
        sock.sendto(b'ok', self.client_address)   # сначала отправляем ОК что значит мы получили запрос и приступаем к вычислению
        # print(f' send: ок; client: {self.client_address}')
        time.sleep(CALC_DURATION)   # тут собственно проводим вычисления
        message = b'answer2'
        sock.sendto(message, self.client_address)
        print(f'{time.ctime()}; request: {self.request[0]}; send: answer2; client: {self.client_address}')

# функция отправки оповещеия диспетчера
def send_ready(address, message = READY_MESSAGE):
    message = str.encode(message)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(message, address)

# Запуск вычислителя
my_calc = socketserver.UDPServer(address_calc, CalHandler)
my_calc.timeout = 0.2
now = time.time()

# Вечный цикл ожидания запроса, и отправки запроса "ready" с заданной периодичностью
while True:
    period = time.time()-now
    if period>=READY_REQUEST:
        now = time.time()
        send_ready(address_server)
    try:
        my_calc.handle_request()
    except Exception as e:
        print(e)

