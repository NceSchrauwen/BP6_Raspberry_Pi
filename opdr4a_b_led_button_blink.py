# Opdracht 4a+b Raspberry Pi - Nina Schrauwen
import RPi.GPIO as GPIO
import time
import threading

# Pin config
BUTTON_PIN = 17
LED_PIN = 18

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Pull-up button
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)  # Start with LED off

# State
led_on = False
press_count = 0
led_blinking = False  # Flag to control blinking

print("Toggle LED to start.")

def blink_led():
    while led_blinking:
        GPIO.output(LED_PIN, GPIO.HIGH)  # Turn on the LED
        time.sleep(1)  # Keep it on for 1 second
        GPIO.output(LED_PIN, GPIO.LOW) # Turn off LED
        time.sleep(1)  # Keep it off for 1 second

try:
    while True:
        button_state = GPIO.input(BUTTON_PIN)

        if button_state == GPIO.LOW:  # Button is pressed
            led_on = not led_on
            
            if led_on:
                press_count += 1
                led_blinking = True # Set flag so the LED is able to blink
                print(f"LED turned ON ({press_count} times)")

                # Start a thread to make sure the blink loop does not get 'stuck'
                blink_thread = threading.Thread(target=blink_led)
                blink_thread.daemon = True  # Ensure thread stops on exit
                blink_thread.start()
            else:
                print("LED turned OFF")
                GPIO.output(LED_PIN, GPIO.LOW) # Turn off LED
                led_blinking = False # Reset flag to stop the blinking
            
            # Debounce delay
            while GPIO.input(BUTTON_PIN) == GPIO.LOW:
                time.sleep(0.01)  # Wait for button release
            time.sleep(0.1)  # Prevent bouncing

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    GPIO.cleanup()
