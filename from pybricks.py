from pybricks.ev3devices import ColorSensor, GyroSensor, Motor
from pybricks.hubs import EV3Brick
from pybricks.parameters import Color, Port, Stop
from pybricks.tools import wait
# Initializing
ev3 = EV3Brick()
left_motor = Motor(Port.A)
right_motor = Motor(Port.B)
left_sensor = ColorSensor(Port.S1)
right_sensor = ColorSensor(Port.S2)
gyro = GyroSensor(Port.S4)

COLOR = Color.BLACK
TURN_COLOR = Color.GREEN

SPEED = 100
Kp = 2.5
Ki = 0.05
TURN_SPEED = 50
FORWARD_DRIVE_DURATION = 1500
AFTER_TURN_DURATION = 500
SCAN_DELAY = 1000


# Check for GREEN return boolean
def scan_for_green():
    drive_forward(300)
    green_detected = False
    if left_sensor.Color == Color.GREEN or right_sensor.Color == Color.GREEN:
        green_detected = True
    return green_detected


def reset_gyro():
    gyro.reset_angle(0)
 # Turn for x degrees


def turn(degrees, direction):
    reset_gyro()
    target_angle = direction * degrees
    while abs(gyro.angle()) < abs(target_angle):
        if target_angle > 0:
            left_motor.run(-TURN_SPEED)
            right_motor.run(TURN_SPEED)
        else:
            left_motor.run(TURN_SPEED)
            right_motor.run(-TURN_SPEED)
        wait(10)
        left_motor.stop()
        right_motor.stop()


def turn_left_90():
    turn(90, 1)


def turn_right_90():
    turn(90, -1)


def turn_180():
    turn(180, 1)



def drive_forward(duration):
    left_motor.run(SPEED)
    right_motor.run(SPEED)
    wait(duration)
    left_motor.stop()
    right_motor.stop()
 # Drive forward for x duration

# Uses all above functions
def follow_line():
    error_sum = 0
    while not left_sensor == Color.RED and not right_sensor == Color.RED:
        left_green = left_sensor.color() == TURN_COLOR
        right_green = right_sensor.color() == TURN_COLOR
        if left_green or right_green:
            if scan_for_green():
                drive_forward(SCAN_DELAY)
                if left_green and right_green:
                    turn_180()
                    drive_forward(AFTER_TURN_DURATION)
                elif left_green and not right_green:
                    drive_forward(FORWARD_DRIVE_DURATION)
                    turn_left_90()
                    drive_forward(AFTER_TURN_DURATION)
                elif right_green and not left_green:
                    drive_forward(FORWARD_DRIVE_DURATION)
                    turn_right_90()
                    drive_forward(AFTER_TURN_DURATION)
                else:
                    ev3.screen.print("False Detected")
            left_detected = left_sensor.color() == COLOR
            right_detected = right_sensor.color() == COLOR
            if left_detected and right_detected:
                left_motor.run(SPEED)
                right_motor.run(SPEED)
                error_sum = 0
            elif left_detected:
                error_sum += 1
                left_motor.run(SPEED - Kp * (SPEED) - Ki * error_sum)
                right_motor.run(SPEED + Kp * (SPEED) + Ki * error_sum)
            elif right_detected:
                error_sum += 1
                left_motor.run(SPEED + Kp * (SPEED) + Ki * error_sum)
                right_motor.run(SPEED - Kp * (SPEED) - Ki * error_sum)
            else:
                left_motor.run(SPEED)
                right_motor.run(SPEED)
                error_sum = 0
            wait(10)

follow_line()