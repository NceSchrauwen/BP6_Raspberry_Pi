// Opdracht 8a - Nina Schrauwen
// Dit programma ontvangt en voert de commando’s uit die via de Pi worden verzonden
// Definieer constante variabelen
const int LED1 = 4;
const int LED2 = 7;

// Setup van de leds en de seriële communicatie
void setup() {
  Serial.begin(9600);
  pinMode(LED1, OUTPUT);  
  pinMode(LED2, OUTPUT);  
  digitalWrite(LED1, LOW);
  digitalWrite(LED2, LOW);
}

// Hoofdlus om de ontvangen commando’s van de Pi te vertalen en uit te voeren
void loop() {
  // Als er een seriële verbinding is gemaakt met de Pi
  if (Serial.available()) {
    Serial.println("Verbonden met Pi");
    // Lees het commando uit
    char cmd = Serial.read();
    // Commando om LED1 aan te zetten en LED2 uit (knippervolgorde)
    if (cmd == 'A') {
      Serial.println("Eerste volgorde");
      digitalWrite(LED1, HIGH);
      digitalWrite(LED2, LOW);
    // Commando om LED2 aan te zetten en LED1 uit (knippervolgorde)
    } else if (cmd == 'B') {
      Serial.println("Tweede volgorde"); 
      digitalWrite(LED1, LOW);
      digitalWrite(LED2, HIGH);
    }
  }
}
