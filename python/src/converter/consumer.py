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
    channel = connection.channel()

    #whenever a message is taken by the queue this function is being executed
    def callback(ch,method,properties,body):
        err = to_mp3.start(body,fs_videos,fs_mp3s,ch)
        if err:
            ch.basic_nack(delivery_tag = method.delivery_tag)
        else:
            ch.basic_ack(delivery_tag = method.delivery_tag)

    # consume the messages from video queue
    channel.basic_consume(queue = os.environ.get("VIDEO_QUEUE"), on_message_callback = callback)  

    # start consuming
    channel.start_consuming()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)  


