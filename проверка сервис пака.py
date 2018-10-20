# -*- coding: utf-8 -*-

file = open('rpm.txt')
list_old=[]
for rpm in file:
    list_old.append(rpm)
file.close()

file_sp = open('rpm_sp.txt')
list_sp=[]
for rpm in file_sp:
    list_sp.append(rpm)
file_sp.close()

new_rpm =[]
for rpm in list_sp:
    if rpm not in list_old:
        new_rpm.append(rpm)

new_rpm = sorted(new_rpm, key= str.lower)
file = open('new_rpm.txt', 'w')
for rpm in new_rpm:
    file.write(rpm)

file.close()