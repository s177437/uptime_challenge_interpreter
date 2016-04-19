import couchdb
from Course import *
from DbAccount import *
from Group import *
from Teacher import *
from collections import OrderedDict
import ast
import pika
import logging

__author__ = 'Stian Stroem Anderssen'


class DbLogic():
    """
    This module is the logic for the interpreter. Here, the account object is received and created before
    it is written to the database.
    """

    logging.basicConfig(filename='/var/log/interpreter.log', level=logging.DEBUG)

    def set_queue_content(self, value):
        """
        A function to set the content to be sent to the queue for later usage
        :param value:
        :type value:
        :return:
        :rtype:
        """
        self.queuecontent = value

    def get_queue_content(self):
        """
        Return the queue content
        :return:
        :rtype:
        """
        return self.queuecontent

    @staticmethod
    def build_account_object(self, received_list):
        """
        This functions builds an account object which can be written directly to the database. The function received a
        list containing the teacher, course, groups and students plus semester.

        Example list style: [{"teacher": ["Teachername"], {"course":["Coursename"]}...}]
        :param received_list:
        :type received_list:
        :return account:
        :rtype DbAccount:
        """
        account = DbAccount()
        teacher = Teacher()
        course = Course()
        group = Group()
        groupdict = {}
        for i in received_list:
            for key, value in i.iteritems():
                if "teacher" in key:
                    teacher.set_name(value[0])
                elif "semester" in key:
                    teacher.set_semester(value[0])
                elif "course" in key:
                    course.set_coursename(value[0])
                elif "group" in key:
                    for groupkey, memberlist in value.iteritems():
                        group = Group()
                        groupdict.update({groupkey: memberlist})
                        group.set_groupname(groupkey)
                        group.set_students(memberlist)
                        if any(x.get_groupname() == groupkey for x in course.get_groups()):
                            logging.info(groupkey + " exists in the object from before")
                        else:
                            course.set_group_list(group)
        teacher.set_course(course)
        account.set_teacher(teacher)
        return account

    def create_group_account(self, userlist):
        """
        Function to post the accountobject to the database.
        :param userlist:
        :type userlist:
        :return:
        :rtype:
        """
        couch = couchdb.Server("http://USER:PASSWORD@couchdb:5984/")
        teacheraccount = self.build_account_object(userlist)
        db = couch["accounts"]
        logging.info(str(teacheraccount.get_teacher().get_course().get_groups()))
        for i in teacheraccount.get_teacher().get_course().get_groups():
            accountdict = OrderedDict()
            accountdict.update({"teacher": teacheraccount.get_teacher().get_name()})
            accountdict.update({"course": teacheraccount.get_teacher().get_course().get_coursename()})
            accountdict.update({"semester": teacheraccount.get_teacher().get_semester()})
            accountdict.update({"group": i.get_groupname()})
            accountdict.update({"members": i.get_students()})
            value = self.check_if_databaseuser_exists(i.get_groupname(), teacheraccount.get_teacher().get_name())
            if "True" in value:
                db.save(accountdict)
            else:
                logging.info(i.get_groupname() + " exists in the database from before, no need to create it")

    @staticmethod
    def check_if_databaseuser_exists(self, user, teacher):
        """
        Function to see if a user exist in the database from before.
        :param user:
        :type String:
        :param teacher:
        :type String:
        :return:
        :rtype:
        """
        couch = couchdb.Server("http://USER:PASSWORD@couchdb:5984/")
        checkuserlist = []
        db = couch['accounts']
        map_fun = '''function(doc) {
                        if(doc.teacher=="''' + teacher + '''"){
                          emit(doc.teacher, doc.group);
                        }    
                    }'''
        results = db.query(map_fun)
        for element in results:
            checkuserlist.append(element['value'])
        if user in checkuserlist:
            return "False"
        else:
            logging.info(user + " does not exist, need to create it")
            return "True"

    @staticmethod
    def save_report_to_couchdb(self, reportdict):
        """
        Function to save the report objects in the couchdb.
        :param reportdict:
        :type dict
        :return:
        :rtype:
        """
        couch = couchdb.Server("http://USER:PASSWORD@couchdb:5984/")
        logging.info(str(reportdict))
        db = None
        try:
            db = couch.create("reports")
        except couchdb.http.PreconditionFailed:
            db = couch["reports"]
        db.save(reportdict)
        logging.info("Document saved in the database")
