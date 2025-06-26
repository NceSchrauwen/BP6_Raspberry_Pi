# Opdracht 9 Raspberry Pi - Nina Schrauwen
# Beschrijving: Dit script ontvangt IR commando's van een afstandsbediening en bestuurt LEDs (op basis van de IR commando's) op de Raspberry Pi.

import serial
import time
import RPi.GPIO as GPIO
import random

# Definieer de GPIO-pins voor de LEDs in een lijst
LED_PINS = [22, 27, 18, 17]  # GPIO pins for LED1 to LED4
# Setup GPIO
GPIO.setmode(GPIO.BCM)
# Zorg dat alle leds gedefinieerd zijn en niet al aan staan door over de lijst te itereren
for pin in LED_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Definieer startvariabelen
active_leds = []   # Max 2 active LEDs tegelijk
blink_speed = 1000
led_state = False
last_toggle = time.time()

# Seriële communicatie instellen door de juiste poort te gebruiken
ser = serial.Serial('/dev/serial0', 9600, timeout=1)

# Map binding van knoppen naar LED-pins
LED_MAPPING = {
    1: 22,  # led1
    2: 27,  # led2
    3: 18,  # led3
    4: 17   # led4
}

# Match de knop nummers met de LED-pins via de mapping
LED_PINS = list(LED_MAPPING.values())

# Actieve LEDs lijst initialiseren (altijd leeg starten)
active_leds = []

# Selecteer willekeurig twee LEDs om te starten (er moeten altijd twee LEDs actief zijn)
# Er zijn nog geen knoppen ingedrukt, dus we kiezen willekeurig twee LEDs
starter_leds = random.sample(LED_PINS, 2)
# Stuur de geselecteerde LEDs aan door ze toe te voegen aan de actieve lijst
active_leds.append(starter_leds[0])
active_leds.append(starter_leds[1])
print("Initial random active LEDs:", active_leds)

# Functie om de LEDs te toggelen, de status van de actieve LEDs te controleren en de status van de LED te wisselen
def toggle_leds():
    global led_state
    for pin in LED_PINS:
        # Als de ledpin in de actieve LEDs zit, toggle de status op basis van de huidige ledstatus
        if pin in active_leds:
            GPIO.output(pin, GPIO.HIGH if led_state else GPIO.LOW)
        # Als de pin niet in de actieve LEDs zit, zet deze uit
        else:
            GPIO.output(pin, GPIO.LOW)
    # Update de status van de LED, zodat je de volgende keer de led kunt toggelen op basis van de laatste status
    led_state = not led_state

print("Ready to receive IR button commands...")

# Hoofdlus om te luisteren naar seriële input en de LEDs te beheren
try:
    while True:
        # Lees seriële input vanuit de Arduino
        if ser.in_waiting:
            # Lees een regel van de seriële poort
            line = ser.readline().decode('utf-8').strip()
            # Als de regel begint met "BTN:", verwerk de knop
            if line.startswith("BTN:"):
                try:
                    # Parse de knop nummer uit de regel door de string te splitsen
                    btn_number = int(line.split(":")[1])
                    # Als de knop nummer in de led mapping zit, verwerk deze 
                    if btn_number in LED_MAPPING:
                        # Associeer de knop met de juiste LED pin
                        btn_pin = LED_MAPPING[btn_number]

                        # Als de led bij de knop al actief is, verander de snelheid
                        if btn_pin in active_leds:
                            # Change speed
                            blink_speed = btn_number * 1000  # Verander de snelheid op basis van de knop nummer, bv. knop 1 = 1000ms, knop 2 = 2000ms, etc.
                            print(f"Changed speed to {blink_speed}ms")
                        # Als de knop niet actief is
                        else:
                            # Als er minder dan 2 actieve LEDs zijn, voeg de knop toe
                            if len(active_leds) < 2:
                                # Voeg de knop toe aan de actieve LEDs
                                active_leds.append(btn_pin)
                            # Als er al 2 actieve LEDs zijn, verwijder de oudste en voeg de nieuwe toe
                            else:
                                # Verwijder de oudste LED (eerste in de lijst)
                                removed = active_leds.pop(0)
                                print(f"Removed LED with pin {removed}")
                                # Nu de oude verwijderd is, voeg de nieuwe toe
                                active_leds.append(btn_pin)
                            print(f"Now blinking LEDs (GPIO): {active_leds}")
                # Als de knop nummer niet correct is, vang de fout af
                except ValueError:
                    pass

        # Controleer of het tijd is om de LEDs te toggelen op basis van de blink snelheid
        if time.time() - last_toggle >= blink_speed / 1000:
            # Roep de toggle_leds functie om de LEDs te wisselen waar nodig wanneer het blink interval is verstreken
            toggle_leds()
            # Reset de last_toggle tijd zodat de tijdsduur van het volgende blink interval bereikt kan worden
            last_toggle = time.time()

# Vangen van KeyboardInterrupt om het programma netjes af te sluiten
except KeyboardInterrupt:
    print("Stopping...")
# Zorg ervoor dat de GPIO-pins worden opgeruimd en de seriële verbinding wordt gesloten
finally:
    GPIO.cleanup()
    ser.close()
  
