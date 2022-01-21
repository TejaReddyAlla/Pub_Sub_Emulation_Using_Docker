from threading import Lock
from logging import DEBUG

import requests
import random
import json
import os

from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import Producer, Consumer

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit, disconnect
from flask_sock import Sock

from werkzeug.utils import send_from_directory 


app = Flask(__name__,static_folder='templates/static',template_folder='templates')
app.config['SECRET_KEY'] = 'as!@zASD'
app.config['DEBUG'] = True

socket_ = SocketIO(app, async_mode=None)

thread = None
thread_lock = Lock()

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html") , 404

@app.route('/')
def index(): # home page for the app
    return render_template("index.html")

@socket_.on('message', namespace='/sendMessage')
def _message(message):
    pubSub_Broker = getkafka_address()
    url1 = "http://"+pubSub_Broker+":7000/notifications/"+str(subscriptionId)
    response = requests.get(url1)
    pings = {}
    topics = []
    for topicId, topicName in response.json().items():
        url2 = "http://"+pubSub_Broker+":7000/broker/getBrokerAddresses/"+str(topicId)
        broker = requests.get(url2).text
        if broker:
            url3 = "http://"+broker+":7000/getAlertsFromTopic/"+str(topicId)
            topicAlerts = requests.get(url3).json()
        pings[topicName] = topicAlerts
        topics.append(topicName)
    return ({
        "topics": topics,
        "notifications": pings
    },200)

@app.route('/sendClientNotifications')
async def sendClientNotifications(webSocketInstance):
    await webSocketInstance.receive().then(lambda data: webSocketInstance.send(data))

@app.route('/getNotificationsKafka')
def getNotificationsKafka(topicName, value):
    conf = {
        "bootstrap.servers": "kafka-1:19092,kafka-2:29092,kakfa-3:39092"
    }
    producer= Producer(conf)
    producer.produce(topicName, value, pp)
    producer.flush()

    return ("testing fine", 200)

@app.route('/createKafkaTopics')
def createKafkaTopics():
    conf = {
        "bootstrap.servers": "kafka-1:19092,kafka-2:29092,kakfa-3:39092"
    }

    admin_client = AdminClient(conf)

    topic_list = []
    for i in range(1, 20):
        topic_list.append(NewTopic("carrier_code_"+str(i), 2, 2))

    admin_client.create_topics(topic_list)

@app.route('/getKafkaTopics')
def getKafkaTopics():
    conf = {
        "bootstrap.servers": "kafka-1:19092,kafka-2:29092,kakfa-3:39092"
    }

    admin_client = AdminClient(conf)

    fs = admin_client.topics_list()

    for topic, f in fs.items():
        try:
            f.result()
            print("Topic {} created".format(topic))
        except Exception as e:
            print("Failed to create topic {}: {}".format(topic, e))
    return ("", 200)

@app.route('/consumerSocket')
def Consumer(topicNames):
    conf = {
        "bootstrap.servers": "kafka-1:19092,kafka-2:29092,kakfa-3:39092",
        'group.id': 'mygroup','auto.offset.reset': 'earliest'
    }

    consumer = Consumer(conf)

    consumer.subscribe(topicNames)
    msg = consumer.poll(1.0)

    if msg.error():
        print("Consumer error: {}".format(msg.error()))

    print('Received message: {}'.format(msg.value().decode('utf-8')))
    
    consumer.close()
    return ("testing fine", 200)

@app.route('/subscriber/<subscriptionId>', methods=['GET'])
def subscriberPage(subscriptionId): #This function renderd the html page of subscriber/subscriber interface
    return render_template("subscriber.html")

@app.route('/publisher/<publisherId>')
def publisherPage(publisherId): #This function renders the webpage of publisher/publisher interface
    return render_template("publisher.html")

@app.route('/subscriber/static/<path:path>')
def staticSubJSFiles(path):
    return send_from_directory('js',path)

def getkafka_address():
    return random.choice(os.environ["PUBSUB_BROKER"].split(','))

@app.route('/subscriber/<subscriptionId>/notifications', methods=['GET'])
def notifications(subscriptionId): #receive the info about subscribed topics of a particular subscriber
    pubSub_Broker = getkafka_address()
    url1 = "http://"+pubSub_Broker+":7000/notifications/"+str(subscriptionId)
    response = requests.get(url1)
    pings = {}
    topics = []
    for topicId, topicName in response.json().items():
        url2 = "http://"+pubSub_Broker+":7000/broker/getBrokerAddresses/"+str(topicId)
        broker = requests.get(url2).text
        if broker:
            url3 = "http://"+broker+":7000/getAlertsFromTopic/"+str(topicId)
            topicAlerts = requests.get(url3).json()
        pings[topicName] = topicAlerts
        topics.append(topicName)
    return ({
        "topics": topics,
        "notifications": pings
    },200)

@app.route('/<userType>/<userId>/fetchSubscriptions', methods=['GET'])
def fetchSubscriptions(userType, userId): #the list of subscriptions
    response = requests.get("http://kafka_1:7000/fetchSubscriptions")
    subscriptions= response.text
    return (subscriptions,200)

@app.route('/subscriber/<subscriptionId>', methods=['POST'])
def subscribe(subscriptionId): #displays the list of subscriptions
    topicId = request.form.get('topic')
    data={"subscriptionId": str(subscriptionId),"topicId": str(topicId)}
    requests.post(url="http://kafka_1:7000/subscribe",data=json.dumps(data))
    return('',200)

@app.route('/unsubscribe/<subscriptionId>', methods=['POST'])
def unsubscribe(subscriptionId): 
    topicId = request.form.get('topic_')
    data={"subscriptionId": str(subscriptionId),"topicId": str(topicId)}
    requests.post(url="http://kafka_1:7000/unsubscribe",data=json.dumps(data))
    return('',200)

@app.route('/publisher/<publisherId>/publish', methods=['POST'])
def publish(publisherId): 
    topicId = request.form.get('topicId')
    info = request.form.get('info')
    data = {"topicId": str(topicId) , "info": str(info)}
    requests.post(url="http://kafka_1:7000/publish", data=json.dumps(data))
    return ('',200)

@app.route('/publisher/<publisherId>/advertise', methods=['POST'])
def advertise(publisherId):
    advertise = request.form.get('advte')
    data={"advertisement": str(advertise)} 
    requests.post(url="http://kafka_1:7000/advertise", data = json.dumps(data))
    return ('',200)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port="8000")