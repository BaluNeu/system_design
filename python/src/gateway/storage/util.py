import pika, json


def upload(f, fs, channel, access):
    try:
        fid = fs.put(f)
    except Exception as err:
        print(err)
        return "internal server error", 500

    message = {
        "video_fid": str(fid),
        "mp3_fid": None,
        "username": access["username"],
    }

    try:
        channel.basic_publish(
            exchange="",
            routing_key="video", # queue name
            body=json.dumps(message), # converts python object to json string
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE # even pod fails videos sill be there , message should be persisted until we remove
            ),
        )
    except Exception as err:
        # if the message is not successfully put on to our queue we need to delete it from the database(it wont be processed if not acknowledged by queue)
        print(err)
        fs.delete(fid)
        return "internal server error", 500