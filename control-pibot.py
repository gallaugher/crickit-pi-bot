# control-pibot.py
# If your pi's hostname is something different than "mil-mascaras", see comments
# below the lines labeled *** IMPORTANT *** below.

# *** IMPORTANT ***
# The commands below assume your pi's hostname is mil-mascaras. If you have a
# different name, then use that name in place of mil-mascaras in the mosquitto_pub
# commands, below.
# once running, you can test with the shell commands:
# To play any of the numbered sounds (substitute a diffrent number for "1" for a different sound:
# mosquitto_pub -h mil-mascaras.local -t "pibot/move" -m "1"
# To start the robot:
# mosquitto_pub -h mil-mascaras.local -t "pibot/move" -m "forward"
# To stop the robot:
# mosquitto_pub -h mil-mascaras.local -t "pibot/move" -m "stop"

import pygame
import time
import paho.mqtt.client as mqtt
#from adafruit_motorkit import MotorKit
# if you're using an Adafruit Crickit hat, uncomment the line below and comment out the statement above:
from adafruit_crickit import crickit
# NOTE: The line below is needed if you're using the Waveshare Motor Driver Hat
# comment out this line if you're using a Crickit
# kit = MotorKit(0x40)
# Also, only if using the Waveshare Motor Driver Hat, be sure you've installed
# and modified CircuitPython files, in particular the file at:
# /usr/local/lib/python3.5/dist-packages/adafruit_motorkit.py
# as described in the tutorial at:
# https://gallaugher.com/mil-mascaras

# uncomment lines below if you're using a Crickit
# then replace any reference to kit.motor1 with motor_1 and kit.motor2 with motor_2
motor_1 = crickit.dc_motor_1
motor_2 = crickit.dc_motor_2

clientName = "PiBot"
# *** IMPORTANT ***
# This is your pi's host name. If your name is something different than
# mil-mascaras, then be sure to change it, here - make it the name of your Pi
#serverAddress = "profgpi"
serverAddress = "localhost"
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
pygame.mixer.music.load(fileLocation + "wanna-build-me.mp3")
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
