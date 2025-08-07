# Opdracht 5a Raspberry Pi - Nina Schrauwen
# 1x indrukken = knipperen met interval van 1 sec bij LED 1 / 0.7 sec bij LED 2 
# 2x indrukken = uit 
# 3x indrukken = knipperen met interval van 1 sec bij LED 1 / 0.7 sec bij LED 2 
# 4x indrukken = uit en daarna reset

import RPi.GPIO as GPIO
import time

# Functie om tijd om te rekenen naar milliseconden 
def millis():
    return int(time.monotonic() * 1000)

# Pinconfiguratie
LED_PIN = 17
LED_PIN2 = 27
BUTTON_PIN = 18
BUTTON_PIN2 = 22

# Instellen van knoppen en LEDs
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(LED_PIN2, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_PIN2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Status van LEDs, tijd en intervallen
led_state = False
led_state2 = False
last_toggle_time = millis()
last_toggle_time2 = millis()
blink_interval = 1000
blink_interval2 = 700

# Overige statusvariabelen
press_count = 0
press_count2 = 0
last_button_state = GPIO.input(BUTTON_PIN)
last_button_state2 = GPIO.input(BUTTON_PIN2)
button_debounce_time = millis()
button_debounce_time2 = millis()

print("Klaar om ingedrukt te worden")

try:
    while True:
        # Variabele bevat de huidige tijd in milliseconden
        current_time = millis()
        # Lees de status van beide knoppen
        button_state = GPIO.input(BUTTON_PIN)
        button_state2 = GPIO.input(BUTTON_PIN2)

        # Detecteer knopdruk voor knop 1 (overgang van HOOG naar LAAG)
        if last_button_state == GPIO.HIGH and button_state == GPIO.LOW:
            # Debounce-controle
            if current_time - button_debounce_time > 200:
                # Verhoog de telwaarde
                press_count += 1
                # Zet debounce-tijd op huidige tijd
                button_debounce_time = current_time
                print(f"Knop ingedrukt! Aantal drukken voor LED 1: {press_count}")

                # Reset naar 0 na 3 drukken (4e druk)
                if press_count > 3:
                    press_count = 0

        # Update vorige status van knop 1
        last_button_state = button_state

        # Als knop 1 één of drie keer is ingedrukt, laat LED 1 knipperen
        if press_count == 1 or press_count == 3:
            # Controleer of interval is verstreken, wissel dan LED-status
            if current_time - last_toggle_time >= blink_interval:
                led_state = not led_state
                GPIO.output(LED_PIN, led_state)
                # Update toggle-tijd
                last_toggle_time = current_time
        else:
            # Zet LED uit in andere gevallen
            GPIO.output(LED_PIN, False)
            led_state = False

        # Detecteer knopdruk voor knop 2 (overgang van HOOG naar LAAG)
        if last_button_state2 == GPIO.HIGH and button_state2 == GPIO.LOW:
            # Debounce-controle
            if current_time - button_debounce_time2 > 200:
                # Verhoog de telwaarde
                press_count2 += 1
                # Zet debounce-tijd op huidige tijd
                button_debounce_time2 = current_time
                print(f"Knop ingedrukt! Aantal drukken voor LED 2: {press_count2}")

                # Reset naar 0 na 3 drukken (4e druk)
                if press_count2 > 3:
                    press_count2 = 0

        # Update vorige status van knop 2
        last_button_state2 = button_state2

        # Als knop 2 één of drie keer is ingedrukt, laat LED 2 knipperen
        if press_count2 == 1 or press_count2 == 3:
            # Controleer of interval is verstreken, wissel dan LED-status
            if current_time - last_toggle_time2 >= blink_interval2:
                led_state2 = not led_state2
                GPIO.output(LED_PIN2, led_state2)
                # Update toggle-tijd
                last_toggle_time2 = current_time
        else:
            # Zet LED uit in andere gevallen
            GPIO.output(LED_PIN2, False)
            led_state2 = False

        # Kleine vertraging om CPU-belasting te beperken
        time.sleep(0.01)

# Foutafhandeling bij onderbreking via toetsenbord (Ctrl+C)
except KeyboardInterrupt:
    GPIO.cleanup()
