#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import time
import random

dataProcessing = 0

# Define event callbacks
def on_connect(mosq, obj, flags, rc):
    print ('on_connect:: Connected with result code '+ str ( rc ) )
    print('rc: ' + str(rc))

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))

def on_log(mosq, obj, level, string):
    print(string)

def on_message(mosq, obj, msg):
	global dataProcessing
	print ('on_message:: this means  I got a message from broker for this topic')
	print(msg.topic + ' ' + str(msg.qos) + ' ' + str(msg.payload))
	if ( str(msg.topic) == '/Imgselect/status' ):
		if ( (msg.payload).decode('utf-8') == 'Done' ):
			dataProcessing = 0

def on_subscribe(mosq, obj, mid, granted_qos):
    print('This means broker has acknowledged my subscribe request')
    print('Subscribed: ' + str(mid) + ' ' + str(granted_qos))

imagedata = ['Mountains', 'Snow', 'Nature', 'Lights']

def chooseImage():
	global dataProcessing
	global imagedata
	#Send messages to the Broker
	secure_random = random.SystemRandom()
	choice = secure_random.choice(imagedata);
	print('Sending ' + choice + ' to the Webapp')
	client.publish ( "/Imgselect/data", choice)
	time.sleep(1)
	dataProcessing = 1

client = mqtt.Client()
# Assign event callbacks
#client.on_connect = on_connect
#client.on_publish = on_publish
#client.on_subscribe = on_subscribe
client.on_message = on_message

# Uncomment to enable debug messages
#client.on_log = on_log

#Connect to the Broker
client.connect('192.168.43.51', 18831, 60)
time.sleep(1)
client.subscribe('/Imgselect/status')
client.loop_start()

try:
	while True:
		if dataProcessing == 0:
			chooseImage()
			time.sleep(1)
		else:
			continue

except KeyboardInterrupt:
    print ('exiting')
    client.loop_stop()
    client.disconnect()
