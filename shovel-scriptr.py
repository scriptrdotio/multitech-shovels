import paho.mqtt.client as mqtt
import json

localClient = mqtt.Client()
scriptrClient = mqtt.Client()

def on_message(client, userdata, msg):
        global scriptClient
        print("received message")
        print(msg.topic+" "+str(msg.payload))
        scriptrMessage = {
                "method":"Publish",
                "params":{
                        "apsdb.channel": "multitech"
                }
        }

        message = {}
        try:
                originalPayload = json.loads(msg.payload)
                if 'data' in originalPayload:#this is a data packet, decode lora encryption
                        message['original'] = msg.payload
                else:#this isn't a data packet, just send it
                        message["payload"] = msg.payload
        except:
                print 'not a valid json'
                message["payload"] = msg.payload
        #in all cases, add original topic to message

        message['topic'] = msg.topic
        scriptrMessage["params"]["apsdb.message"] = json.dumps(message)
        print(json.dumps(scriptrMessage))
        scriptrClient.publish("VzE3NkE2OUY5QQ==", json.dumps(scriptrMessage))


#localClient = mqtt.Client()
#scriptrClient = mqtt.Client()

localClient.connect("localhost", 1883, 60)
print("connected to localhost")
scriptrClient.connect("mqtt.scriptrapps.io", 1883, 60)
print("connected to scriptr.io")
localClient.on_message = on_message
localClient.subscribe("#", 0)
#forever loop to keep the scriptr running
localClient.loop_forever()
