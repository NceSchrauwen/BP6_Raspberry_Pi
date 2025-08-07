# Opdracht 5a Raspberry Pi - Nina Schrauwen
# 1x indrukken = knipperen met interval van 1 sec
# 2x indrukken = uit 
# 3x indrukken = knipperen met interval van 1 sec
# 4x indrukken = uit en daarna reset

import RPi.GPIO as GPIO
import time

# Functie om tijd om te rekenen naar milliseconden 
def millis():
    return int(time.monotonic() * 1000)

# Pinconfiguratie
LED_PIN = 17
BUTTON_PIN = 18

# Setup van knop en LED
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Statusvariabelen voor LED, tijd en knipperinterval
led_state = False
last_toggle_time = millis()
blink_interval = 1000

# Overige statusvariabelen
press_count = 0
last_button_state = GPIO.input(BUTTON_PIN)
button_debounce_time = millis()

print("Klaar om ingedrukt te worden")

try:
    while True:
        # Variabele houdt de huidige tijd bij in milliseconden
        current_time = millis()
        # Lees de huidige status van de knop uit
        button_state = GPIO.input(BUTTON_PIN)

        # Detecteer een druk op de knop (overgang van HOOG naar LAAG)
        if last_button_state == GPIO.HIGH and button_state == GPIO.LOW:
            # Debounce-check
            if current_time - button_debounce_time > 200:
                # Verhoog het aantal keer dat op de knop is gedrukt
                press_count += 1
                # Stel de debounce-tijd opnieuw in op de huidige tijd
                button_debounce_time = current_time
                print(f"Knop ingedrukt! Aantal drukken: {press_count}")

                # Reset het aantal drukken na 3x indrukken (dus bij 4e druk)
                if press_count > 3:
                    press_count = 0

        # Update de vorige knopstatus naar de huidige status
        last_button_state = button_state

        # Als de knop 1 of 3 keer is ingedrukt, laat de LED knipperen
        if press_count == 1 or press_count == 3:
            # Controleer of er 1 seconde is verstreken, en wissel dan de LED-status
            if current_time - last_toggle_time >= blink_interval:
                led_state = not led_state
                GPIO.output(LED_PIN, led_state)
                # Update de laatste toggle-tijd naar het huidige moment
                last_toggle_time = current_time
        else:
            # In alle andere gevallen: zet de LED uit
            GPIO.output(LED_PIN, False)
            led_state = False

        # Kleine vertraging om CPU-belasting te beperken
        time.sleep(0.01)

# Foutafhandeling bij handmatige onderbreking (Ctrl+C)
except KeyboardInterrupt:
    GPIO.cleanup()
