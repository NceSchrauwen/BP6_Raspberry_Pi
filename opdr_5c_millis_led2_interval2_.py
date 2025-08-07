# Opdracht 5c Raspberry Pi - Nina Schrauwen
# BTN == HIGH -> LED1 knippert (1s aan / 1s uit)
# BTN == LOW  -> LED2 knippert (1.3s aan / 0.7s uit)

import RPi.GPIO as GPIO
import time

# Functie die de tijd in milliseconden teruggeeft
def millis():
    return int(time.monotonic() * 1000)

# LED- en knopconfiguratie
LED_PIN1 = 17 
LED_PIN2 = 27  
BUTTON_PIN = 18

# Instellen van GPIO voor LEDs en knop
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN1, GPIO.OUT)
GPIO.setup(LED_PIN2, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Statusvariabelen voor LEDs en schakeltijden
led1_state = False
led2_state = False
last_toggle_time1 = millis()
last_toggle_time2 = millis()

try:
    while True:
        # Huidige tijd in milliseconden opslaan
        current_time = millis()
        # Lees de huidige status van de knop uit
        button_state = GPIO.input(BUTTON_PIN)

        # Let op: button_state == 0 betekent ingedrukt (AAN), button_state == 1 betekent niet ingedrukt (UIT) vanwege pull-up
        print(f"Huidige knopstatus: {'AAN' if button_state == 0 else 'UIT'}")

        # Als de knop is ingedrukt, laat LED1 knipperen met onderstaand interval
        if button_state == GPIO.LOW:
            # KNOP INGEDRUKT -> LED1 knippert (1s aan / 1s uit)
            on_duration1 = 1000
            off_duration1 = 1000
            elapsed1 = current_time - last_toggle_time1

            # Zet LED2 (groen) uit
            led2_state = False
            GPIO.output(LED_PIN2, False)

            # Wissel de LED-status als de aan/uit-duur verstreken is en update de schakeltijd
            if led1_state:
                if elapsed1 >= on_duration1:
                    led1_state = False
                    last_toggle_time1 = current_time
            else:
                if elapsed1 >= off_duration1:
                    led1_state = True
                    last_toggle_time1 = current_time

            # Zet LED1 aan of uit op basis van de huidige status
            GPIO.output(LED_PIN1, led1_state)

        # Als de knop niet is ingedrukt, laat LED2 knipperen met onderstaand interval
        else:
            # KNOP NIET INGEDRUKT -> LED2 knippert (1.3s aan / 0.7s uit)
            on_duration2 = 1300
            off_duration2 = 700
            # Meet de verstreken tijd
            elapsed2 = current_time - last_toggle_time2

            # Zet LED1 uit
            led1_state = False
            GPIO.output(LED_PIN1, False)

            # Wissel de LED-status als de aan/uit-duur verstreken is en update de schakeltijd
            if led2_state:
                if elapsed2 >= on_duration2:
                    led2_state = False
                    last_toggle_time2 = current_time
            else:
                if elapsed2 >= off_duration2:
                    led2_state = True
                    last_toggle_time2 = current_time

            # Zet LED2 aan of uit op basis van de huidige status
            GPIO.output(LED_PIN2, led2_state)

        # Korte vertraging om CPU-belasting te beperken
        time.sleep(0.01)

# Foutafhandeling bij toetsenbordonderbreking (Ctrl+C)
except KeyboardInterrupt:
    GPIO.cleanup()
