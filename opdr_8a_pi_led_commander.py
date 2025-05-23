# Opdracht 8a Raspberry Pi - Nina Schrauwen
# LED1 and LED2 have to flash alternately with a 1 second interval.
# This program is to command the arduino to power the LEDs when they need to be on/off.

import serial
import time

# Serial communication with Arduino with baudrate 9600
ser = serial.Serial('/dev/serial0', 9600)
time.sleep(2)

print("Seriële verbinding met Arduino is tot stand gebracht.")

# Main loop to command the Arduino
while True:
    ser.write(b'A')  # Turn on LED1, turn off LED2
    print("LED1 aan, LED2 uit")
    time.sleep(1)
    ser.write(b'B')  # Turn off LED1, turn on LED2
    print("LED1 uit, LED2 aan")
    time.sleep(1)
