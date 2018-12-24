import socketserver
import threading
import time
import socket
import re
import os
import json

with open('server.json', encoding='utf-8') as file:
    conf = json.load(file)

HOST = conf['HOST']  # Задаем адрес диспетчра
PORT = conf['PORT']  # Задаем порт диспетчера
ServerAddress = (HOST, PORT)
TIMEOUT = conf['TIMEOUT']  # время ожидания ответа от калькулятора

calc_ready = set()  # глобальная очередь свободныx калькуляторов
TURN = []  # глобальная очередь запросов от клиентов

# создаем Log файл при первом запуске
if os.path.isfile('server.log') is not True:
    with open('server.log', 'a', encoding='utf-8') as f_obj:
        string = f'{time.ctime()}: Первый запуск\n'
        f_obj.write(string)


# функция записи лога
def log_insert(log):
    with open('server.log', 'a', encoding='utf-8') as f_obj:
        string = f'{time.ctime()}: {log}\n'
        f_obj.write(string)


class MyUDPRequestHandler(socketserver.BaseRequestHandler):

    def message(self):
        message = bytes.decode(self.request[0])
        return message

    def add_ready(self):
        message = self.message()
        found_str = 'ready'
        found_address = r'\"[a-z0-9.]+\"\, [0-9]+'
        result = re.search(found_str, message)
        if result:
            add_port = re.findall(found_address, message)[0]
            address, port = add_port.split(',')
            correct_address = address.split('"')[1]
            port = int(port)
            free_calc = (correct_address, port)
            calc_ready.add(free_calc)
            return True
        else:
            self._add_turn()   # если пришел не ready, то добавляем его в очередь запросо
            return False

    def _add_turn(self):
        message = self.request[0]
        sock = self.request[1]
        address = self.client_address
        thread = {'msg': message, 'sock': sock, 'address': address}
        TURN.append(thread)
        log_message = f'Дата:{time.ctime()} от {self.client_address} сообщение {self.request[0]}'
        # log_insert(log_message)
        print(log_message)

    def handle(self):
        ready = self.add_ready()  # если пришел ready, то добавляем его в очередь свободных калькуляторов

        if ready is not True:
            while len(TURN) > 0 and len(calc_ready) > 0:
                thread = TURN.pop(0)
                datagram = thread['msg']
                sock = thread['sock']
                address = thread['address']
                #  цикл на тот случай если не придет ответ от вычислителя и переслать запрос повторно другому свободному
                while len(calc_ready) > 0:
                    udp_forward = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    try:
                        calc = calc_ready.pop()
                    except KeyError:
                        TURN.insert(0, thread)
                        continue
                    try:
                        udp_forward.sendto(datagram, calc)
                        udp_forward.settimeout(0.05)
                        ok = udp_forward.recvfrom(1024)  # Ожидаем 'ок' от вычислителя, если не получаем что шлем запрос другому свободному
                        if ok[0] == b'ok':
                            udp_forward.settimeout(TIMEOUT)
                            answer = udp_forward.recvfrom(1024)
                            sock.sendto(answer[0], address)
                            calc_ready.add(calc)
                            log_message = f'дата: {time.ctime()} отправленно {address} сообщение {answer[0]}'
                            # log_insert(log_message)
                            print(log_message)
                            break
                        else:
                            continue
                    except Exception as e:
                        if len(calc_ready) == 0:
                            TURN.insert(0, thread)
                        # log_insert(e)
                        print(f'{time.ctime()}; error: {e}')  # пишем всю эту хрень в лог
                time.sleep(0.01)


UDPServerObject = socketserver.ThreadingUDPServer(ServerAddress, MyUDPRequestHandler)
server_thread = threading.Thread(target=UDPServerObject.serve_forever())
server_thread.daemon = True
server_thread.start()
