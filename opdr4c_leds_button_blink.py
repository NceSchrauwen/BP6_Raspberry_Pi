# Opdracht 4c Raspberry Pi - Nina Schrauwen
# 1x indrukken = 1.3 sec aan/0.7 sec uit voor Led 1 (Led 2 is uit) 
# 2x indrukken = 1.3 sec aan/0.7 sec uit voor Led 1 EN Led 2 is aan 
# 3x indrukken = Reset LEDS (alles uit)

import RPi.GPIO as GPIO
import time
import threading

# Pin config
BUTTON_PIN = 18
LED_PIN = 17
LED_PIN2 = 27

# Setup Leds and button
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)
GPIO.setup(LED_PIN2, GPIO.OUT)
GPIO.output(LED_PIN2, GPIO.LOW)

# State button/led config
press_count = 0
blinking = False
blink_thread = None

# Function to make the LED blink in a loop (1.3sec on/0.7 off)
def blink_led():
    while blinking:
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(1.3)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(0.7)

# Function to decide which LED needs to be turned on/off based on the amount of presses
def handle_press():
    global press_count, blinking, blink_thread

    press_count += 1
    print(f"Button pressed {press_count} time(s)")
    
    # If there has been pressed once let the first LED blink and keep the second one off
    if press_count == 1:
        blinking = True
        GPIO.output(LED_PIN2, GPIO.LOW)  # Ensure LED2 is off
        # Start the blink thread
        if blink_thread is None or not blink_thread.is_alive():
            blink_thread = threading.Thread(target=blink_led, daemon=True)
            blink_thread.start()

    # If there has been pressed twice let the first LED blink and turn on the second one
    elif press_count == 2:
        blinking = True
        GPIO.output(LED_PIN2, GPIO.HIGH)
        print("Turning LED2 on")
        # Start the blink thread (if not already or has stopped)
        if blink_thread is None or not blink_thread.is_alive():
            blink_thread = threading.Thread(target=blink_led, daemon=True)
            blink_thread.start()

    # If there has been pressed twice turn off both LEDS to reset the states 
    elif press_count >= 3:
        # Reset everything and turn off the LEDS
        blinking = False
        GPIO.output(LED_PIN, GPIO.LOW)
        GPIO.output(LED_PIN2, GPIO.LOW)
        press_count = 0
        print("Reset LEDs")

try:
    print("Press the button...")
    # Keep listening for button presses
    while True:
        # If a button is pressed make sure it's handled correctly by calling the handle_press() function
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            handle_press()
            # Slight delay between state changes
            while GPIO.input(BUTTON_PIN) == GPIO.LOW:
                time.sleep(0.01)  # Wait for release
            time.sleep(0.2)  # Debounce

# If you exit the terminal
except KeyboardInterrupt:
    print("\nExiting...")
# Reset the blinking value and give the blink thread time to end
finally:
    blinking = False
    time.sleep(0.1)  
    GPIO.cleanup()
