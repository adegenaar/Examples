from paho.mqtt import client as mqtt_client


def on_connect(client: mqtt_client.Client, userdata, flags, rc):
    """
    The callback for when the client receives
    a CONNACK response from the server.
    """
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")


def on_message(client: mqtt_client.Client, userdata, msg):
    """ The callback for when a PUBLISH message is received from the server. """
    print(msg.topic + " " + str(msg.payload))


def connect_mqtt():
    client = mqtt_client.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    # client.connect("mqtt.eclipse.org", 1883, 60)
    # client.username_pw_set(username, password)
    # pitop=192.168.50.88
    client.connect("192.168.50.88", 1883, 60)
    return client


def run():
    client = connect_mqtt()
    while run:
        client.loop()


if __name__ == "__main__":
    run()
