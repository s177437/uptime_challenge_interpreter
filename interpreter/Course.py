class Course():
    coursename = ""
    groups = []

    def get_coursename(self):
        return self.__coursename

    def set_coursename(self, value):
        self.__coursename = value

    def get_groups(self):
        return self.groups

    def setGroupList(self, group):
        self.groups.append(group)
