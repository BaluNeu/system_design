import os, gridfs, pika, json
from flask import Flask, request, send_file
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util
from bson.objectid import ObjectId

server = Flask(__name__)
server.config["MONGO_URI"] = "mongodb://host.minikube.internal:27017/videos"

mongo = PyMongo(server)

fs = gridfs.GridFS(mongo.db)


connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()

# login logs the user by communicates with auth service and assign a token to that user

server.route("/login", methods=["POST"])
def login():
    token,err = access.login(request)

# print(token,err)
    if err:
        return err
    else:
        return token
    

# upload route to upload videos through gate way
    
server.route("/upload", methods=["POST"])
def upload():
    access,err = validate.token(request)
