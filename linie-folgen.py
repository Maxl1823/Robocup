from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Stop, Direction
from pybricks.tools import wait

ev3 = EV3Brick()
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
left_sensor = ColorSensor(Port.S1)
right_sensor = ColorSensor(Port.S4)
x = (ev3.screen.width) // 2
y = (ev3.screen.height) // 2
black = 20
speed = 50


while not Button().any():
    l_reflection = left_sensor.reflection()
    r_reflection = right_sensor.reflection()

    correction = l_reflection - r_reflection

    l_speed = speed - correction
    r_speed = speed + correction

    if l_reflection < black and r_reflection < black:
        left_motor.run(speed)
        right_motor.run(speed)


        ev3.screen.print("Forward", (x, y))

    else:
        left_motor.run(l_speed)
        right_motor.run(r_speed)
        if l_speed < r_speed:

         ev3.screen.print("Left", (x, y))
        else:
         ev3.screen.print("Right", (x, y))



wait(10)
ev3.screen.print("End", (x, y))
sound.beep(500, 100, 2)
wait(5)