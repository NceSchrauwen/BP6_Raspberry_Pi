#include <IRremote.hpp>

// Definieer constante variabele (IR receiver pin)
const int RECV_PIN = 2;

void setup() {
  // Start seriële communicatie 
  Serial.begin(9600);
  // Start de IR receiver
  IrReceiver.begin(RECV_PIN, ENABLE_LED_FEEDBACK);  
  Serial.println("IR Ready...");
}

// Hoofdlus functie om IR codes te kunnen ontvangen, verwerken en versturen naar de Raspberry Pi
void loop() {
  // Als er een signaal ontvangen wordt door de IR receiver
  if (IrReceiver.decode()) {
    // Zet het signaal om naar een HEX formaat 
    uint32_t rawCode = IrReceiver.decodedIRData.decodedRawData;

    // Match de HEX codes met de knop nummers op de remote
    // Deze HEX code komt overeen met de eerste knop, print het bericht
    if (rawCode == 0xBA45FF00) {
      Serial.println("BTN:1");
    // Deze HEX code komt overeen met de tweede knop, print het bericht
    } else if (rawCode == 0xB946FF00) {
      Serial.println("BTN:2");
    // Deze HEX code komt overeen met de derde knop, print het bericht
    } else if (rawCode == 0xB847FF00) {
      Serial.println("BTN:3");
    // Deze HEX code komt overeen met de vierde knop, print het bericht
    } else if (rawCode == 0xBB44FF00) {
      Serial.println("BTN:4");
    // Bericht komt niet overeen met knop 1 tm 4 dus is het een onbekende knop, print het bericht met de onbekende HEX code
    } else {
      Serial.print("Unknown code: 0x");
      Serial.println(rawCode, HEX);
    }
    
    // Zet IR receiver klaar om een nieuw signaal te ontvangen, met cooldown om herhaalde invoer te voorkomen.
    IrReceiver.resume();  
    delay(200);           
  }
}
