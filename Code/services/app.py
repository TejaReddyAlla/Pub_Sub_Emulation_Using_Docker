import json
from flask import Flask, jsonify, request ,render_template
from dbLogic import *
import requests
import mysql.connector
import os
import random

app = Flask(__name__)

topicsBrokersAddresses = {
    "kafka_1": {
        "1": "mint",
        "3": "AT&T",
        "9":"Verizon",
        "0": "Promotions",
        "10":"Vodafone",
        "11":"Idea",
        "12":"Boost",
        "15":"Visible"
    },
    "kafka_2": {
        "2": "T-mobile",
        "0": "Promotions",
        "5" : "JIO",
        "6":"Airtel",
        "7":"Verizon",
        "8":"BSNL"
    },
    "kafka_3": {
        "0": "Promotions",
        "4": "Lyka",
        "1": "mint",
        "15":"Visible",
        "13":"Metro",
        "14":"Sprint",
    }
}

@app.route('/broker/getBrokerAddresses/<topicId>', methods=['GET'])
def getBrokerAddress(topicId):
    for brokerId, notifications in topicsBrokersAddresses.items():
        if topicId in notifications:
            return (brokerId, 200)
    return('', 404)

@app.route('/getAlertsFromTopic/<topicId>', methods=['GET'])
def getAlertsFromTopic(topicId):
    topicId = int(topicId)
    notifications = fetch_info(topicId)
    return (json.dumps(notifications), 200)

@app.route('/notifications/<subscriptionId>', methods=['GET'])
def fetchNotifications(subscriptionId):
    subscriptionId = int(subscriptionId)
    topics = subscribed_topics(subscriptionId)
    topics.append(0)
    allTopics = fetchAllTopics()
    subTopics = {}
    for topic in allTopics:
        if topic[0] in topics:
            subTopics[topic[0]] = topic[1]
    return json.dumps(subTopics)


@app.route('/subscribe', methods=['POST'])
def subscription():
    data = json.loads(request.data.decode("utf-8"))
    subscriptionId = int(data["subscriptionId"])
    topicId = int(data["topicId"])
    subscribe(subscriptionId, topicId)
    return('', 200)

@app.route('/unsubscribe', methods=['POST'])
def unSubscribe():
    try:
        data = json.loads(request.data.decode("utf-8"))
        subscriptionId = int(data["subscriptionId"])
        topicId = int(data["topicId"])
        unsubscribe(subscriptionId, topicId)
        return('', 200)
    except:
        return('', 400)

@app.route('/publish', methods=['POST'])
def publishinfo():
    try:
        data = json.loads(request.data.decode("utf-8"))
        topicId = int(data["topicId"])
        info = str(data["info"])
        publish_info(topicId, info)
        return('', 200)
    except:
        return('', 400)

@app.route('/advertise', methods=['POST'])
def advertiseinfo():
    try:
        data = json.loads(request.data.decode("utf-8"))
        advertisement = str(data["advertisement"])
        advertise_info(advertisement)
        return('', 200)
    except:
        return('', 400)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port="7000")