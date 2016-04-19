__author__ = 'Stian Stroem Anderssen'


class DbAccount():
    """
    This is a module for the DbAccount object
    """
    teacher = None

    def get_teacher(self):
        """
        Function to return teacher.
        :return teacher:
        :rtype:
        """
        return self.__teacher

    def set_teacher(self, value):
        """
        Function to set the teacher object
        :param value:
        :type value:
        :return:
        :rtype:
        """
        self.__teacher = value
