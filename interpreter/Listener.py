import pika
from DbLogic import *
from DbConfig import *


class Listener():
    """
    OUTDATED class, only used to create general queue methods that the interpreter can use if the communication between
    the manager and the interpreter should be over a queue instead of an API.
    """
    def listenToQueue(self):
        """
        Function to listen continiously to a mainqueue
        :return:
        :rtype:
        """
        quename = "mainqueue"
        logic = DbLogic()
        logic.createQueue(quename, "firstcontent")
        self.listenContinouslyToQueue(quename)

    def connectToRabbitMQ(self):
        """
        Connect function that returns the connection object.
        :return connection :
        :rtype Instance:
        """
        credentials = pika.PlainCredentials('guest', 'guest')
        connection = pika.BlockingConnection(pika.ConnectionParameters('10.1.0.56', 5672, '/', credentials))
        return connection

    def listenContinouslyToQueue(self, quename):
        """
        Listen contininously to a queue with a given name
        :param quename:
        :type quename:
        :return:
        :rtype:
        """
        connection = self.connectToRabbitMQ()
        channel = connection.channel()
        channel.queue_declare(queue=quename)
        channel.basic_consume(self.callback, queue=quename, no_ack=True)
        channel.start_consuming()

    def callback(self, channel, method, properties, body):
        """
        The main class to execute functions based on the contents of the queueelements.
        :param channel:
        :type channel:
        :param method:
        :type method:
        :param properties:
        :type properties:
        :param body:
        :type body:
        :return:
        :rtype:
        """
        logic = DbLogic()
        dbconfig = DbConfig()
        print body
        if "config" in body:
            logic.createQueue(body, "firstContent")
            dbconfig.ListenQToFetchConfig(body)
        elif "report" in body:
            logic.createQueue(body, "firstContent")
        elif "account" in body:
            logic.createQueue(body, "firstContent")
            logic.receiveOneElementFromQ("createuserq")
            userList = logic.convertUserElementFromQToList()
            logic.createGroupAccount(userList)


listen = Listener()
listen.listenContinouslyToQueue("mainq")
