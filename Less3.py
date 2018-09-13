# -*- coding: utf-8 -*-

# Постарайтесь использовать то, что мы прошли на уроке при решении этого ДЗ,
# вспомните про zip(), map(), lambda, посмотрите где лучше с ними, а где они излишни!

# Задание - 1
# Создайте функцию, принимающую на вход Имя, возраст и город проживания человека
# Функция должна возвращать строку вида "Василий, 21 год(а), проживает в городе Москва"
print('---------------------Задача №1 (easy)----------------------')

def about_human (name, age, city):
    print(name.title(),',' , int(age), 'год(а)', 'проживает в городе', city.title())

name = input('Введите имя: ')
age = input('Введите возраст: ')
city = input('Введите город: ')

about_human(name, age, city)

# Задание - 2
# Создайте функцию, принимающую на вход 3 числа, и возвращающую наибольшее из них
print('---------------------Задача №2 (easy)----------------------')

#Решение №1
def max_number (num1,num2,num3):
    num1 =int(num1)
    num2 =int(num2)
    num3 =int(num3)
    return max(num1,num2,num3)

#Решение №2
numbers = input('Введите три числа через запятую (1,2,4): ')
a, b, c = numbers.split(',')
max_number = lambda a,b,c: max(int(a),int(b),int(c))

print('макисмальное число', max_number(a,b,c))


# Задание - 3
# Создайте функцию, принимающую неограниченное количество строковых аргументов,
# верните самую длинную строку из полученных аргументов
print('---------------------Задача №3 (easy)----------------------')

def longest_string (*args):
    return max(args, key=len)

a = ['23223r34r23r34r3','1111111111111111111111111111111111111', '222222', '123d']

print(longest_string(*a))


# Задание - 1
# Вам даны 2 списка одинаковой длины, в первом списке имена людей, во втором зарплаты,
# вам необходимо получить на выходе словарь, где ключ - имя, значение - зарплата.
# Запишите результаты в файл salary.txt так, чтобы на каждой строке было 2 столбца,
# столбцы разделяются пробелом, тире, пробелом. в первом имя, во втором зарплата, например: Vasya - 5000
# После чего прочитайте файл, выведите построчно имя и зарплату минус 13% (налоги ведь),
# Есть условие, не отображать людей получающих более зарплату 500000, как именно
#  выполнить условие решать вам, можете не писать в файл
# можете не выводить, подумайте какой способ будет наиболее правильным и оптимальным,
#  если скажем эти файлы потом придется передавать.
# Так же при выводе имя должно быть полностью в верхнем регистре!
# Подумайте вспоминая урок, как это можно сделать максимально кратко, используя возможности языка Python.
print('---------------------Задача №1 (normal)----------------------')
import os

names = ['Вася', 'Петя','Евлампий', 'Ярополк', 'Капиталина', 'Настя', 'Ганс','Маша']
salary = ['10000', '20000', '80000', '500001', '120000', '70000', '30000', '15000']

def output_dict (names, salary):
    result = []
    data_salary = dict(zip(names, salary))
    max_salary = len(max(salary, key=len))
    max_name = len(max(names, key=len))
    for dict_name in data_salary:
        if int(data_salary[dict_name]) <= 500000:
            sdvig = max_name - len(dict_name)+1
            result.append('{} {} {} \n'.format(dict_name,'-'.rjust(sdvig), data_salary[dict_name].rjust(max_salary+1)))
    return result

file = open('salary.txt','w')
buffer = output_dict(names,salary)
for element in buffer:
    file.write(element)
file.close()


with open('salary.txt', 'r', encoding='UTF-8') as file:
    file_name = []
    file_salary = []
    for line in file:
        salary_string = line.split(' ')
        only_salary = int(salary_string[len(salary_string)-2])
        file_name.append(salary_string[0].upper())
        file_salary.append(str(int(only_salary* 0.87)))

buffer = output_dict(file_name, file_salary)
for element in buffer:
    print(element, end='')

# Задание - 1
# Давайте опишем пару сущностей player и enemy через словарь,
# который будет иметь ключи и значения:
# name - строка полученная от пользователя,
# health - 100,
# damage - 50.
# Поэксперементируйте с значениями урона и жизней по желанию.
# Теперь надо создать функцию attack(person1, persoтn2), аргументы можете указать свои,
# функция в качестве аргумента будет принимать атакующего и атакуемого,
# функция должна получить параметр damage атакующего и отнять это количество
# health от атакуемого. Функция должна сама работать с словарями и изменять их значения.

# Задание - 2
# Давайте усложним предыдущее задание, измените сущности, добавив новый параметр - armor = 1.2
# Теперь надо добавить функцию, которая будет вычислять и возвращать полученный урон по формуле damage / armor
# Следовательно у вас должно быть 2 функции, одна наносит урон, вторая вычисляет урон по отношению к броне.

# Сохраните эти сущности, полностью, каждую в свой файл,
# в качестве названия для файла использовать name, расширение .txt
# Напишите функцию, которая будет считывать файл игрока и его врага, получать оттуда данные, и записывать их в словари,
# после чего происходит запуск игровой сессии, где сущностям поочередно наносится урон,
# пока у одного из них health не станет меньше или равен 0.
# После чего на экран должно быть выведено имя победителя, и количество оставшихся единиц здоровья.
print('---------------------Задача № 1+2 (hard)----------------------')

name = input('Введите имя:')
player = {'name':name, 'health':100, 'damage':50, 'armor':1.3}
enemy = {'name':'Devil', 'health':130, 'damage':35, 'armor':1.2}
answer = ''
def damage (player, enemy):
    dam = player['damage']/enemy['armor']
    return dam

def attack (player,enemy):
    enemy['health'] = enemy['health']-player['damage']

file = open(player['name']+'.txt','w')
for buffer in player:
    file.write('{} {} \n'.format(buffer,player[buffer]))
file.close()

file = open(enemy['name']+'.txt','w')
for buffer in enemy:
    file.write('{} {} \n'.format(buffer,enemy[buffer]))
file.close()

def game (name):
    with open(name+'.txt', 'r', encoding='UTF-8') as file1:
        dict = {}
        for line in file1:
            key, value, perenos = line.split(' ')
            dict[key] = value
            if key != 'name':
                dict[key] = float(value)
    return dict

dict_2 = game('Devil')
dict_1 = game(name)

while answer != 'n':
    answer = input('Приступим к игре? (y/n)')
    dam = damage(dict_1, dict_2)
    dict_1['damage'] = dam
    dam = damage(dict_2, dict_1)
    dict_2['damage'] = dam
    print(dict_1['name']+':'+str(dict_1['health']), dict_2['name']+':'+str(dict_2['health']))
    print(dict_1['name']+':', 'наносит УДАР!', 'урон: '+ str(dict_1['damage']))
    attack(dict_1,dict_2)
    print(dict_1['name']+':'+str(dict_1['health']), dict_2['name']+':'+str(dict_2['health']))
    print(dict_2['name']+':', 'наносит УДАР!', 'урон: '+ str(dict_2['damage']))
    attack(dict_2, dict_1)
    print(dict_1['name']+':'+str(dict_1['health']), dict_2['name']+':'+str(dict_2['health']))
    if dict_1['health']<= 0:
        print(dict_1['name'], 'погиб!')
        break
    elif dict_2['health']<= 0:
        print(dict_2['name'], 'погиб!')
        break


