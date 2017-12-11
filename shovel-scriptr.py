import paho.mqtt.client as mqtt
import json
localClient = mqtt.Client()
scriptrClient = mqtt.Client()
def on_message(client, userdata, msg):
scriptrMessage = { #message in the format scriptr.io expects
"method":"Publish",
"params":{
"apsdb.channel": "multitech" #channel on which to publish the message
"apsdb.message": JSON.dumps({"payload": msg.payload, "topic":msg.topic})
}
}
scriptrClient.publish("VzE3XXXXXXXXX", json.dumps(scriptrMessage)) # Use your scriptr.io Access Token as shown in the above figure
localClient.connect("localhost", 1883, 60) #local broker on gateway
scriptrClient.connect("mqtt.scriptrapps.io", 1883, 60) #scriptr.io mqtt endpoint
localClient.on_message = on_message
localClient.subscribe("#", 0)
localClient.loop_forever() #forever loop since the on_message is async and we need to leave script running
