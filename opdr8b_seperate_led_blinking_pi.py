# Opdracht 8b Raspberry Pi - Nina Schrauwen
# LED1 en LED2 moeten afzonderlijk knipperen met een interval van 3s/1s.
# Dit programma stuurt de Arduino aan om de LEDs aan of uit te zetten wanneer dat nodig is.

import serial
import time

# Definieer seriële poort en baudrate
ser = serial.Serial('/dev/serial0', 9600)
time.sleep(2)

# Schrijf de intervallen voor de LEDs naar de Arduino
ser.write(b'SET LED1 3000\n')  # LED1 knippert elke 3 seconden
ser.write(b'SET LED2 1000\n')  # LED2 knippert elke 1 seconde

# Wacht tot de Arduino de commando’s heeft verwerkt
time.sleep(1)

# Startcommando om de Arduino te laten beginnen met knipperen
ser.write(b'START\n')
print("Knipperen gestart.")
