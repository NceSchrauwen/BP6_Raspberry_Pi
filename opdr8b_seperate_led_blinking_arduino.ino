// Opdracht 8b - Nina Schrauwen
// Ontvang en verwerk berichten van de Pi om de leds te laten knipperen zoals de Pi dat heeft aangegeven

// Definieer constanten
const int LED1 = 4;
const int LED2 = 7;

// Definieer interval- en statusgerelateerde variabelen
unsigned long intervalLED1;
unsigned long intervalLED2;

unsigned long lastToggleLED1 = 0;
unsigned long lastToggleLED2 = 0;
bool led1State = false;
bool led2State = false;

// Andere globale variabelen
bool blinking = false;
String input = "";

// Setup voor leds en seriële communicatie
void setup() {
  Serial.begin(9600);
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  digitalWrite(LED1, LOW);
  digitalWrite(LED2, LOW);
}

// Hoofdlus
void loop() {
  // Leest de seriële communicatie uit en stuurt deze door naar de handleCommand-functie voor verdere verwerking
  while (Serial.available()) {
    char c = Serial.read();
    // Als het bericht eindigt op een newline-karakter, stuur dan het volledige bericht door naar de handleCommand-functie
    if (c == '\n') {
      handleCommand(input);
      input = "";
    // Blijf tekens toevoegen totdat het newline-karakter is bereikt
    } else {
      input += c;
    }
  }

  // Laat leds afzonderlijk knipperen vanwege verschillende intervaltijden
  if (blinking) {
    // Gebruik millis om de huidige tijd in milliseconden op te halen
    unsigned long now = millis();

    // Als het interval voor LED1 is bereikt of overschreden, wissel de LED-status
    if (now - lastToggleLED1 >= intervalLED1) {
      // Wissel naar de tegenovergestelde status (HIGH naar LOW en omgekeerd)
      led1State = !led1State;
      digitalWrite(LED1, led1State ? HIGH : LOW);
      // Update het tijdstip waarop de LED voor het laatst is gewisseld
      lastToggleLED1 = now;
    }
    // Als het interval voor LED2 is bereikt of overschreden, wissel de LED-status
    if (now - lastToggleLED2 >= intervalLED2) {
      // Wissel naar de tegenovergestelde status (HIGH naar LOW en omgekeerd)
      led2State = !led2State;
      digitalWrite(LED2, led2State ? HIGH : LOW);
      // Update het tijdstip waarop de LED voor het laatst is gewisseld
      lastToggleLED2 = now;
    }
  }
}

// Functie om inkomende commando’s van de Pi te verwerken en acties uit te voeren op basis van het bericht
void handleCommand(String cmd) {
  if (cmd.startsWith("SET")) {
    int ledPin = -1;
    unsigned long interval = 0;

    // Splits het bericht op in verschillende onderdelen
    int firstSpace = cmd.indexOf(' ');
    int secondSpace = cmd.indexOf(' ', firstSpace + 1);

    // Haal de LED-pin en waarde uit het bericht
    String led = cmd.substring(firstSpace + 1, secondSpace);
    String value = cmd.substring(secondSpace + 1);
    // Zet het interval voor de LED om van string naar int
    interval = value.toInt();

    // Als het bericht betrekking heeft op LED1
    if (led == "LED1") {
      // Stel het interval van LED1 in op de opgegeven waarde
      intervalLED1 = interval;
      Serial.println("LED1-interval ingesteld op " + value);
    // Als het bericht betrekking heeft op LED2
    } else if (led == "LED2") {
      // Stel het interval van LED2 in op de opgegeven waarde
      intervalLED2 = interval;
      Serial.println("LED2-interval ingesteld op " + value);
    }
  // Als het bericht "START" is, stel blinking in op true zodat het knipperen begint
  }
  else if (cmd == "START") {
    blinking = true;
    Serial.println("Knipperen gestart.");
  }
}
