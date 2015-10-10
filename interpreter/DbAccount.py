'''
Created on 2. sep. 2015

@author: stianstrom
'''


class DbAccount():
    teacher = None

    def get_teacher(self):
        return self.__teacher

    def set_teacher(self, value):
        self.__teacher = value
