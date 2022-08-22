import paho.mqtt.client as mqtt

# The callback function of connection
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("$SYS/#")

# The callback function for received message
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def subscribe(host : str, port : int, timeout:int)-> mqtt.Client:
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host, port, timeout)
    return client


def main ():
    client = subscribe("broker.emqx.io", 1883, 60)
    client.loop_forever()

if __name__ == "__main__":
    main()
