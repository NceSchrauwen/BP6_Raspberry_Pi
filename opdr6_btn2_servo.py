# Opdracht 6 Raspberry Pi - Nina Schrauwen
# BTN1 == HOOG -> Servo draait van 0 naar 120 graden in 1 seconde (aan het einde van de beweging terug naar 0 graden in 1 seconde)
# BTN2 == HOOG -> Servo draait van 0 naar 120 graden in 0.5 seconde (aan het einde van de beweging terug naar 0 graden in 0.5 seconde)

import RPi.GPIO as GPIO
import time

# Servo- en knop pin configuratie
SERVO_PIN = 27
BUTTON1_PIN = 17
BUTTON2_PIN = 18

# GPIO-instellingen
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(BUTTON1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# PWM-instelling voor servo
pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0)

# Functie om de hoek van de servo in te stellen door de hoek om te zetten naar een 'duty cycle'
def set_angle(angle):
    duty = 2 + (angle / 18)
    GPIO.output(SERVO_PIN, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.02)
    GPIO.output(SERVO_PIN, False)

# Functie om de servo naar een bepaalde hoek te bewegen en weer terug
# Functie om de servo naar een bepaalde hoek te bewegen en direct te stoppen als de knop losgelaten wordt
def move_servo_while_pressed(speed_sec, button_pin):
    # Beweeg van 0 naar 120 graden in kleine stapjes
    for angle in range(0, 121, 10):
        if GPIO.input(button_pin):  # Knop losgelaten? Stop zo snel mogelijk (maakt de kleine tussenstap af en stopt dan)
            break
        set_angle(angle)
        time.sleep(speed_sec / (120 / 10)) # Uitrekenen hoelang de kleine tussenstappen duren (graden per seconde / aantal stappen)
    # Beweeg terug naar 0 graden in kleine stapjes
    for angle in range(120, -1, -10):
        if GPIO.input(button_pin):  # Knop losgelaten? Stop zo snel mogelijk (maakt de kleine tussenstap af en stopt dan)
            break
        set_angle(angle)
        time.sleep(speed_sec / (120 / 10)) # Uitrekenen hoelang de kleine tussenstappen duren (graden per seconde / aantal stappen)

# Hoofdlus om knopdrukken te controleren en de servo aan te sturen
try:
    print("Druk op de knoppen om de servo te bedienen.")
    while True:
        # Lees de status van de knoppen
        btn1 = not GPIO.input(BUTTON1_PIN)  # True als knop is ingedrukt
        btn2 = not GPIO.input(BUTTON2_PIN)

        # Als alleen knop 1 is ingedrukt, beweeg de servo met snelheid 1 seconde
        if btn1 and not btn2:
            print("Knop 1 ingedrukt")
            # Beweeg de servo zolang knop 1 is ingedrukt
            while not GPIO.input(BUTTON1_PIN):
                # Beweeg de servo met snelheid 1 seconde
                move_servo_while_pressed(1, BUTTON1_PIN)
                time.sleep(0.1) # Kleine vertraging om snel herhalen te voorkomen
        # Als alleen knop 2 is ingedrukt, beweeg de servo met snelheid 0.5 seconde
        elif btn2 and not btn1:
            print("Knop 2 ingedrukt")
            # Beweeg de servo zolang knop 2 is ingedrukt
            while not GPIO.input(BUTTON2_PIN):
                # Beweeg de servo met snelheid 0.5 seconde
                move_servo_while_pressed(0.5, BUTTON2_PIN)
                time.sleep(0.1) # Kleine vertraging om snel herhalen te voorkomen

# Vang keyboard interrupt op om het programma netjes af te sluiten
except KeyboardInterrupt:
    pass
# Bij andere fouten, reset de GPIO/stop de servo
finally:
    pwm.stop()
    GPIO.cleanup()
