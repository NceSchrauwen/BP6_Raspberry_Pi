# Opdracht 5a Raspberry Pi - Nina Schrauwen
# 1x indrukken = knipperen met interval van 1 sec bij LED 1/ 0.7 sec bij LED 2 
# 2x indrukken = uit 
# 3x indrukken = knipperen met interval van 1 sec bij LED 1/ 0.7 sec bij LED 2 
# 4x indrukken = uit en daarna reset

import RPi.GPIO as GPIO
import time

# Functie om tijd om te rekenen naar milliseconden 
def millis():
    return int(time.monotonic() * 1000)

# Pinconfiguratie
LED_PIN = 17
LED_PIN2 = 27
BUTTON_PIN = 18
BUTTON_PIN2 = 22

# Button and Led setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(LED_PIN2, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_PIN2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Led, time and interval states
led_state = False
led_state2 = False
last_toggle_time = millis()
last_toggle_time2 = millis()
blink_interval = 1000
blink_interval2 = 700

# Other state variables
press_count = 0
press_count2 = 0
last_button_state = GPIO.input(BUTTON_PIN)
last_button_state2 = GPIO.input(BUTTON_PIN2)
button_debounce_time = millis()
button_debounce_time2 = millis()

print("Ready to be pressed")

try:
    while True:
        # Variable holds the current time in milliseconds
        current_time = millis()
        # Button state is read and saved
        button_state = GPIO.input(BUTTON_PIN)
        button_state2 = GPIO.input(BUTTON_PIN2)

        # Detect a button press for BTN(1) (edge: HIGH -> LOW)
        if last_button_state == GPIO.HIGH and button_state == GPIO.LOW:
            # Debounce check
            if current_time - button_debounce_time > 200:
                # Add to the press counter
                press_count += 1
                # Set button_debounce_time to the current time 
                button_debounce_time = current_time
                print(f"Knop ingedrukt! Aantal drukken voor LED(1): {press_count}")

                # Reset to 0 after 3 presses to reset the press_counter
                if press_count > 3:
                    press_count = 0

        #Update the last_button_state to the current state
        last_button_state = button_state

        # If the button has been pressed either once or thrice set the LED to blink
        if press_count == 1 or press_count == 3:
            # Check if an interval of 1 second has been passed, if so switch the current state of the led (LOW to HIGH, etc)
            if current_time - last_toggle_time >= blink_interval:
                led_state = not led_state
                GPIO.output(LED_PIN, led_state)
                # Update last_toggle_time to the current time for the next check
                last_toggle_time = current_time
        else:
            # If it hasn't been pressed those amount of times turn the LEDs OFF
            GPIO.output(LED_PIN, False)
            led_state = False

        # Detect a button press for BTN2 (edge: HIGH -> LOW)
        if last_button_state2 == GPIO.HIGH and button_state2 == GPIO.LOW:
            # Debounce check
            if current_time - button_debounce_time2 > 200:
                # Add to the press counter
                press_count2 += 1
                # Set button_debounce_time to the current time 
                button_debounce_time2 = current_time
                print(f"Knop ingedrukt! Aantal drukken voor LED2: {press_count2}")

                # Reset to 0 after 3 presses to reset the press_counter
                if press_count2 > 3:
                    press_count2 = 0

        #Update the last_button_state to the current state
        last_button_state2 = button_state2

        # If the button has been pressed either once or thrice set the LED to blink
        if press_count2 == 1 or press_count2 == 3:
            # Check if an interval of 1 second has been passed, if so switch the current state of the led (LOW to HIGH, etc)
            if current_time - last_toggle_time2 >= blink_interval2:
                led_state2 = not led_state2
                GPIO.output(LED_PIN2, led_state2)
                # Update last_toggle_time to the current time for the next check
                last_toggle_time2 = current_time
        else:
            # If it hasn't been pressed those amount of times turn the LEDs OFF
            GPIO.output(LED_PIN2, False)
            led_state2 = False

        # Slight delay
        time.sleep(0.01)

# Error handling in case of keyboard interruption 
except KeyboardInterrupt:
    GPIO.cleanup()
