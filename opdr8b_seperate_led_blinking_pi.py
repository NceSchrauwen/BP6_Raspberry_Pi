# Opdracht 8b Raspberry Pi - Nina Schrauwen
# LED1 and LED2 have to flash seperately with a 3s/1s interval.
# This program is to command the arduino to power the LEDs when they need to be on/off.

import serial
import time

# Define serial poort en baudrate
ser = serial.Serial('/dev/serial0', 9600)
time.sleep(2)

# Write the intervals for the LEDs to the Arduino
ser.write(b'SET LED1 3000\n')  # LED1 knippert elke 3s
ser.write(b'SET LED2 1000\n')  # LED2 knippert elke 1s

# Wait for the Arduino to process the commands
time.sleep(1)

# Start commando for the arduino to begin flashing
ser.write(b'START\n')
print("Knipperen gestart.")
