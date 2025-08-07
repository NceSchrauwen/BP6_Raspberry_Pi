// Opdracht 8c Raspberry Pi - Nina Schrauwen
// Als de knop wordt ingedrukt, wisselen de LEDs tussen LED1 en LED2.
// Dit programma laat de pi weten wanneer een knop wordt ingedrukt en ontvangt signalen om de led-statussen te wisselen.

// Definieer constante imports
const int BUTTON = 8;
const int LED1 = 4;
const int LED2 = 7;

// Globale variabelen voor status en string
int lastButtonState = HIGH;
String input = "";

// Setup van LED, knop en seriële communicatie
void setup() {
  Serial.begin(9600);
  pinMode(BUTTON, INPUT_PULLUP);
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  // Begin met beide LEDs uit
  digitalWrite(LED1, LOW);
  digitalWrite(LED2, LOW);
  Serial.println("Arduino klaar");
}

// Hoofdlus om te bepalen of een knop is ingedrukt en of de led-statussen moeten worden gewisseld
void loop() {
  // Lees de status van de knop
  int currentState = digitalRead(BUTTON);
  // Als een knop is ingedrukt, stuur een bericht naar de pi
  if (lastButtonState == HIGH && currentState == LOW) {
    Serial.println("BUTTON_PRESS");
    delay(200);  // eenvoudige debounce
  }
  // Update de lastButtonState naar de huidige ledstatus
  lastButtonState = currentState;

  // Als er seriële communicatie is ontvangen
  while (Serial.available()) {
    // Lees het karakter van een groter bericht van de huidige seriële communicatie
    char c = Serial.read();
    // Als het einde van de regel is bereikt, bepaal welk bericht het is en onderneem actie
    if (c == '\n') {
      // Verwijder witruimte uit het bericht
      input.trim();
      // Als het bericht "LED1" is, zet die led aan en de andere uit
      if (input == "LED1") {
        digitalWrite(LED1, HIGH);
        digitalWrite(LED2, LOW);
      // Als het bericht "LED2" is, zet die led aan en de andere uit
      } else if (input == "LED2") {
        digitalWrite(LED1, LOW);
        digitalWrite(LED2, HIGH);
      }
      // Anders wordt de input weer leeg gemaakt
      input = "";
    // Als het einde van de regel nog niet is bereikt, blijf tekens toevoegen
    } else {
      input += c;
    }
  }
}
