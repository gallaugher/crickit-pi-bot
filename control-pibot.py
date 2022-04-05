# control-pibot.py
# Written by Prof. John Gallaugher. For build videos see:
# https://YouTube.com/profgallaugher
# You can control this subscriber program with an iOS app named
# Mil Mascaras, which you can download for free from the iOS App Store at:
# https://apps.apple.com/us/app/mil-mascaras/id1550345112?platform=iphone
#
# serverAddress, below is your pi's host name. But, since our Mosquitto broker and
# this program (which acts as the subscriber) are on the same Raspberry Pi
# we can simply use "localhost" as the server name.
serverAddress = "localhost"

# *** IMPORTANT ***
# The commands below also substitute localhost with your Pi's hostname.
# This works when you've opened a Terminal & connected to your Pi.
# If you're in a class with other students, you can substitue "localhost"
# with the name of their py (e.g. hostname.local if they're on a standard
# Wi-Fi network, or just "hostname" if they're on a network like the Boston
# College campus network, where "hostname" is the name of your friend's Pi.
#
# Once this code is running, you can test with the shell commands:
# To play any of the numbered sounds (substitute a diffrent number for "1" for a different sound:
# mosquitto_pub -h localhost -t "pibot/move" -m "1"
# To start the robot:
# mosquitto_pub -h localhost -t "pibot/move" -m "forward"
# To stop the robot:
# mosquitto_pub -h localhost -t "pibot/move" -m "stop"

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
