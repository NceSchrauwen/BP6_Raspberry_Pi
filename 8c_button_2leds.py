# Opdracht 8c Raspberry Pi - Nina Schrauwen
# Als de knop wordt ingedrukt, wisselen de LEDs tussen LED1 en LED2.
# Dit programma is bedoeld om de arduino te laten bepalen welke LED (LED1 of LED2) moet branden op basis van het indrukken van de knop.

import serial
import time

# Definieer seriële poort en baudrate
ser = serial.Serial('/dev/serial0', 9600)
time.sleep(2)  # wacht tot Arduino is opgestart

state = False  # LED wisselstatus

print("Pi klaar. Wacht op knopdruk...")

# Hoofdlus om te luisteren naar knopdrukken
while True:
    # Lees de berichten die via seriële communicatie worden verstuurd
    line = ser.readline().decode().strip()
    # Een knopdruk wordt aangegeven door de string "BUTTON_PRESS"
    if line == "BUTTON_PRESS":
        # Werk de status van de LED bij
        state = not state
        # Stuur het commando naar de Arduino om de LED te wisselen
        command = "LED1\n" if state else "LED2\n"
        # Stuur het commando naar de Arduino
        ser.write(command.encode())
        print(f"Verzonden: {command.strip()}")
        
