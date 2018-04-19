#start script with token as only paramter
#eg, python shovel-scriptr.py XXXXxxxx== (where XXXXxxxx== is your device token)
import paho.mqtt.client as mqtt
import json
import sys
localClient = mqtt.Client()
scriptrClient = mqtt.Client()
def on_message(client, userdata, msg):
        print "received message" + msg.topic + " " + msg.payload
        scriptrMessage = {
                'method':'Publish',
                'params':{
                        'apsdb.channel': "multitech", #channel on which to publish the message
                        'apsdb.message': json.dumps({'payload': msg.payload, 'topic':msg.topic})
                }
        }
        scriptrClient.publish(sys.argv[1], json.dumps(scriptrMessage)) # Use your scriptr.io Access Token as shown in the above figure
        print "published message" + json.dumps(scriptrMessage)
localClient.connect("localhost", 1883, 60) #local broker on gateway
#access to mqtt.scriptrapps.io for demo purposes is available to everyone over 1883 and 8883. 
#WARNING: DATA SENT OVER THIS BRIDGE IS PUBLIC
#for production endpoints, please contact support@scriptr.io
scriptrClient.connect("mqtt.scriptrapps.io", 1883, 60) #scriptr.io mqtt endpoint
localClient.on_message = on_message
localClient.subscribe("#", 0)
localClient.loop_forever() #forever loop since the on_message is async and we need to leave script running
