# Opdracht 8c Raspberry Pi - Nina Schrauwen
# If the button is pressed, the LEDs will toggle between LED1 and LED2.
# This program is to command the arduino to power the LEDs, which LED1 or LED2 is determined by the button press.

import serial
import time

# Define serial port and baud rate
ser = serial.Serial('/dev/serial0', 9600)
time.sleep(2)  # let Arduino boot up

state = False  # LED toggle state

print("Pi ready. Waiting for button press...")

# Main loop to listen for button presses
while True:
    # Read the messages sent via serial communication 
    line = ser.readline().decode().strip()
    # A button press is indicated by the string "BUTTON_PRESS"
    if line == "BUTTON_PRESS":
        # Update the state of the LED
        state = not state
        # Send the command to the Arduino to toggle the LED
        command = "LED1\n" if state else "LED2\n"
        # Send the command to the Arduino
        ser.write(command.encode())
        print(f"Sent: {command.strip()}")
