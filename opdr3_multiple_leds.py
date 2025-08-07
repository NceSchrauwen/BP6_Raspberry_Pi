# Opdracht 3: Bestuur 2 LEDs tegelijk
# Naam: Nina Schrauwen
# Beschrijving: Bestuur 2 LEDs tegelijk, na elkaar en met verschillende intervallen. Opdracht onderverdeeld in 3 aparte functies die achter elkaar worden aangeroepen (a t/m c).

# Importeer bibliotheken
import RPi.GPIO as GPIO
import time

# GPIO-pin nummers van de LEDs
LED1 = 17
LED2 = 18

# GPIO-instellingen
GPIO.setmode(GPIO.BCM)  # Gebruik Broadcom SOC-pinnummering
GPIO.setup(LED1, GPIO.OUT)  # Zet pin als output
GPIO.setup(LED2, GPIO.OUT)  # Zet pin als output

# Laat beide LEDs tegelijk knipperen, 1 seconde aan, 1 seconde uit
def opdracht_a():
    print("Opdracht a: Beide LEDs knipperen tegelijk.")
    
    # LEDs 5 keer tegelijk laten knipperen
    for _ in range(5):
        GPIO.output(LED1, GPIO.HIGH)  # Zet LED aan
        GPIO.output(LED2, GPIO.HIGH)  # Zet LED aan
        time.sleep(1)  # Laat LEDs 1 seconde aan
        
        GPIO.output(LED1, GPIO.LOW)  # Zet LED uit
        GPIO.output(LED2, GPIO.LOW)  # Zet LED uit
        time.sleep(1)  # Laat LEDs 1 seconde uit

# Laat de LEDs om de beurt knipperen, elk 1 seconde aan/uit
def opdracht_b():   
    print("Opdracht b: LEDs knipperen om de beurt.")
    
    # LEDs 5 keer om en om laten knipperen
    for _ in range(5):
        GPIO.output(LED1, GPIO.HIGH)  # Zet LED1 aan
        time.sleep(1)
        GPIO.output(LED1, GPIO.LOW)  # Zet LED1 uit
        time.sleep(1)

        GPIO.output(LED2, GPIO.HIGH)  # Zet LED2 aan
        time.sleep(1)
        GPIO.output(LED2, GPIO.LOW)  # Zet LED2 uit
        time.sleep(1)

# Laat beide LEDs tegelijk knipperen met verschillende intervallen
def opdracht_c():   
    print("Opdracht c: Beide LEDs knipperen tegelijk met verschillende intervallen.")
    
    # Definieer de intervallen voor beide LEDs
    led1_intervals = [1.3, 0.7]  # [aan, uit] intervallen voor LED1
    led2_intervals = [0.8, 1.7]  # [aan, uit] intervallen voor LED2

    # Initialiseer LED-statussen en timers
    led1_state = GPIO.HIGH
    led2_state = GPIO.HIGH
    # Start met interval[0] omdat de LEDs beginnen met HIGH
    led1_timer = time.time() + led1_intervals[0]
    led2_timer = time.time() + led2_intervals[0]
    # Houd bij hoelang de LED daadwerkelijk aan of uit is geweest
    led1_last_interval = time.time()
    led2_last_interval = time.time()

    # Starttijd ophalen
    start_time = time.time()
    # Voer de knippervolgorde 10 seconden uit
    while time.time() - start_time < 10:
        current_time = time.time()

        # Controleer of timer verlopen is → wissel status LED1 (toggle LED1 HIGH/LOW)
        if current_time >= led1_timer:
            actual_interval1 = current_time - led1_last_interval
            print(f"LED1 {'AAN' if led1_state == GPIO.HIGH else 'UIT'} gedurende {actual_interval1:.2f} seconden")
            led1_state = GPIO.LOW if led1_state == GPIO.HIGH else GPIO.HIGH
            GPIO.output(LED1, led1_state)
            led1_timer = current_time + (led1_intervals[0] if led1_state == GPIO.HIGH else led1_intervals[1])
            led1_last_interval = current_time

        # Controleer of timer verlopen is → wissel status LED2 (toggle LED2 HIGH/LOW)
        if current_time >= led2_timer:
            actual_interval2 = current_time - led2_last_interval
            print(f"LED2 {'AAN' if led2_state == GPIO.HIGH else 'UIT'} gedurende {actual_interval2:.2f} seconden")
            led2_state = GPIO.LOW if led2_state == GPIO.HIGH else GPIO.HIGH
            GPIO.output(LED2, led2_state)
            led2_timer = current_time + (led2_intervals[0] if led2_state == GPIO.HIGH else led2_intervals[1])
            led2_last_interval = current_time

        # Korte vertraging om CPU-gebruik te beperken
        time.sleep(0.01)

# Voer de opdrachten een voor een uit
try:
    opdracht_a()
    opdracht_b()
    opdracht_c()

# Reset GPIO-instellingen, ook als er fouten optreden of het script wordt onderbroken
finally:
    GPIO.cleanup()
    print("GPIO-reset voltooid.")
