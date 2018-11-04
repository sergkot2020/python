# -*- coding: utf-8 -*-

import requests
import json
import pprint
import telebot
from telebot.types import Message
import re
import time
import datetime
import os

TOKEN = 'Сюда надо ввести токен'
BASE_URL = 'https://api.telegram.org/'
TIME_LIMIT = 18000  # Время в секундах, через этот промежуток отправляется повторное сообщение

bot = telebot.TeleBot(TOKEN)

# создаем Log файл при первом запуске
if os.path.isfile('update.log') is not True:
    with open('update.log', 'a', encoding='utf-8') as f_obj:
        string = f'{datetime.datetime.now()}: Первый запуск\n'
        f_obj.write(string)

new_user = []

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: Message):
    bot.reply_to(message, 'Чё надо?')
    # print(message.entities[].type)
    # [Daniil Gentili](mention: 123456789)

# Привиетствие новых членов чата
@bot.message_handler(content_types=['new_chat_members'])
def welcome(message: Message):
    chat_id = message.chat.id
    new = message.new_chat_member
    bot.send_message(chat_id, f'[{new.first_name}](tg://user?id={new.id}),  доброго времени суток! \n'
                              f'Xочу обратить Ваше внимание на то, что у нас принято представляться и немного рассказывать о себе'
                              f' используя тэги #whois или #представляемся. \n'
                              f'Спасибо за внимание!', parse_mode="markdown")
    now = time.time()
    user ={'id': new.id,'first_name': new.first_name, 'told_about': False, 'data': now, 'chat_id': chat_id}
    new_user.append(user)

# Фильтруем все сообщения чата и ищем хуиз
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    who = r'#whois'
    who2 = r'#представляемся'
    is_whois = re.search(who, message.text)
    is_whois2 = re.search(who2, message.text)
    user_id = message.from_user.id

    if is_whois or is_whois2:
        bot.reply_to(message, 'Добро пожаловать.')
        for index, user in enumerate(new_user):
            if user['id'] == user_id:
                new_user.pop(index)

    for index, user in enumerate(new_user):
        now = time.time()
        last_time = now - user['data']
        if last_time >= TIME_LIMIT:
            first_name = user['first_name']
            chat_id = user['chat_id']
            u_id = user['id']
            bot.send_message(chat_id, f'[{first_name}](tg://user?id={u_id}), БОТ грустит, т.к. Вы так и не представились,\n'
                                      f'используя тэги #whois или #представляемся.\n', parse_mode="markdown")
            new_user.pop(index)

# функция записи лога
def log_insert(log):
    with open('update.log', 'a', encoding='utf-8') as f_obj:
        string = f'{datetime.datetime.now()}: {log}\n'
        f_obj.write(string)

# запускаем вечный цикл
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        log_insert(e)
        time.sleep(15)

# bot.polling()
