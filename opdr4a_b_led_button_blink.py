# Opdracht 4a+b Raspberry Pi - Nina Schrauwen
# Beschrijving: Wanneer de knop wordt ingedrukt dan begint de LED te knipperen, bij opnieuw indrukken gaat de LED uit.

import RPi.GPIO as GPIO
import time
import threading

# Pinconfiguratie
BUTTON_PIN = 17
LED_PIN = 18

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Pull-up knop
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)  # Start met LED uit

# Status
led_on = False
press_count = 0
led_blinking = False  # Vlag om knipperstatus te regelen

print("Druk op de knop om de LED aan/uit te zetten.")

# Functie om de LED te laten knipperen
def blink_led():
    while led_blinking:
        GPIO.output(LED_PIN, GPIO.HIGH)  # Zet de LED aan
        time.sleep(1)  # Laat de LED 1 seconde aan
        GPIO.output(LED_PIN, GPIO.LOW)   # Zet de LED uit
        time.sleep(1)  # Laat de LED 1 seconde uit

try:
    while True:
        button_state = GPIO.input(BUTTON_PIN)

        if button_state == GPIO.LOW:  # Knop is ingedrukt
            led_on = not led_on

            # Als de led wordt ingedrukt, start met knipperen (dmv thread)
            if led_on:
                press_count += 1
                led_blinking = True  # Zet vlag zodat LED mag knipperen
                print(f"LED AAN ({press_count} keer)")

                # Start een thread om te voorkomen dat de knipperlus de hoofdcode blokkeert
                blink_thread = threading.Thread(target=blink_led)
                blink_thread.daemon = True  # Thread stopt automatisch bij afsluiten
                blink_thread.start()
                
            # Als de led niet wordt ingedrukt, zet de LED uit en werk de vlag bij
            else:
                print("LED UIT")
                GPIO.output(LED_PIN, GPIO.LOW)  # Zet LED uit
                led_blinking = False  # Zet vlag uit zodat knipperen stopt
            
            # Debounce-vertraging
            while GPIO.input(BUTTON_PIN) == GPIO.LOW:
                time.sleep(0.01)  # Wacht tot knop wordt losgelaten
            time.sleep(0.1)  # Voorkom stuiteren (bouncing)

except KeyboardInterrupt:
    # Vang handmatige onderbreking af (Ctrl+C)
    print("\nAfsluiten...")

finally:
    # Reset GPIO-instellingen (ook bij fouten)
    GPIO.cleanup()
