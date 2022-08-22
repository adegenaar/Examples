""" module docstring """
import paho.mqtt.client as mqtt
import json 


def on_connect(client: mqtt.Client, userdata, flags, rc):
    """
    The callback for when the client receives
    a CONNACK response from the server.
    """
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("tasmota/discovery/#" )


def on_message(client: mqtt.Client, userdata, msg):
    """
    on_message The callback for when a PUBLISH message is received from the server.

    Args:
        client (mqtt.Client): _description_
        userdata (_type_): _description_
        msg (_type_): _description_
    """
    #print(str(msg.payload))
    #print(msg.topic + " " + str(msg.payload))

    payload = json.loads(msg.payload)
    # if payload:
    #     print("payload = " + json.dumps(payload))

    if userdata is not None:
        userdata[msg.topic]= payload
        #print(userdata)

    if msg.topic:
        print(msg.topic)


def connect_mqtt(server: str, port: int):
    """
    connect_mqtt Connect to an mqtt server

    Returns:
        _type_: Mqtt.Client
    """
    devices = {}
    client = mqtt.Client(userdata=devices)
    client.on_connect = on_connect
    client.on_message = on_message

    # client.connect("mqtt.eclipse.org", 1883, 60)
    # client.username_pw_set(username, password)
    # pitop=192.168.50.88
    # filedump=192.168.0.124

    client.connect(server, port, 60)
    return client


def run():
    """
    run Main entry point
    """
    client = connect_mqtt("filedump.local", 1883)
    while run:
        client.loop()


if __name__ == "__main__":
    run()
