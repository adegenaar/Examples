"""
    minimal test for paho.mqtt client
"""
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, retcode):
    """
    on_connect The callback for when the client receives a CONNACK response from the server.

    Args:
        client (_type_): MQTT Client
        userdata (_type_): custom data
        flags (_type_): any flags that have been passed to the client
        rc (_type_): return code of the connection
    """
    print(client)
    print(userdata)
    print(flags)
    print("Connected with result code "+str(retcode))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")


def on_message(client, userdata, msg):
    """
    on_message The callback for when a PUBLISH message is received from the server.

    Args:
        client (_type_): MQTT Client
        userdata (_type_): custom data
        msg (_type_): payload for the msg
    """
    print(client)
    print(userdata)
    print(msg.topic+" "+str(msg.payload))

if __name__ == "__main__":
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect("mqtt.eclipse.org", 1883, 60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    mqtt_client.loop_forever()
