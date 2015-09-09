import pika
from DbLogic import *
from DbConfig import *
class Listener() :

    def listenToQueue(self):
        quename="mainqueue"
        logic= DbLogic()
        logic.createQueue(quename,"firstcontent")
        self.listenContinouslyToQueue(quename)


    def listenContinouslyToQueue(self, quename):
        connection=self.connectToRabbitMQ()
        channel=connection.channel()
        channel.queue_declare(queue=quename)
        channel.basic_consume(self.callback, queue=quename, no_ack=True)
        channel.start_consuming()

    def callback(self,channel, method, properties, body) :
        logic= DbLogic()
        dbconfig=DbConfig()
        if "config" in body :
            logic.createQueue(body, "firstContent")
            dbconfig.ListenQToFetchConfig(body)
        elif "report" in body :
            logic.createQueue(body,"firstContent")
        elif "account" in body :
            logic.createQueue(body, "firstContent")
            logic.receiveOneElementFromQ(body)
            userList=logic.convertUserElementFromQToList()
            logic.createGroupAccount(userList)


listen = Listener()
listen.listenContinouslyToQueue("masterq")














