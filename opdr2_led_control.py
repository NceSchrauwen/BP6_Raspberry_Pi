# Opdracht 2: LED control
# Name: Nina Schrauwen
# Description: Control a LED with at differing blinking intervals

#Import libraries
import RPi.GPIO as GPIO
import time

# GPIO pin number of LED
LED = 18

# GPIO setup
GPIO.setmode(GPIO.BCM) # Use Broadcom SOC channel numbering
GPIO.setup(LED, GPIO.OUT) # Set pin as output

# Function to blink LED at given interval
def blink_led(speed_on, speed_off, repetitions):
    for _ in range(repetitions):
        GPIO.output(LED, GPIO.HIGH) # Turn on LED
        time.sleep(speed_on) # Duration of on interval
        GPIO.output(LED, GPIO.LOW) # Turn off LED
        time.sleep(speed_off) # Duration of off interval

# Blink LED at different intervals
try:
    print("Opdracht a: Blink speed is 1 second on, 1 second off.")
    blink_led(1, 1, 5)

    print("Opdracht b: Blink speed is 1 second on, 2 seconds off.")
    blink_led(1, 2, 5)

    print("Opdracht c: Blink speed is 0.1 seconds on, 0.1 seconds off.")
    blink_led(0.1, 0.1, 25)

    print("Opdracht d: Giving the illusion of being always on because of the short blinking interval.")
    blink_led(0.01, 0.01, 100)

# Clean up GPIO settings
finally:
    GPIO.cleanup()
    print("GPIO cleanup completed.")
