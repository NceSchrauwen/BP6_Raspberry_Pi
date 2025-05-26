// Opdracht 8c Raspberry Pi - Nina Schrauwen
// If the button is pressed, the LEDs will toggle between LED1 and LED2.
// This program lets the pi know when a button is pressed and receives signals to toggle the led states

// Define constant imports 
const int BUTTON = 8;
const int LED1 = 4;
const int LED2 = 7;

// State and string global variables
int lastButtonState = HIGH;
String input = "";

// LED, button and serial communication setup
void setup() {
  Serial.begin(9600);
  pinMode(BUTTON, INPUT_PULLUP);
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  // Start of with both LEDs being off
  digitalWrite(LED1, LOW);
  digitalWrite(LED2, LOW);
  Serial.println("Arduino ready");
}

// Main loop to determine if a button is pressed and if led states need to be toggled
void loop() {
  // Read the button state
  int currentState = digitalRead(BUTTON);
  // If a button is pressed sent a message to the pi
  if (lastButtonState == HIGH && currentState == LOW) {
    Serial.println("BUTTON_PRESS");
    delay(200);  // basic debounce
  }
  // Update the lastButtonState to the current ledstate
  lastButtonState = currentState;

  // If serial communication is received
  while (Serial.available()) {
    // To read the character of a larger message of the current serial communcation
    char c = Serial.read();
    // If end of line character has been reached determine which message it is and act on it
    if (c == '\n') {
      // Trim the message from whitespace
      input.trim();
      // If the message says LED1, turn on the ledstate and turn off the ledstate of LED2
      if (input == "LED1") {
        digitalWrite(LED1, HIGH);
        digitalWrite(LED2, LOW);
      // If the message says LED2, turn on the ledstate and turn off the ledstate of LED1
      } else if (input == "LED2") {
        digitalWrite(LED1, LOW);
        digitalWrite(LED2, HIGH);
      }
      // Otherwise input is set to nothing 
      input = "";
    // If the end of the line has not been reached keep adding the characters
    } else {
      input += c;
    }
  }
}
