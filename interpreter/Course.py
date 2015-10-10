class Course():
    """
This module aims to build a course object and fill it with metainformation provided in the config.
    """
    coursename = ""
    groups = []

    def get_coursename(self):
        """
        Function to return the name of the course
        :return coursename:
        :rtype:
        """
        return self.__coursename

    def set_coursename(self, value):
        """
        Function to set coursename
        :param value:
        :type value:
        :return:
        :rtype:
        """
        self.__coursename = value

    def get_groups(self):
        """
        Function to return a list of all groups bound to a teacher object
        :return grouplist:
        :rtype:
        """
        return self.groups

    def setGroupList(self, group):
        """
        Function to properly set a group_name
        :param group:
        :type group:
        :return:
        :rtype:
        """
        self.groups.append(group)
