"""
    subscriber example
"""

import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, retcode):
    """
    on_connect The callback function of connection

    Args:
        client (_type_): the mqtt client
        userdata (_type_): _description_
        flags (_type_): _description_
        rc (_type_): _description_
    """
    print(client)
    print(userdata)
    print(flags)
    print(f"Connected with result code {retcode}")
    client.subscribe("$SYS/#")


def on_message(client, userdata, msg):
    """
    on_message The callback function for received message

    Args:
        client (_type_): _description_
        userdata (_type_): _description_
        msg (_type_): _description_
    """
    print(client)
    print(userdata)
    print(msg.topic+" "+str(msg.payload))

def subscribe(host : str, port : int, timeout:int)-> mqtt.Client:
    """
    subscribe

    Args:
        host (str): hostname
        port (int): port
        timeout (int): how long to wait

    Returns:
        mqtt.Client: the new mqtt client instance
    """

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host, port, timeout)
    return client


def main ():
    """
    main entry point
    """
    client = subscribe("broker.emqx.io", 1883, 60)
    client.loop_forever()

if __name__ == "__main__":
    main()
