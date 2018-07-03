# -*- coding: utf-8 -*-
"""
Created on 2017/9/30
@author: MG
"""


class Car:

    def __init__(self, passenger_list=[]):
        self.passenger_list = passenger_list

    def pick(self, name):
        self.passenger_list.append(name)

    def drop(self, name):
        self.passenger_list.remove(name)

    def show(self):
        print(self.passenger_list)

if __name__ == "__main__":
    car1 = Car(['A', 'B'])
    car1.pick('C')
    car1.drop('B')
    car1.show()
    car2 = Car()
    car2.pick('B')
    car2.pick('D')
    car2.show()
    car3 = Car()
    car3.pick('E')
    car3.show()
