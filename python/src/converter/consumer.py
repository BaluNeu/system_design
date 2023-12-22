import pika, sys, os, time
from pymongo import MongoClient
import gridfs
from convert import to_mp3

def main():
    client = MongoClient("host.minikube.internal",27017)

    videos_db = client.videos
    mp3_db = client.mp3s

    #gridfs
    fs_videos = gridfs.GridFS(videos_db)
    fs_mp3s = gridfs.GridFS(mp3_db)

    # rabbitmq connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host = "rabbitmq"))

    #whenever a message is taken by the queue this function is being executed
    def callback():


    channel = connection.channel()

    # consume the messages from video queue
    channel.basic_consume(queue = os.environ.get("VIDEO_QUEUE"), on_message_callback = callback)    
