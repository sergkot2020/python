# -*- coding: utf-8 -*-
import socket
import time
import json

# подгружаем конфиг из json файла
with open('client.json', encoding='utf-8') as file:
    conf = json.load(file)

HOST = conf['HOST']  # Задаем адрес диспетчра
PORT = conf['PORT']  # Задаем порт диспетчера
COUNT = conf['COUNT']  # Количество запросов (отправляются в цикле).
# Периодичность запроса  в секундах
timeout = conf['TIME_REQ']  # При таком параметре запрос отправляется сразу же после получения ответа
ANSW_TIMEOUT = conf['TIME_ANSWER']  # время ожидания ответа

server_address = (HOST, PORT)
count_requests = 1  # Счетчик количества запросов
report = []  # Список в который складываем  словари с запросами


# Цикл отправки запросов на сервер(Дисптчер)
def start(count):
    count_requests = 1  # Счетчик количества запросов
    udp_message = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for _ in range(COUNT):
        request = {
            'datasend': '',
            'timeout': '',
            'error': 0,
            'answer': ''
        }
        msg = 'hello1'
        msg = str.encode(msg)
        udp_message.sendto(msg, server_address)
        send_time = time.time()
        request['datasend'] = send_time
        count_requests += 1
        udp_message.settimeout(ANSW_TIMEOUT)
        try:
            answer = udp_message.recvfrom(1024)
            answer_time = time.time()
            answer_str = bytes.decode(answer[0])
            request['answer'] = answer_str
            request['timeout'] = (answer_time - send_time)
            report.append(request)
        except Exception as e:
            # Не получил ответа и сокет закрылся по таймауту
            request['timeout'] = 0
            request['error'] = 1
            report.append(request)
        if request['error'] == 0:
            print(f'{count_requests-1}. Ответ: {answer_str}')
        else:
            print(f'{count_requests-1}. Ответ: error')
        time.sleep(timeout)


start(COUNT)

# Считаем количество доставленноых пакетов и исключаем те сокеты, которые завершились ошибкой
error = 0
summa = []
for r in report:
    if r['error'] == 1:
        error += 1
    else:
        summa.append(float(r['timeout']))

# Вычисляем максимальное время доставки, минимальное и среднее
max_time, mid_time, min_time = 0, 0, 0
if len(summa) > 0:
    mid_time = sum(summa)/len(summa)
    max_time = max(summa)
    min_time = min(summa)

# Вывод на печать отчета об отправки
for index, r in enumerate(report):
    send = time.ctime(r['datasend'])
    print(f"Дата отправки: {send}; Время доставки: {r['timeout']}")
try:
    print(f"------------------------------------------\n "
          f"Общее количество запросов: {len(report)}\n "
          f"Среднее время ответа: {mid_time}\n "
          f"Max время ответа: {max_time}\n"
          f"MIN время ответа: {min_time}\n"
          f"Кол-во потерянных запросов: {error}\n")
except Exception as e:
    print(e)