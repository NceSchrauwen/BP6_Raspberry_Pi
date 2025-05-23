# Opdracht 6 Raspberry Pi - Nina Schrauwen
# BTN1 == HIGH -> Servo turns from 0 to 120 degrees in 1 second (at the end of the movement, turn back to 0 degrees in 1 second)
# BTN2 == HIGH -> Servo turns from 0 to 120 degrees in 0.5 seconds (at the end of the movement, turn back to 0 degrees in 0.5 second)
# BTN1 + BTN2 == HIGH -> Servo turns from 0 to 120 degrees in 1 second, hold for 2 seconds, then turn back to 0 degrees in 1 second

import RPi.GPIO as GPIO
import time

# Servo and buttons pin configuration
SERVO_PIN = 27
BUTTON1_PIN = 17
BUTTON2_PIN = 18

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(BUTTON1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# PWM setup for servo
pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0)

# Function to set the angle of the servo by translating the angle to a duty cycle
def set_angle(angle):
    duty = 2 + (angle / 18)
    GPIO.output(SERVO_PIN, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.02)
    GPIO.output(SERVO_PIN, False)

# Function to move the servo to a specified angle and back, holding if specified
def move_servo(speed_sec, hold=False):
    set_angle(0)
    time.sleep(0.1)
    set_angle(120)
    time.sleep(speed_sec)
    # If a hold is requested, wait for 2 seconds at the end of the first position
    if hold:
        time.sleep(2)
    set_angle(0)
    time.sleep(speed_sec)

# Main loop to check button presses and control the servo
try:
    print("Press the buttons to control the servo.")
    while True:
        # Read button states
        btn1 = not GPIO.input(BUTTON1_PIN)  # True if button is pressed
        btn2 = not GPIO.input(BUTTON2_PIN)

        # If both buttons are pressed, move the servo with hold
        if btn1 and btn2:
            print("Both buttons pressed")
            move_servo(1, hold=True)
        # If only button 1 is pressed, move the servo with speed 1 second
        elif btn1:
            print("Button 1 pressed")
            move_servo(1)
        # If only button 2 is pressed, move the servo with speed 0.5 seconds
        elif btn2:
            print("Button 2 pressed")
            move_servo(0.5)
        # Slight delay to prevent button bounce
        time.sleep(0.1)

# Catch keyboard interrupt to exit the program gracefully
except KeyboardInterrupt:
    pass
# If any other exception occurs, clean up GPIO
finally:
    pwm.stop()
    GPIO.cleanup()
