import Pyro4
from DbConfig import *
from DbLogic import *
import logging
import couchdb

__author__ = 'Stian Stroem Anderssen'


class Apilistener():
    """
    This class distributes an API to the manager that can be used to communicate with the database.
    """
    logging.basicConfig(filename='/var/log/interpreter.log', level=logging.DEBUG)

    @staticmethod
    def fetch_config(self, teacher):
        """
        This function creates a new config object and calls the DbConfig fetchconfig class and returns a config object

        :return config:
        :rtype:
        """
        dbconfig = DbConfig()
        config = dbconfig.get_config(teacher, "testconfig")
        return config

    @staticmethod
    def get_enabled_users(self):
        couch = couchdb.Server("http://USER:PASSWORD@couchdb:5984/")
        db = couch["accounts"]
        map_fun = '''
        function(doc) {
            if(doc.enabled==1)
                emit(null, doc);
        }
        '''
        result = db.query(map_fun)
        returnvalues = []
        for element in result:
            returnvalues.append(element["value"])
        return returnvalues

    @staticmethod
    def create_accounts(self, accountlist):
        """
        This function creates a new account by calling the create_group_account function in DbLogic.

        :param accountlist:
        :type accountList:
        :return:
        :rtype:
        """
        dblogic = DbLogic()
        dblogic.create_group_account(accountlist)

    @staticmethod
    def post_report_to_database(self, reportdict):
        """
        This function posts a report to the datbase. A dictionary is sent as a parameter.
        :param reportdict:
        :type reportdict:
        :return:
        :rtype:
        """
        dblogic = DbLogic()
        dblogic.save_report_to_couchdb(reportdict)

    @staticmethod
    def modify_key(self, dbservername, dbname, key, value, keytoupdate, valuetoupdate):
        """
        This function updates any given key, value in the database. A unique key, value is passed as arguments to the
        function. This is necessary to get the correct document back from the database. The document is then
         updated with a given key, value.
        :param dbservername:
        :type dbservername:
        :param dbname:
        :type dbname:
        :param key:
        :type key:
        :param value:
        :type value:
        :param keytoupdate:
        :type keytoupdate:
        :param valuetoupdate:
        :type valuetoupdate:
        :return:
        :rtype:
        """
        couch = couchdb.Server("http://USER:PASSWORD@" + dbservername + ":5984/")
        db = couch[dbname]
        map_fun = '''function(doc) {
                        if(doc.''' + key + '''=="''' + value + '''"){
                          emit(doc.''' + keytoupdate + ''', doc._id);
                        }
                    }'''
        result = db.query(map_fun)
        for element in result:
            documentid = element["value"]
        doc = db[documentid]
        doc[keytoupdate] = valuetoupdate
        db[documentid] = doc

    @staticmethod
    def get_file_and_offset(self, username):
        """
        Return workload-profile name and offset for a user
        :param username:
        :type username:
        :return:
        :rtype:
        """
        couch = couchdb.Server("http://USER:PASSWORD@couchdb:5984/")
        db = couch["accounts"]
        map_fun = '''function(doc) {
	if(doc.group == "''' + username + '''")
		emit("offset",doc.offset);
        if(doc.group=="''' + username + '''")
		emit("configfile", doc.configfile);
}'''
        result = db.query(map_fun)
        returnvalues = {}
        for element in result:
            returnvalues.update({element["key"]: element["value"]})
        return returnvalues

    @staticmethod
    def update_balance(self, dbname, groupname, value):
        """
        This test function updates the existing balance of a user. When a job is performed.
        The results are parsed, and this functions is called to update the balance of the user
        :param dbname:
        :type dbname:
        :param groupname:
        :type groupname:
        :param value:
        :type value:
        :return:
        :rtype:
        """
        couch = couchdb.Server("http://USER:PASSWORD@couchdb:5984/")
        db = couch[dbname]
        map_fun = '''function(doc) {
                        if(doc.group=="''' + groupname + '''"){
                          emit(doc.group, doc._id);
                        }
                    }'''
        result = db.query(map_fun)
        documentid = ""
        for element in result:
            documentid = element["value"]
        doc = db[documentid]
        try:
            oldbalance = doc["Balance"]
            balance = oldbalance + value
            doc["Balance"] = balance
        except KeyError:
            logging.info(groupname + " has no previous balance, creating balance")
            doc["Balance"] = value

        db[documentid] = doc

    @staticmethod
    def get_ip_from_user(self, username):
        """
        Return IP-address of a bookface-site to a user.
        :param username:
        :type username:
        :return:
        :rtype:
        """
        couch = couchdb.Server("http://USER:PASSWORD@couchdb:5984/")
        db = couch["accounts"]
        map_fun = '''function(doc) {
	if(doc.group == "''' + username + '''")
		emit("ipaddress",doc.ipaddress);
}'''
        result = db.query(map_fun)
        returnvalues = {}
        for element in result:
            returnvalues.update({element["key"]: element["value"]})
        return returnvalues

    @staticmethod
    def get_user_config(self, username, dbserver):
        """
        Return all config for a config-account
        :param username:
        :type username:
        :param dbserver:
        :type dbserver:
        :return:
        :rtype:
        """
        couch = couchdb.Server("http://USER:PASSWORD@" + dbserver + ":5984/")
        db = couch["accounts"]
        map_fun = '''function(doc) {
        if(doc.group == "''' + username + '''")
            emit("userconfig",doc);
    }'''
        result = db.query(map_fun)
        returnvalues = {}
        for element in result:
            returnvalues.update({element["key"]: element["value"]})
        return returnvalues["userconfig"]


daemon = Pyro4.Daemon('IP/HOSTNAME')
ns = Pyro4.locateNS()
uri = daemon.register(Apilistener)
ns.register("interpreter", uri)
logging.info("Ready " + str(uri))
daemon.requestLoop()
