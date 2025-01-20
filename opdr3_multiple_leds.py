# Opdracht 3: Control 2 leds at once
# Name: Nina Schrauwen
# Description: Control 2 leds at once simultaneously, one after the other and with different intervals.

#Import libraries
import RPi.GPIO as GPIO
import time

# GPIO pin number of LED
LED1 = 17
LED2 = 18

# GPIO setup
GPIO.setmode(GPIO.BCM) # Use Broadcom SOC channel numbering
GPIO.setup(LED1, GPIO.OUT) # Set pin as output
GPIO.setup(LED2, GPIO.OUT) # Set pin as output

# Let the leds blink at the same time, 1 second on, 1 second off
def opdracht_a():
    print("Opdracht a: Both LEDs blink at the same time.")
    
    # Blink the leds 5 times simultaneously
    for _ in range(5):
        GPIO.output(LED1, GPIO.HIGH) # Turn on LED
        GPIO.output(LED2, GPIO.HIGH) # Turn on LED
        time.sleep(1) # Keep LED on for 1 second
        
        GPIO.output(LED1, GPIO.LOW) # Turn off LED
        GPIO.output(LED2, GPIO.LOW) # Turn off LED
        time.sleep(1) # Turn off LED for 1 second

# Let the leds blink one after the other, 1 second on, 1 second off
def opdracht_b():   
    print("Opdracht b: Both LEDs blink one after the other.")
    
    # Blink the leds 5 times one after the other
    for _ in range(5):
        GPIO.output(LED1, GPIO.HIGH) # Turn on LED
        time.sleep(1) # Keep LED on for 1 second
        GPIO.output(LED1, GPIO.LOW) # Turn off LED
        time.sleep(1) # Turn off LED for 1 second

        GPIO.output(LED2, GPIO.HIGH) # Turn on LED
        time.sleep(1) # Keep LED on for 1 second
        GPIO.output(LED2, GPIO.LOW) # Turn off LED
        time.sleep(1) # Turn off LED for 1 second

# Let the leds blink at the same time, both with different intervals 
def opdracht_c():   
    print("Opdracht c: Both LEDs blink at the same time with different intervals.")
    
    # Define the intervals for both leds
    led1_intervals = [1.3, 0.7] # [on, off] intervals for led1
    led2_intervals = [0.8, 1.7] # [on, off] intervals for led2

    # Initialize the led states and timers
    led1_state = GPIO.HIGH
    led2_state = GPIO.HIGH
    # Start at intervals[0] because the led states are initialized as HIGH
    led1_timer = time.time() + led1_intervals[0]
    led2_timer = time.time() + led2_intervals[0]
    # Initialize the last interval times to measure the actual time the led was on or off
    led1_last_interval = time.time()
    led2_last_interval = time.time()

    # Get the start time
    start_time = time.time()
    # Run led blinking sequence for 10 seconds
    while time.time() - start_time < 10:
        # Get the current time
        current_time = time.time()

        # If the current time exceeds the timer, toggle the led state, show the led state and set the next timer
        if current_time >= led1_timer:
            # Calculate the actual interval to compare the actual time the led was on or off
            actual_interval1 = current_time - led1_last_interval
            print(f"LED1 {'ON' if led1_state == GPIO.HIGH else 'OFF'} for {actual_interval1:.2f} seconds")
            # Toggle the led state (HIGH to LOW or LOW to HIGH)
            led1_state = GPIO.LOW if led1_state == GPIO.HIGH else GPIO.HIGH
            # Show the current led state
            GPIO.output(LED1, led1_state)
            # Set the next timer based on the current state of the led
            led1_timer = current_time + (led1_intervals[0] if led1_state == GPIO.HIGH else led1_intervals[1])
            # Update the last interval time
            led1_last_interval = current_time

        # If the current time exceeds the timer, toggle the led state, show the led state and set the next timer
        if current_time >= led2_timer:
            # Calculate the actual interval to compare the actual time the led was on or off
            actual_interval2 = current_time - led2_last_interval
            print(f"LED2 {'ON' if led2_state == GPIO.HIGH else 'OFF'} for {actual_interval2:.2f} seconds")
            # Toggle the led state (HIGH to LOW or LOW to HIGH)
            led2_state = GPIO.LOW if led2_state == GPIO.HIGH else GPIO.HIGH
            # Show the current led state
            GPIO.output(LED2, led2_state)
            # Set the next timer based on the current state of the led
            led2_timer = current_time + (led2_intervals[0] if led2_state == GPIO.HIGH else led2_intervals[1])
            # Update the last interval time
            led2_last_interval = current_time

        # Short delay to avoid high CPU usage
        time.sleep(0.01)

# Run the opdracht functions
try:
    opdracht_a()
    opdracht_b()
    opdracht_c()

# Clean up GPIO settings
finally:
    GPIO.cleanup()
    print("GPIO cleanup completed.")

