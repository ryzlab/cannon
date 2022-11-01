import paho.mqtt.client as mqtt
import json
import sys

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    sys.stderr.write("Connected to MQTT server with result code "+str(rc) + "\n")

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    sys.stderr.write("Subscribing to topic 'cannon/commands'\n")
    client.subscribe("cannon/commands")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    try:
        json_message = json.loads(msg.payload)
        if not 'cmd' in json_message or not 'duration' in json_message:
            sys.stderr.write("Message is missing 'cmd' or 'duration': '" + str(msg.payload) + "'\n")
        else:
            print(json_message['cmd'] + " " + str(json_message['duration']))
            sys.stdout.flush()
    except json.decoder.JSONDecodeError:
        sys.stderr.write("Invalid JSON: '" + str(msg.payload) + "'\n")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.publish("cannon/commands", payload="None", qos=0, retain=False)
client.loop_forever()
