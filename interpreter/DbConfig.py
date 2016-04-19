import pika
import couchdb
import logging

__author__ = 'Stian Stroem Anderssen'


class DbConfig():
    """
    This module is the logic class for the Config class in the couchdb. Some of the functions are a little outdated,
    because it was decided to use an API to handle the the config interaction with the database.
    """
    logging.basicConfig(filename='/var/log/interpreter.log', level=logging.DEBUG)

    @staticmethod
    def callback(channel, method, properties, body):
        print "Received message...." + body

    @staticmethod
    def get_config(self, teacher, dbname):
        couch = couchdb.Server('http://USER:PASSWORD@couchdb:5984/')
        db = couch[dbname]
        map_fun = '''function(doc) {
        	if(doc.teacher=="''' + teacher + '''"){
            	emit(doc.teacher, doc._id);                                                                                  }    
    		}'''
        result = db.query(map_fun)
        documentid = ""
        for element in result:
            documentid = element["value"]
            doc = db[documentid]
        del doc['_id']
        del doc['_rev']
        del doc['teacher']
        configdict = {}
        for key, value in doc.iteritems():
            configdict.update({key: value})
        return configdict

    @staticmethod
    def fetch_elements_from_couchdb(self):
        """
        This function fetches the config element from the couchdb, and sends it back to the manager as as a dictionary
        :return configdict:
        :rtype dict:
        """
        couch = couchdb.Server('http://USER:PASSWORD@couchdb:5984/'
        fieldlist = []
        configdict = {}
        db = couch['configcourse']
        for element in db:
            fieldlist.append(element)
        for name in fieldlist:
            configdict.update({name: db[name][name]})
        return configdict

    def send_config_to_queue(self, quename):
        """
        This function sends the configfict to the configqueue. OUTDATED.
        :param quename:
        :type quename:
        :return:
        :rtype:
        """
        credentials = pika.PlainCredentials('guest', 'guest')
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672, '/', credentials))
        channel = connection.channel()
        channel.queue_declare(queue=quename)
        content = str(self.fetch_elements_from_couchdb())
        channel.basic_publish(exchange='', routing_key=quename, body=content)
        logging.info(content)
        connection.close()
