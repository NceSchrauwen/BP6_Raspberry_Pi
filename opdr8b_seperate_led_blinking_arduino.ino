// Opdracht 8b - Nina Schrauwen
// Receive and extract messages from the Pi to power the leds to blink in the way the Pi instructed them to do so

// Define constants
const int LED1 = 4;
const int LED2 = 7;

// Define interval and other state related variables
unsigned long intervalLED1;
unsigned long intervalLED2;

unsigned long lastToggleLED1 = 0;
unsigned long lastToggleLED2 = 0;
bool led1State = false;
bool led2State = false;

// Other global variables
bool blinking = false;
String input = "";

// Led and serial communication setup
void setup() {
  Serial.begin(9600);
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  digitalWrite(LED1, LOW);
  digitalWrite(LED2, LOW);
}

// Main loop
void loop() {
  // Returns the serial communication and forwards it to the handleCommand function for further processing
  while (Serial.available()) {
    char c = Serial.read();
    // If the message has reached the new line character then forward the compiled messafe to the handleCommand function
    if (c == '\n') {
      handleCommand(input);
      input = "";
    // Keep adding charachters until the message has reached the new line character
    } else {
      input += c;
    }
  }

  // Blink seperately due to different timing intervals 
  if (blinking) {
    // Use millis to get the exact time in milliseconds
    unsigned long now = millis();

    // If the interval that has been given to LED1 has been reached/exceeded then toggle ledstates
    if (now - lastToggleLED1 >= intervalLED1) {
      // Toggle to the opposite ledstate (HIGH to LOW, and vise versa)
      led1State = !led1State;
      digitalWrite(LED1, led1State ? HIGH : LOW);
      // Update the time it has last been toggled to now
      lastToggleLED1 = now;
    }
    // If the interval that has been given to LED2 has been reached/exceeded then toggle ledstates
    if (now - lastToggleLED2 >= intervalLED2) {
      // Toggle to the opposite ledstate (HIGH to LOW, and vise versa)
      led2State = !led2State;
      digitalWrite(LED2, led2State ? HIGH : LOW);
      // Update the time it has last been toggled to now
      lastToggleLED2 = now;
    }
  }
}

// Function to process incoming commands from the pi and take actions based on the incoming messages
void handleCommand(String cmd) {
  if (cmd.startsWith("SET")) {
    int ledPin = -1;
    unsigned long interval = 0;

    // Disect the message into different parts
    int firstSpace = cmd.indexOf(' ');
    int secondSpace = cmd.indexOf(' ', firstSpace + 1);

    // Extract the Led pins and the value from the message
    String led = cmd.substring(firstSpace + 1, secondSpace);
    String value = cmd.substring(secondSpace + 1);
    // Convert the led interval from a string into an int
    interval = value.toInt();

    // If the message contains LED1
    if (led == "LED1") {
      // The interval for LED1 becomes the interval that was listed in the message
      intervalLED1 = interval;
      Serial.println("LED1 interval ingesteld op " + value);
    // If the message contains LED2
    } else if (led == "LED2") {
      // The interval for LED2 becomes the interval that was listed in the message
      intervalLED2 = interval;
      Serial.println("LED2 interval ingesteld op " + value);
    }
  // If the message is just start set blinking to true, this means the blinking sequence can start  
  }
  else if (cmd == "START") {
    blinking = true;
    Serial.println("Knipperen gestart.");
  }
}
