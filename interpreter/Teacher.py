class Teacher():
    name = ""
    course = ""
    semester = ""

    def get_name(self):
        return self.__name

    def set_semester(self, s):
        self.semester = s

    def get_semester(self):
        return self.semester

    def set_name(self, value):
        self.__name = value

    def get_course(self):
        return self.__course

    def set_course(self, value):
        self.__course = value
