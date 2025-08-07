# Opdracht 8a Raspberry Pi - Nina Schrauwen
# LED1 en LED2 moeten afwisselend knipperen met een interval van 1 seconde.
# Dit programma stuurt de Arduino aan om de LEDs aan of uit te zetten wanneer dat nodig is.

import serial
import time

# Seriële communicatie met de Arduino met een baudrate van 9600
ser = serial.Serial('/dev/serial0', 9600)
time.sleep(2)

print("Seriële verbinding met Arduino is tot stand gebracht.")

# Hoofdlus om de Arduino aan te sturen
while True:
    ser.write(b'A')  # LED1 aanzetten, LED2 uitzetten
    print("LED1 aan, LED2 uit")
    time.sleep(1)
    ser.write(b'B')  # LED1 uitzetten, LED2 aanzetten
    print("LED1 uit, LED2 aan")
    time.sleep(1)
    
