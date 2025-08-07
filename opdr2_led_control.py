# Opdracht 2: LED aansturing
# Naam: Nina Schrauwen
# Omschrijving: Stuur een LED aan met verschillende knipperintervallen

# Importeren van bibliotheken
import RPi.GPIO as GPIO
import time

# GPIO pin nummer van de LED
LED = 18

# GPIO setup
GPIO.setmode(GPIO.BCM) # Gebruik Broadcom SOC kanaalnummering
GPIO.setup(LED, GPIO.OUT) # Zet pin als uitgang

# Functie om LED te laten knipperen met opgegeven interval
def blink_led(snelheid_aan, snelheid_uit, herhalingen):
    for _ in range(herhalingen):
        GPIO.output(LED, GPIO.HIGH) # Zet LED aan
        time.sleep(snelheid_aan) # Duur van het aan-interval
        GPIO.output(LED, GPIO.LOW) # Zet LED uit
        time.sleep(snelheid_uit) # Duur van het uit-interval

# Laat LED knipperen met verschillende intervallen door de blink_led() functie aan te roepen
try:
    print("Opdracht a: Knippersnelheid is 1 seconde aan, 1 seconde uit.")
    blink_led(1, 1, 5)

    print("Opdracht b: Knippersnelheid is 1 seconde aan, 2 seconden uit.")
    blink_led(1, 2, 5)

    print("Opdracht c: Knippersnelheid is 0.1 seconde aan, 0.1 seconde uit.")
    blink_led(0.1, 0.1, 25)

    print("Opdracht d: De illusie wekken dat de LED altijd aan is door het korte knipperinterval.")
    blink_led(0.01, 0.01, 100)

# Maak de GPIO-instellingen schoon
finally:
    GPIO.cleanup()
    print("GPIO schoonmaak voltooid.")
    
