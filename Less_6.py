# -*- coding: utf-8 -*-

# EASY (решение объеденил в одном коде)
# Задача - 1
# Опишите несколько классов TownCar, SportCar, WorkCar, PoliceCar
# У каждого класса должны быть следующие аттрибуты:
# speed, color, name, is_police - Булево значение.
# А так же несколько методов: go, stop, turn(direction) - которые должны сообщать,
#  о том что машина поехала, остановилась, повернула(куда)

# Задача - 2
# Посмотрите на задачу-1 подумайте как выделить общие признаки классов
# в родительский и остальные просто наследовать от него.
print('-----------------------ЗАДАЧА №1 + 2 (easy)--------------------------')

import random

#Родительский класс
class Car:

    def __init__(self, speed, color, name):
        self._speed = speed
        self._color = color
        self._name = name
        print('*****************\n'
              'Название - {}\n'
              'Максимальная скорость {}\n'
              'Цвет - {}'.format(self._name, self._speed, self._color))

    def go (self):
        print('поехали...')

    def stop (self):
         print('остановилась...')

    def turn (self, direction):
        print('повернули на {}'.format(direction))

class TownCar(Car):
    def __init__(self, speed, color, name, boolean):
        self._is_police = boolean
        super().__init__(speed, color, name)
        print('Полицейская машина - {}'.format(self._is_police))

class SportCar(TownCar):
    def nitro (self):
        print('Включаем суперскорость')

class WorkCar(TownCar):
    def pogruzka (self):
        print('Включаем погрузочный кран...')

class PolisCar(TownCar):
    def sirena (self):
        print('Включаем сирену...')


def turn_random ():
    direction= {1:'left', 2:'right'}
    return(direction[random.randint(1,2)])

first_car = TownCar(160,'white','BMW', False)
second_car = SportCar(260,'red','MACLAREN',False)
third_car = WorkCar(90,'brown','ГАЗон', False)
fourth_car = PolisCar(200,'blue','FORD', True)


# NORMAL-------------------------------------------------------------------
# Задача - 1
# Ранее мы с вами уже писали игру, используя словари в качестве
# структур данных для нашего игрока и врага, давайте сделаем новую, но уже с ООП
# Опишите базовый класс Person, подумайте какие общие данные есть и у врага и у игрока
# Не забудьте, что у них есть помимо общих аттрибутов и общие методы.
# Теперь наследуясь от Person создайте 2 класса Player, Enemy.
# У каждой сущности должы быть аттрибуты health, damage, armor
# У каждой сущности должно быть 2 метода, один для подсчета урона, с учетом брони противника,
# второй для атаки противника.
# Функция подсчета урона должна быть инкапсулирована
# Вам надо описать игровой цикл так же через класс.
# Создайте экземпляры классов, проведите бой. Кто будет атаковать первым оставляю на ваше усмотрение.
print('-----------------------ЗАДАЧА №1(normal)--------------------------\n'
      'Каждый раунд игрок наносящий удар определяется random`но')

class Person:
    def __init__(self, name, health, damage, armor):
        self.name = name
        self.health = health
        self.damage = damage
        self.armor = armor

class Player(Person):

    def attack (self, enemy):
        enemy.health = enemy.health - self._count_damage(enemy)
        return '**********************\n' \
               '{} наносит: {} ед. урона\n' \
               'Здоровье {}: {} ед. \n' \
               'Здоровье {}: {} ед.'.format(self.name, self._count_damage(enemy), self.name, self.health, enemy.name, enemy.health)

    def _count_damage (self, enemy):
        coefficient_armor = enemy.armor - 1
        damage_after_armor = int(self.damage- (self.damage* coefficient_armor))
        return damage_after_armor

class Enemy (Player):
    pass

class Batle:

    def round (self, player, enemy):
        round_count = 0
        while player.health> 0 and enemy.health> 0:
            round_count += 1
            print('--------ROUND № {}----------'.format(round_count))
            rand = random.randint(1,2) # Атакуйщий определяется случайным образом
            if rand ==1:
                print(player.attack(enemy))
                answer = input('Нажмите 2 для выхода, для продолжения любую...')
                if answer == '2':
                    break
            else:
                print(enemy.attack(player))
                answer = input('Нажмите 2 для выхода, для продолжения любую...')
                if answer == '2':
                    break
        if player.health<= 0:
            print('{} - проиграл...'.format(player.name))
        else:
            print('{} - выйграл !!!'.format(player.name))




player = Player('Игрок', 120, 38, 1.2)
enemy = Enemy('Враг', 135, 31, 1.1)
batle = Batle()

batle.round(player, enemy)



# HARD---------------------------------------------------------------------
# Задача - 1
# Вам необходимо создать завод по производству мягких игрушек для детей.
# Вам надо продумать структуру классов,
# чтобы у вас был класс, который создает игрушки на основании:
#  Названия, Цвета, Типа (животное, персонаж мультфильма)
# Опишите процедуры создания игрушки в трех методах:
# -- Закупка сырья, пошив, окраска
# Не усложняйте пусть методы просто выводят текст о том, что делают.
# В итоге ваш класс по производству игрушек должен вернуть объект нового класса Игрушка.

# Задача - 2
# Доработайте нашу фабрику, создайте по одному классу на каждый тип, теперь надо в классе фабрика
# исходя из типа игрушки отдавать конкретный объект класса, который наследуется от базового - Игрушка

print('-----------------------ЗАДАЧА №1+2(hard)--------------------------')


class ToyData:

    def __init__(self, name, color, type):
        self.name = name
        self.color = color
        self.type = type


class FabricToy(ToyData):

    def purchase(self):
        return ('Закупка материала...')

    def sewing(self):
        return ('Пошив игрушки')

    def painting(self):
        return ('Покраска')

    def result(self):
        print('************************\n'
              '{}\n'
              '{}\n'
              '{}\n'
              'Изготовлена: {}\n'
              'Цвет: {}\n'
              'Тип: {}\n'.format(self.purchase(), self.sewing(), self.painting(), self.name, self.color, self.type))


toy = FabricToy('Машка', 'white', 'charecter') # первая часть задачки hard
toy.result()


class AnimalToy(FabricToy):
    pass


class CharecterToy(FabricToy):
    pass

toy2 = AnimalToy('Бегемотик', 'Желтый', 'зверушка')
toy3 = CharecterToy('Чебурашка', 'Коричневый', 'мульт-герой')

toy2.result()
toy3.result()