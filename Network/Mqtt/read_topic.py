""" module docstring """
import json
import logging
import paho.mqtt.client as mqtt



def on_connect(client: mqtt.Client, userdata, flags, retcode):
    """
    The callback for when the client receives
    a CONNACK response from the server.
    """
    print("Connected with result code " + str(retcode))

    topic = userdata['topic']
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
#    client.subscribe("tasmota/discovery/#" )
    client.subscribe(topic)
    print(userdata)
    print(flags)

def on_message(_: mqtt.Client, userdata, msg):
    """
    on_message The callback for when a PUBLISH message is received from the server.

    Args:
        client (mqtt.Client): _description_
        userdata (_type_): _description_
        msg (_type_): _description_
    """
    if userdata is not None:
        logger = userdata['logger']
        payload = json.loads(msg.payload)
        if payload:
            logger.debug("payload = %s", json.dumps(payload))
        userdata[msg.topic]= payload
        if msg.topic:
            logger.debug("topic: %s", msg.topic)


def connect_mqtt(server: str, port: int, topic:str):
    """
    connect_mqtt Connect to an mqtt server

    Returns:
        _type_: Mqtt.Client
    """
    logger = logging.getLogger(__name__)

    devices = {
        "topic": topic,
        "logger": logger
    }
    client = mqtt.Client(userdata=devices)
    client.on_connect = on_connect
    client.on_message = on_message

    client.enable_logger(logger)

    # client.connect("mqtt.eclipse.org", 1883, 60)
    # client.username_pw_set(username, password)
    # pitop=192.168.50.88
    # filedump=192.168.0.124

    client.connect(server, port, 60)
    return client


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
#    mqtt_client = connect_mqtt("filedump.local", 1883)
    try:
        mqtt_client = connect_mqtt("test.mosquitto.org", 1883,"DataHub")
        mqtt_client.loop_forever()
    except KeyboardInterrupt:
        pass
    finally:
        mqtt_client.disconnect()
