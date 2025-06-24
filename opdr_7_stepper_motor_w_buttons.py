# Opdracht 7 Raspberry Pi - Nina Schrauwen
# Beschrijving: Dit script stuurt een steppermotor aan via een ULN2003 driver op basis van drukknoppen.

import RPi.GPIO as GPIO
import time

# Definieer GPIO-pinnen die verbonden zijn met IN1-IN4 van de ULN2003 driver
IN1 = 17  # IN1
IN2 = 18  # IN2
IN3 = 27  # IN3
IN4 = 22  # IN4

# Definieer GPIO-pinnen voor de drukknoppen
BTN = 24  # BTN1
BTN2 = 25  # BTN2

# Gebruik BCM-pin nummering
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Stel de motorpinnen in als uitgang
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

# Stel de knop-pinnen in als input met pull-up weerstanden
# Interne pull-up weerstand geactiveerd: de standaardwaarde is HIGH (1), dus wanneer de knop wordt ingedrukt is de waarde LOW (0)
GPIO.setup(BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(BTN2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Aantal stappen voor een volledige 360° rotatie
step_count = 4096
# Tijd (in seconden) voor een volledige rotatie
time_rotation = None 

# Half-step volgorde (8 stappen per cyclus)
# Deze methode zorgt voor soepelere rotatie dan volledige stappen (die gebruiken 4 stappen per cyclus)
step_sequence = [
    [1, 0, 0, 1],  # Stap 1
    [1, 0, 0, 0],  # Stap 2
    [1, 1, 0, 0],  # Stap 3
    [0, 1, 0, 0],  # Stap 4
    [0, 1, 1, 0],  # Stap 5
    [0, 0, 1, 0],  # Stap 6
    [0, 0, 1, 1],  # Stap 7
    [0, 0, 0, 1]   # Stap 8
]

# Functie om de motor te laten draaien in een bepaalde richting zolang een knop ingedrukt wordt
def step_motor(btn_pin, delay=None, direction=None):
    # Kies de juiste stapvolgorde op basis van de richting.
    # Als 'direction' "forward" is, gebruik normale volgorde, anders omgekeerde volgorde (voor achterwaartse rotatie)
    sequence = step_sequence if direction == "forward" else step_sequence[::-1]
    
    # Herhaal zolang de knop is ingedrukt (actief laag)
    while(GPIO.input(btn_pin) == GPIO.LOW):
        for step in sequence:
            GPIO.output(IN1, step[0])
            GPIO.output(IN2, step[1])
            GPIO.output(IN3, step[2])
            GPIO.output(IN4, step[3])
            time.sleep(delay)

# Functie om de tijd per stap te berekenen op basis van gewenste rotatietijd
def calculate_time_rotation(given_time):
    global step_count, time_rotation
    
    # Bereken de tijd per stap door de tijd van de rotatie door het stappen aantal te delen
    if given_time is not None:
        time_rotation = given_time
        time_per_step = time_rotation / step_count
        return time_per_step
    # Als er geen rotatietijd is opgegeven, geef een standaardvertraging terug zodat de motor toch blijft werken
    else:
        print(f"Rotatietijd van {time_rotation} seconden is niet ingesteld.")
        return 0.001  # Standaard vertraging als fallback

# Het programma draait continu in een lus totdat het handmatig wordt gestopt
try:
    print("Klaar om de steppermotor aan te sturen.")
    
    # Main loop van de applicatie
    while True:
        # Lees de status van beide knoppen
        # GPIO.LOW betekent dat de knop is ingedrukt (omdat we pull-up gebruiken)
        button_state = GPIO.input(BTN)
        button_state2 = GPIO.input(BTN2)

        # Als alleen de eerste knop is ingedrukt, draai voorwaarts (linksom) met 5 seconden per omwenteling
        if button_state == GPIO.LOW and button_state2 != GPIO.LOW:
            print("Draait voorwaarts met 5 sec per 360° rotatie...")
            time_rotation = 5
            # Bereken tijd per stap op basis van totale gewenste rotatietijd
            calculated_time = calculate_time_rotation(time_rotation)
            # Beweeg de motor op basis van de knop input, de berekende tijd per stap en de richting die is meegegeven
            step_motor(btn_pin=BTN, delay=calculated_time, direction="forward")

        # Als alleen de tweede knop is ingedrukt, draai achterwaarts (rechtsom) met 12 seconden per omwenteling
        elif button_state2 == GPIO.LOW and button_state != GPIO.LOW:
            print("Draait achterwaarts met 12 sec per 360° rotatie...")
            time_rotation = 12
            # Bereken tijd per stap op basis van totale gewenste rotatietijd
            calculated_time = calculate_time_rotation(time_rotation)
            # Beweeg de motor op basis van de knop input, de berekende tijd per stap en de richting die is meegegeven
            step_motor(btn_pin=BTN2, delay=calculated_time, direction="backwards")

        # Kleine vertraging om CPU-gebruik te beperken
        time.sleep(0.05)

# Zorg ervoor dat alle GPIO-instellingen netjes worden teruggezet bij het afsluiten
finally:
    GPIO.cleanup()
  
