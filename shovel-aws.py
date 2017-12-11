from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import paho.mqtt.client as mqtt
import json
#aws configuration
awsClient = AWSIoTMQTTClient("multitech-gateway")
awsClient.configureEndpoint("a3m9jbp3s169k0.iot.us-west-2.amazonaws.com", 8883)
awsClient.configureCredentials("/home/root/aws/root-CA.crt", "/home/root/aws/Mote.private.key", "/home/root/aws/Mote.cert.pem")
awsClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
awsClient.configureDrainingFrequency(2)  # Draining: 2 Hz
awsClient.configureConnectDisconnectTimeout(10)  # 10 sec
awsClient.configureMQTTOperationTimeout(5)  # 5 sec

def on_message(client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        #push message to aws
        #create a new message which includes the topic and a decrypted version of the payload
        message = {}
        try:
                originalPayload = json.loads(msg.payload)
                if 'data' in originalPayload:#this is a data packet, decode lora encryption
                        message = {}
                        message['original'] = msg.payload
                else:#this isn't a data packet, just send it
                        message = msg.payload
        except:
                print 'not a valid json'
                print msg.payload
                message = msg.payload
        #in all cases, add original topic to message
        message['topic'] = msg.topic
        awsClient.publish(msg.topic, json.dumps(message), 0)

subscribed = False
def on_connect(localClient, userdata, flags, rc):
        print("Connected to local mqtt server")
        if subscribed == False:
                localClient.subscribe("#")
                awsClient.connect()
                localClient.on_message = on_message

localClient = mqtt.Client()
localClient.on_connect = on_connect
localClient.connect("localhost", 1883, 60)

localClient.loop_forever()
