__author__ = 'Stian Stroem Anderssen'


class Group():
    """
    This function creates a group object
    """
    groupname = ""
    students = []

    def get_groupname(self):
        """
        get the name of the group
        :return groupname:
        :rtype:
        """
        return self.__groupname

    def get_students(self):
        """
        Get the name of the students in a list.
        :return:
        :rtype:
        """
        return self.__students

    def set_groupname(self, value):
        """
        Set the groupname of the group
        :param value:
        :type value:
        :return:
        :rtype:
        """
        self.__groupname = value

    def set_students(self, value):
        """
        Set the studentnames.
        :param value:
        :type value:
        :return:
        :rtype:
        """
        self.__students = value
