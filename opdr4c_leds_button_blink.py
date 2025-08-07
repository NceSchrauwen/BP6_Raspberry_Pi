# Opdracht 4c Raspberry Pi - Nina Schrauwen
# 1x indrukken = 1,3 sec aan/0,7 sec uit voor Led 1 (Led 2 is uit) 
# 2x indrukken = 1,3 sec aan/0,7 sec uit voor Led 1 EN Led 2 is aan 
# 3x indrukken = Reset LEDS (alles uit)

import RPi.GPIO as GPIO
import time
import threading

# Pinconfiguratie
BUTTON_PIN = 18
LED_PIN = 17
LED_PIN2 = 27

# Instellen van de leds en knop
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)
GPIO.setup(LED_PIN2, GPIO.OUT)
GPIO.output(LED_PIN2, GPIO.LOW)

# Status van knop/led-configuratie
press_count = 0
blinking = False
blink_thread = None

# Functie om de LED te laten knipperen in een lus (1,3 sec aan/0,7 sec uit)
def blink_led():
    while blinking:
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(1.3)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(0.7)

# Functie om te bepalen welke LED aan/uit moet op basis van het aantal drukken
def handle_press():
    global press_count, blinking, blink_thread

    # Er is op de knop gedrukt dus moet het press_count met 1 omhoog
    press_count += 1
    print(f"Knop {press_count} keer ingedrukt")
    
    # Bij één keer drukken: laat de eerste LED knipperen en zet de tweede uit
    if press_count == 1:
        blinking = True
        GPIO.output(LED_PIN2, GPIO.LOW)  # Zorg dat LED2 uit is
        # Start de knipper-thread voor LED1
        if blink_thread is None or not blink_thread.is_alive():
            blink_thread = threading.Thread(target=blink_led, daemon=True)
            blink_thread.start()

    # Bij twee keer drukken: laat de eerste LED knipperen en zet de tweede aan
    elif press_count == 2:
        blinking = True
        GPIO.output(LED_PIN2, GPIO.HIGH) # Zet LED2 aan (niet knipperen)
        print("LED2 aanzetten")
        # Start de knipper-thread voor LED1 (indien nog niet gestart of gestopt)
        if blink_thread is None or not blink_thread.is_alive():
            blink_thread = threading.Thread(target=blink_led, daemon=True)
            blink_thread.start()

    # Bij drie keer drukken: zet beide leds uit (reset)
    elif press_count >= 3:
        # Reset alles en zet beiden leds uit
        blinking = False
        GPIO.output(LED_PIN, GPIO.LOW)
        GPIO.output(LED_PIN2, GPIO.LOW)
        press_count = 0
        print("LEDs resetten")

try:
    print("Druk op de knop...")
    # Blijf luisteren naar knoppen
    while True:
        # Als de knop wordt ingedrukt, zorg dan dat handle_press() wordt aangeroepen
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            handle_press()
            # Kleine vertraging tussen statuswisselingen
            while GPIO.input(BUTTON_PIN) == GPIO.LOW:
                time.sleep(0.01)  # Wacht tot knop losgelaten
            time.sleep(0.2)  # Debounce

# Als je de terminal afsluit
except KeyboardInterrupt:
    print("\nAfsluiten...")
# Zet blinking op False en geef de blink-thread tijd om te stoppen
finally:
    blinking = False
    time.sleep(0.1)  
    GPIO.cleanup()
    
