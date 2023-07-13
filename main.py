#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (
    Motor,
    TouchSensor,
    ColorSensor,
    InfraredSensor,
    UltrasonicSensor,
    GyroSensor,
)
from pybricks.iodevices import Ev3devSensor
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.iodevices import I2CDevice

# EV3 brick
ev3 = EV3Brick()

# motors
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
# sensors
sensor = Ev3devSensor(Port.S1)
#variables
values = sensor.read("CAL")
base_speed = 5


def isBlack(senint):
    values = sensor.read("CAL")
    if values[senint] < 40:
        return True
    if values[senint] >= 40:
        return False


def follow_line():

    #check if black
    values = sensor.read("CAL")
    error_r = 1
    error_l = 1

    if isBlack(7):
        error_r = error_r + 6
    else:
        error_r = error_r - 5

    if isBlack(0):
        error_l = error_l + 6
    else:
        error_l = error_l - 5

    if isBlack(6):
        error_r = error_r + 2
    else:
        error_r = error_r - 3

    if isBlack(1):
        error_l = error_l + 2
    else:
        error_r = error_r - 3

    if isBlack(5):
        error_r = error_r + 1
    else:
        error_r = error_r - 2
    
    if isBlack(2):
        error_l = error_l + 1
    else:
        error_r = error_r - 2

    if isBlack(4):
        error_r = error_r + 0.5
    else:
        error_r = error_r - 1

    if isBlack(3):
        error_l = error_l + 0.5
    else:
        error_l = error_l - 1
    


    if (not isBlack(7) and not isBlack(0)) or (not isBlack(6) and not isBlack(1)):
        error_r = 2
        error_l = 2
    

    #calculate error
    speed_l = error_l * base_speed
    speed_r = error_r * base_speed

    #run motors
    left_motor.run(speed_l)
    right_motor.run(speed_r)


    print(error_l, error_r)

while True:
    follow_line()
