# -*- coding: utf-8 -*-

# """
# == Лото ==
# Правила игры в лото.
# Игра ведется с помощью специальных карточек, на которых отмечены числа,
# и фишек (бочонков) с цифрами.
# Количество бочонков — 90 штук (с цифрами от 1 до 90).
# Каждая карточка содержит 3 строки по 9 клеток. В каждой строке по 5 случайных цифр,
# расположенных по возрастанию. Все цифры в карточке уникальны. Пример карточки:
# --------------------------
#     9 43 62          74 90
#  2    27    75 78    82
#    41 56 63     76      86
# --------------------------
# В игре 2 игрока: пользователь и компьютер. Каждому в начале выдается
# случайная карточка.
# Каждый ход выбирается один случайный бочонок и выводится на экран.
# Также выводятся карточка игрока и карточка компьютера.
# Пользователю предлагается зачеркнуть цифру на карточке или продолжить.
# Если игрок выбрал "зачеркнуть":
# 	Если цифра есть на карточке - она зачеркивается и игра продолжается.
# 	Если цифры на карточке нет - игрок проигрывает и игра завершается.
# Если игрок выбрал "продолжить":
# 	Если цифра есть на карточке - игрок проигрывает и игра завершается.
# 	Если цифры на карточке нет - игра продолжается.
#
# Побеждает тот, кто первый закроет все числа на своей карточке.
# Пример одного хода:
# Новый бочонок: 70 (осталось 76)
# ------ Ваша карточка -----
#  6  7          49    57 58
#    14 26     -    78    85
# 23 33    38    48    71
# --------------------------
# -- Карточка компьютера ---
#  7 87     - 14    11
#       16 49    55 88    77
#    15 20     -       76  -
# --------------------------
# Зачеркнуть цифру? (y/n)
# Подсказка: каждый следующий случайный бочонок из мешка удобно получать
# с помощью функции-генератора.
# Подсказка: для работы с псевдослучайными числами удобно использовать
# модуль random: http://docs.python.org/3/library/random.html
import random

class RandomCard:
    def __init__(self):
        self.name = 'Карточка игрока'
        self._card_list = self._random_list()
        self._index_space = self._list_space()
        self.all_number = self.card()

    def _random_list(self, count_element= 27, min=1, max=90):
        card_list = []
        i= 0
        while i< count_element:
            number = random.randint(min, max)
            if number not in card_list:
                card_list.append(number)
                i += 1
        return card_list

    def card(self):
        all_number = self._card_list
        first_str = sorted(all_number[0:9])
        second_str = sorted(all_number[9:18])
        third_str = sorted(all_number[18:27])
        index = self._index_space       # Таким образом получаю случайные индексы в строке карточки, которые замажу пробелом
        for i in index:
            first_str[i]= '  '
        index1 = self._list_space()
        for i in index1:
            second_str[i]= '  '
        index2 = self._list_space()
        for i in index2:
            third_str[i]= '  '
        all_number = [first_str, second_str, third_str]
        return all_number

    def _list_space(self):
        count_element = 4
        min = 0
        max = 8
        index_list = []
        i = 0
        while i < count_element:
            number = random.randint(min, max)
            if number not in index_list:
                index_list.append(number)
                i += 1
        return index_list

    def show_card(self):
        all_number = self.all_number
        card_for_print = []
        for string in all_number:
            one_string = list(map(str,string))
            for i in range(len(one_string)):
                if len(one_string[i])== 1:
                    one_string[i] = one_string[i].ljust(2, ' ') #Если одна циферка то добавляем пробел для ровного отображения при отрисовке карточки
            card_for_print.append(' '.join(one_string))
        a= '------{}--------\n {}\n {}\n {}\n---------------------------'.format(self.name, card_for_print[0], card_for_print[1], card_for_print[2])
        return a

class PlayerCard(RandomCard):
    def __init__(self):
        super().__init__()
        self.name = 'Ваша карточка'

class ComputerCard(RandomCard):
    def __init__(self):
        super().__init__()
        self.name = 'Карточка комп'

class Game:

    def keg_random(self):
        number = random.randint(1,90)
        return number

    @staticmethod                                             #Поиск в карточки и зачеркивание бочонка
    def check_keg (keg, list):
        for one_string in list:  # Ищем бочонок в карточке компа и зачеркиваем
            if keg in one_string:
                index = one_string.index(keg)
                one_string[index] = 'x '
                return True

    def start(self):
        player=PlayerCard()
        enemy = ComputerCard()
        all_number = player.all_number
        all_number_enemy = enemy.all_number
        taken_out_kegs =[]
        all_out_kegs = []
        point_enemy = 0
        point_player = 0
        while True:
            i=0
            keg_in_card= 'не найден'
            print('\n'
                  'Зачеркнуто бочонков:{} ;{}'.format(point_player, point_enemy))
            print(player.show_card())
            print(enemy.show_card())
            while True:
                keg = self.keg_random()
                if keg in all_out_kegs:
                    continue
                else:
                    all_out_kegs.append(keg)
                    show_keg = '({})'.format(keg)
                    taken_out_kegs.insert(0, show_keg)
                    break
            print('=> '+';'.join(taken_out_kegs))
            answer= input('Зачеркнуть БОЧОНОК?(y/n) или продолжить(любую)...')
            if Game.check_keg(keg, all_number_enemy):
                point_enemy +=1
                if point_enemy == 15:
                    print('*****************'
                          '* Комп выгйграл!*'
                          '*****************')
                    break
            if answer == 'y':
                if Game.check_keg(keg, all_number):
                    point_player +=1
                    if point_player == 15:
                        print('*****************'
                              '* Ты выгйграл!  *'
                              '*****************')
                        break
                    keg_in_card = 'Бочонок найден'
                if keg_in_card == 'не найден':
                    print('Вы ошиблись игра окончена')
                    break
            elif answer != 'n':
                continue
            else:
                break


game= Game()
game.start()
