# control-pibot.py
# *** IMPORTANT ***
# serverAddress is your pi's host name. Be sure to replace hostname, below
# with the hostname that you use to log into your Pi.
# If you are running this code from the BostonCollege network, remove .local below
# but REMEMBER if you run this on another Wi-Fi network (e.g. at home), you'll need
# to modify this code to add .local again
serverAddress = "hostname.local"

# *** IMPORTANT ***
# The commands below assume your pi's hostname is hostname. If you have a
# different name, then use that name in place of hostname in the mosquitto_pub
# commands, below.
# once running, you can test with the shell commands:
# To play any of the numbered sounds (substitute a diffrent number for "1" for a different sound:
# mosquitto_pub -h hostname.local -t "pibot/move" -m "1"
# To start the robot:
# mosquitto_pub -h hostname.local -t "pibot/move" -m "forward"
# To stop the robot:
# mosquitto_pub -h hostname.local -t "pibot/move" -m "stop"

import pygame
import time
import paho.mqtt.client as mqtt
# This code assumes you are using an adafruit crickit board to power your Pi
from adafruit_crickit import crickit

motor_1 = crickit.dc_motor_1
motor_2 = crickit.dc_motor_2

# don't modify the name below - this is correct
clientName = "PiBot"

mqttClient = mqtt.Client(clientName)
# Flag to indicate subscribe confirmation hasn't been printed yet.
didPrintSubscribeMessage = False

# If the robot veers left or right, add a small amount to the left or right trim, below
# until the bot moves roughly straight. The #s below reflect the bot I'm working with.
# It's probably best to start both trim values at 0 and adjust from there.
# out of 1.0 full power.
LEFT_TRIM   = 0.0
RIGHT_TRIM  = 0.0

leftSpeed = 1.0 + LEFT_TRIM
rightSpeed = 1.0 + RIGHT_TRIM

# This will make turns at 50% of the speed of fwd or backward
slowTurnBy = 0.5

# setup startup sound. Make sure you have a sounds
# folder with a sound named startup.mp3
fileLocation = "/home/pi/robot_sounds/"
pygame.mixer.init()
pygame.mixer.music.load(fileLocation + "startup.wav")
speakerVolume = ".50" # initially sets speaker at 50%
pygame.mixer.music.set_volume(float(speakerVolume))
pygame.mixer.music.play()

def connectionStatus(client, userdata, flags, rc):
    global didPrintSubscribeMessage
    if not didPrintSubscribeMessage:
        didPrintSubscribeMessage = True
        print("subscribing")
        mqttClient.subscribe("pibot/move")
        print("subscribed")

def messageDecoder(client, userdata, msg):
    message = msg.payload.decode(encoding='UTF-8')

    if message == "forward":
        motor_1.throttle = rightSpeed
        motor_2.throttle = leftSpeed
        print("^^^ moving forward! ^^^")
        print(leftSpeed,rightSpeed)
    elif message == "stop":
        motor_1.throttle = 0.0
        motor_2.throttle = 0.0
        print("!!! stopping!")
    elif message == "backward":
        motor_1.throttle = -rightSpeed
        motor_2.throttle = -leftSpeed
        print("\/ backward \/")
        print(-leftSpeed,-rightSpeed)
    elif message == "left":
        motor_1.throttle = rightSpeed * slowTurnBy
        motor_2.throttle = -leftSpeed * slowTurnBy
        print("<- left")
        print(-leftSpeed * slowTurnBy,rightSpeed * slowTurnBy)
    elif message == "right":
        motor_1.throttle = -rightSpeed * slowTurnBy
        motor_2.throttle = leftSpeed * slowTurnBy
        print("-> right")
        print(leftSpeed * slowTurnBy,-rightSpeed * slowTurnBy)
    elif message.startswith("Vol="):
        speakerVolume = message[4:]
        pygame.mixer.music.set_volume(float(speakerVolume))
    else:
        print("Playing sound at: " + fileLocation + message + ".mp3")
        pygame.mixer.music.stop()
        pygame.mixer.music.load(fileLocation + message + ".mp3") # assumes you have a file$
        pygame.mixer.music.play()

# Set up calling functions to mqttClient
mqttClient.on_connect = connectionStatus
mqttClient.on_message = messageDecoder

# Connect to the MQTT server & loop forever.
# CTRL-C will stop the program from running.
print("server address is:", serverAddress)
mqttClient.connect(serverAddress)
mqttClient.loop_forever()
