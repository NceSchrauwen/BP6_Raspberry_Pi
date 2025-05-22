# Opdracht 5c Raspberry Pi - Nina Schrauwen
# BTN == HIGH -> LED1 blink (1s aan/1s uit)
# BTN == LOW -> LED2 blink (1.3s aan/0.7s uit)

import RPi.GPIO as GPIO
import time

# Function that returns the time in seconds 
def millis():
    return int(time.monotonic() * 1000)

# LED and button setup
LED_PIN1 = 17 
LED_PIN2 = 27  
BUTTON_PIN = 18

# LED and button config
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN1, GPIO.OUT)
GPIO.setup(LED_PIN2, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Led and toggle variables
led1_state = False
led2_state = False
last_toggle_time1 = millis()
last_toggle_time2 = millis()

try:
    while True:
        # Save the current time in seconds
        current_time = millis()
        # Read and save current button state
        button_state = GPIO.input(BUTTON_PIN)

        # Note: button_state == 0 means pressed (ON), button_state == 1 means not pressed (OFF) because of the pull up button
        print(f"Current button state: {'ON' if button_state == 0 else 'OFF'}")

        # If the button has been pressed turn on LED1 with the following blinking interval
        if button_state == GPIO.LOW:
            # BUTTON PRESSED -> LED1 blinks (1s on / 1s off)
            on_duration1 = 1000
            off_duration1 = 1000
            elapsed1 = current_time - last_toggle_time1

            # Reset LED2 (green)
            led2_state = False
            GPIO.output(LED_PIN2, False)

            # Switch led states when the on/off duration has passed and update the last time it was switched to the current time
            if led1_state:
                if elapsed1 >= on_duration1:
                    led1_state = False
                    last_toggle_time1 = current_time
            else:
                if elapsed1 >= off_duration1:
                    led1_state = True
                    last_toggle_time1 = current_time

            # Turn on/off LED1 to current LED state
            GPIO.output(LED_PIN1, led1_state)

        # If the button isn't being pressed turn on LED2 with the following blinking interval
        else:
            # BUTTON NOT PRESSED -> LED2 blinks (1.3s on / 0.7s off)
            on_duration2 = 1300
            off_duration2 = 700
            # Measure the elapsed time 
            elapsed2 = current_time - last_toggle_time2

            # Reset LED1, make sure it is off
            led1_state = False
            GPIO.output(LED_PIN1, False)

            # Switch led states when the on/off duration has passed and update the last time it was switched to the current time
            if led2_state:
                if elapsed2 >= on_duration2:
                    led2_state = False
                    last_toggle_time2 = current_time
            else:
                if elapsed2 >= off_duration2:
                    led2_state = True
                    last_toggle_time2 = current_time

            # Turn on/off LED1 to current LED state
            GPIO.output(LED_PIN2, led2_state)

        # Slight delay 
        time.sleep(0.01)

# Catch keyboard exceptions
except KeyboardInterrupt:
    GPIO.cleanup()
