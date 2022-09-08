from turtle import numinput
from rich import print

number_list = []
for x in range(103):
    number_list.append(str(x))

print(number_list)

number_list_zfilled = []

for number in number_list:
    number_list_zfilled.append(number.zfill(3))

print(number_list_zfilled)