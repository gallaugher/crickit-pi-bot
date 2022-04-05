# This uses an Adafruit CrickitHat to test DC motors
# moving in various directions.
# It assumes Pi and Crickit are upgraded & two DC motors are
# attached to the Crickit, with the Pi & Crickit powered on.
# Part of Prof. John Gallaugher's Physical Computing course.
# For more info see playlists: https://YouTube.com/profgallaugher

import time
from adafruit_crickit import crickit

motor_1 = crickit.dc_motor_1
motor_2 = crickit.dc_motor_2

# Move both motors forward at full speed for one second
motor_1.throttle = 1.0 # 1.0 is full speed
motor_2.throttle = 1.0
time.sleep(1.0)

# Stop both motors and wait one second
motor_1.throttle = 0.0
motor_2.throttle = 0.0
time.sleep(1.0)

# just right forward at 50% speed for one second
motor_1.throttle = 0.5
time.sleep(1.0)

# Stop both motors and wait one second
motor_1.throttle = 0.0
motor_2.throttle = 0.0
time.sleep(1.0)

# just right backward at 50% speed for one second
motor_1.throttle = -0.5
time.sleep(1.0)

# Stop both motors and wait one second
motor_1.throttle = 0.0
motor_2.throttle = 0.0
time.sleep(1.0)

# just left forward at 50% speed for one second
motor_2.throttle = 0.5
time.sleep(1.0)

# Stop both motors and wait one second
motor_1.throttle = 0.0
motor_2.throttle = 0.0
time.sleep(1.0)

# just left backward at 50% speed for one second
motor_2.throttle = -0.5
time.sleep(1.0)

# Stop both motors and wait one second
motor_1.throttle = 0.0
motor_2.throttle = 0.0
time.sleep(1.0)

# Both motors backward at half speed for one second
motor_1.throttle = -0.5
motor_2.throttle = -0.5
time.sleep(1.0)

# Stop both motors and wait one second
motor_1.throttle = 0.0
motor_2.throttle = 0.0
time.sleep(1.0)

# Sharp turn left (right forward, left backward)
motor_1.throttle = 0.5
motor_2.throttle = -0.5
time.sleep(1.0)

# Stop both motors and wait one second
motor_1.throttle = 0.0
motor_2.throttle = 0.0
time.sleep(1.0)

# Sharp turn right (left forward, right backward)
motor_1.throttle = -0.5
motor_2.throttle = 0.5
time.sleep(1.0)

# Stop both motors and wait one second
motor_1.throttle = 0.0
motor_2.throttle = 0.0
time.sleep(1.0)
