# -*- coding: utf-8 -*-

'''
Задение №1 (easy)
'''

a = 123456
b = 'Василий Алибабаевич'
c = 12.3456

print(a, b, c)

d = input('Введите ваше имя: ')
print('Привет! ', d)

'''
Задание №2 (easy)
'''

e = int(input('Введите число: '))
print(e+2)

'''
Задание №3 (easy)
'''

f = int(input('Введите ваш возраст: '))
if f >= 18:
    print('Доступ разрешен')
else:
    print('Приходите, когда исполнится 18')

'''
Задание №1 (NORMAL)
'''

b = 0
while b != 1:
    a = int(input('Введите число >0 но <10: '))
    if a > 0 and a < 10:
        print('Ты молодец!', a**2)
        b = 1
    else:
        print('Не верно!, нужно больше 0 и меньше 10')

'''
Задание №2 (NORMAL)
'''
a = int(input('Введите число <A>'))
b = int(input('Введите число <B>'))

a = a/b
b = a*b
a = b/a

print('А = ', a, '; B = ', b)

'''
Задание №1 (HARD)
'''

name = input('Введите имя: ')
sename = input('Введите фамилию: ')
age = int(input('Введите Ваш возраст: '))
weight = int(input('Введите Ваш вес: '))

if age <= 30 and age >16:
    if weight <= 120 and weight >= 50:
        print(name, sename, ', у Вас все в норме.')
    else:
        print(name, sename, ', Вам следует заняться собой')
elif age >30 and age <= 40:
    if weight <= 120 and weight >= 50:
        print(name, sename, ', у Вас все в норме.')
    else:
        print(name, sename, ', Вам следует заняться собой')
elif age > 40:
    if weight <= 120 and weight >= 50:
        print(name, sename, ', у Вас все в норме.')
    else:
        print(name, sename, ', Вам нужно обратится к доктору')
else:
    print('Вы еще слишком молоды')
