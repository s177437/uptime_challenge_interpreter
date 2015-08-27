import pika
import couchdb
import ast

def connectToRabbitMq(message):
    couch= couchdb.Server("http://10.1.0.57:5984/")
    db=None 
    try :
        db=couch.create("configcourse")
    except couchdb.http.PreconditionFailed :
        db=couch["configcourse"]
    configdict= ast.literal_eval(message)
    db.save(configdict)
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters('10.1.0.56',5672, '/', credentials))
channel=connection.channel() 
channel.queue_declare(queue='stianstestq')
#print 'Waiting for messages...'
def callback(channel, method, properties, body) :
	#print "Received message...."+ body 
        connectToRabbitMq(body)
channel.basic_consume(callback, queue='stianstestq', no_ack=True)
channel.start_consuming()





